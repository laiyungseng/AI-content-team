#!/usr/bin/env python3
"""Content performance dashboard: validate, analyze, assemble.

  python3 build.py reuse   OLD_INDEX.html config.json
      Refresh runs: recover handles, topics (with their colors, verbatim),
      window and title from the published page.

  python3 build.py analyze config.json posts.tsv
      Print what the insights need, computed exactly as the page does:
      every post ranked by outlier score with its quadrant, and topic rows.

  python3 build.py build   config.json posts.tsv OUT.html
      Validate, inject into the template, syntax-check.

posts.tsv: one post per line, tab-separated, no header, 11 columns:
  platform  postId  timestamp  views  likes  comments  shares  saves  durationSec  topic  caption
  - platform: instagram | tiktok (ig | tt also accepted)
  - postId: Instagram shortCode, TikTok numeric video id
  - timestamp: ISO 8601 as Apify returns it
  - empty cell = null. Instagram shares/saves are always null.
  - caption: first 120 characters, no tabs, line breaks written as \\n
"""
import json, re, subprocess, sys, tempfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "perf_template.html"
PALETTE = ["var(--t-case)", "var(--t-brand)", "var(--t-tut)", "var(--t-bts)", "var(--t-show)"]
UNCAT = {"label": "Uncategorized", "color": "var(--t-unk)",
         "description": "Posts that don't fit any of the themes above. Reassign from the table below."}
PLAT = {"instagram": "instagram", "ig": "instagram", "tiktok": "tiktok", "tt": "tiktok"}
QUAD = {"both": "both", "reach_only": "reach-only", "eng_only": "eng-only", "neither": "neither"}


def die(msg):
    sys.exit("FAILED: " + msg)


def script_blocks(html):
    a = html.find("<script>")
    b = html.find("</script>", a)
    return a, b + len("</script>")


def parse_ts(s, where):
    try:
        return datetime.fromisoformat(s.strip().replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        die(f"{where}: timestamp '{s}' is not ISO 8601")


# ---------------------------------------------------------------- reuse
def reuse(old_html, out_cfg):
    s = Path(old_html).read_text(encoding="utf-8")
    a, b = script_blocks(s)
    block = s[a + len("<script>"): b - len("</script>")]
    dump = (";console.log(JSON.stringify({TOPIC_META, PLATFORM_META, PULL_WINDOW_DAYS,"
            " INSIGHTS: (typeof INSIGHTS==='undefined'?null:INSIGHTS)}))")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(block + dump)
    r = subprocess.run(["node", f.name], capture_output=True, text=True)
    if r.returncode != 0:
        die("could not read the old page's config block:\n" + r.stderr[-800:])
    d = json.loads(r.stdout)
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    cfg = {
        "title": t.group(1).strip() if t else "Content Performance",
        "pulledAt": "SET_ME",
        "windowDays": d["PULL_WINDOW_DAYS"],
        "handles": {k: v["handle"].lstrip("@") for k, v in d["PLATFORM_META"].items()},
        "topics": d["TOPIC_META"],
        "insights": {"headline": "",
                     "quadrants": {p: {q: "" for q in QUAD} for p in ("instagram", "tiktok")},
                     "topics": {"instagram": "", "tiktok": ""}},
    }
    Path(out_cfg).write_text(json.dumps(cfg, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_cfg}: topics kept verbatim ({', '.join(cfg['topics'])}), "
          f"window {cfg['windowDays']} days. Set pulledAt; insights are blank and must be rewritten.")


# ---------------------------------------------------------------- load + validate
def load(cfg_path, tsv_path):
    cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
    for k in ("pulledAt", "windowDays", "handles", "topics"):
        if k not in cfg:
            die(f"config.json is missing '{k}'")
    if cfg["windowDays"] not in (7, 30, 90):
        die("windowDays must be 7, 30 or 90")
    pulled = parse_ts(str(cfg["pulledAt"]), "config.json pulledAt")
    handles = {p: str(cfg["handles"].get(p, "")).lstrip("@") for p in ("instagram", "tiktok")}
    if not all(handles.values()):
        die("config.json handles needs both instagram and tiktok")

    topics, used = {}, set()
    for key, t in cfg["topics"].items():
        if key == "uncategorized":
            continue
        if "label" not in t:
            die(f"topic '{key}' needs a label")
        topics[key] = {"label": t["label"], "color": t.get("color"), "description": t.get("description", "")}
        if t.get("color"):
            used.add(t["color"])
    free = [c for c in PALETTE if c not in used]
    for key, t in topics.items():
        if not t["color"]:
            if not free:
                die("more themes than the 5 validated topic colors; use at most 5 themes plus uncategorized")
            t["color"] = free.pop(0)
    topics["uncategorized"] = {**UNCAT, **cfg["topics"].get("uncategorized", {})}

    earliest = (pulled - timedelta(days=cfg["windowDays"])).date()
    posts, seen = [], set()
    for ln, raw in enumerate(Path(tsv_path).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        c = raw.split("\t", 10)
        w = f"posts.tsv line {ln}"
        if len(c) < 10:
            die(f"{w}: expected 11 tab-separated columns, got {len(c)}")
        c += [""] * (11 - len(c))
        plat = PLAT.get(c[0].strip().lower())
        if not plat:
            die(f"{w}: platform '{c[0]}' must be instagram or tiktok")
        pid = c[1].strip()
        if not pid:
            die(f"{w}: empty postId")
        ts = parse_ts(c[2], w)
        if ts.date() < earliest:
            die(f"{w}: posted {ts.date()}, before the {cfg['windowDays']}-day window ({earliest}); drop it")
        if ts > pulled + timedelta(days=1):
            die(f"{w}: posted after pulledAt")
        topic = c[9].strip()
        if topic not in topics:
            die(f"{w}: topic '{topic}' is not in config.json topics")
        if (plat, pid) in seen:
            continue
        seen.add((plat, pid))

        def num(cell, integer=True):
            cell = cell.strip()
            if cell == "" or cell.lower() in ("null", "none"):
                return None
            try:
                v = float(cell.replace(",", ""))
            except ValueError:
                die(f"{w}: '{cell}' is not a number")
            if v < 0:
                die(f"{w}: negative number")
            return int(round(v)) if integer else round(v, 2)

        shares, saves = num(c[6]), num(c[7])
        if plat == "instagram":
            shares = saves = None
        caption = c[10].replace("\\n", "\n").replace("\t", " ").strip()[:120]
        posts.append({
            "id": ("ig_" if plat == "instagram" else "tt_") + pid,
            "platform": plat,
            "url": (f"https://www.instagram.com/p/{pid}/" if plat == "instagram"
                    else f"https://www.tiktok.com/@{handles['tiktok']}/video/{pid}"),
            "caption": caption,
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "views": num(c[3]), "likes": num(c[4]) or 0, "comments": num(c[5]) or 0,
            "shares": shares, "saves": saves, "durationSec": num(c[8], integer=False),
            "topic": topic,
        })
    for plat in ("instagram", "tiktok"):
        if not any(p["platform"] == plat for p in posts):
            die(f"no {plat} posts; the page needs at least one post per platform")
    posts.sort(key=lambda p: p["timestamp"], reverse=True)
    return cfg, topics, handles, posts


# ---------------------------------------------------------------- analyze (mirrors the page)
def median(xs):
    s = sorted(xs)
    if not s:
        return None
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def rich(p):
    return p["likes"] + p["comments"] + (p["shares"] or 0) + (p["saves"] or 0)


def analyze(cfg_path, tsv_path):
    cfg, topics, handles, posts = load(cfg_path, tsv_path)
    for plat in ("instagram", "tiktok"):
        allp = [p for p in posts if p["platform"] == plat]
        ps = [p for p in allp if p["views"] is not None]          # same rule as the page
        photos = [p for p in allp if p["views"] is None]
        print(f"\n=== {plat.upper()}  {len(allp)} posts, {len(ps)} with a view count ===")
        if not ps:
            print("no posts with a view count; view-based sections will be empty")
        else:
            mv = median([p["views"] for p in ps])
            me = median([(rich(p) / p["views"]) if p["views"] > 0 else 0 for p in ps])
            print(f"typical views {mv:,.0f} | typical engagement {me*1000:.1f} per 1,000 viewers")
            rows = []
            for p in ps:
                v = p["views"]
                out = (v / mv) if mv else 0
                er = rich(p) / v if v > 0 else 0
                q = ("both" if v >= mv and er >= me else "reach_only" if v >= mv
                     else "eng_only" if er >= me else "neither")
                rows.append((out, q, p, er))
            rows.sort(key=lambda r: -r[0])
            print(f"{'rank':>4} {'score':>6} {'quadrant':<10} {'topic':<16} {'views':>8} {'eng/1k':>7} {'dur':>5}  first line")
            for i, (out, q, p, er) in enumerate(rows, 1):
                fl = (p["caption"].split("\n")[0])[:70]
                dur = f"{p['durationSec']:.0f}s" if p["durationSec"] is not None else "-"
                print(f"{i:>4} {out:>5.1f}x {QUAD[q]:<10} {p['topic'][:16]:<16} {p['views']:>8,} "
                      f"{er*1000:>7.1f} {dur:>5}  {fl}  [{p['id']}]")
            counts = defaultdict(int)
            for r in rows:
                counts[r[1]] += 1
            print("quadrants:", ", ".join(f"{QUAD[k]}={counts[k]}" for k in QUAD))
            g = defaultdict(list)
            for out, q, p, er in rows:
                g[p["topic"]].append(out)
            trows = sorted(((sum(v) / len(v), k, len(v)) for k, v in g.items()), reverse=True)
            print("topics (as the page ranks them, top first):",
                  "; ".join(f"{k} n={n} avg {a:.1f}x" for a, k, n in trows))
            thin = [k for a, k, n in trows if n < 5]
            if thin:
                print("under 5 posts, describe only, do not prescribe:", ", ".join(thin))
        if photos:
            print(f"photo/carousel posts (no view count, left out of every view-based number; "
                  f"compare them only with each other, by likes + comments):")
            for p in sorted(photos, key=lambda p: -(p["likes"] + p["comments"])):
                print(f"     likes {p['likes']:>6,} comments {p['comments']:>5,}  {p['topic'][:16]:<16} "
                      f"{p['caption'].split(chr(10))[0][:70]}  [{p['id']}]")


# ---------------------------------------------------------------- build
def js(obj):
    return json.dumps(obj, ensure_ascii=False, indent=None, separators=(",", ":")).replace("</", "<\\/")


def build(cfg_path, tsv_path, out_path):
    cfg, topics, handles, posts = load(cfg_path, tsv_path)
    ins = cfg.get("insights") or {}
    insights = {
        "headline": ins.get("headline", ""),
        "quadrants": {p: {q: (ins.get("quadrants", {}).get(p, {}) or {}).get(q, "") for q in QUAD}
                      for p in ("instagram", "tiktok")},
        "topics": {p: (ins.get("topics") or {}).get(p, "") for p in ("instagram", "tiktok")},
    }
    if not insights["headline"].strip():
        print("WARN headline insight is empty; the 'What to do next' card will not show")
    block = (
        "<script>\n"
        f"const SEED_POSTS = {js(posts)};\n"
        f"const TOPIC_META = {js(topics)};\n"
        "const PLATFORM_META = " + js({
            "instagram": {"label": "Instagram", "color": "var(--ig)", "handle": "@" + handles["instagram"]},
            "tiktok": {"label": "TikTok", "color": "var(--tt)", "handle": "@" + handles["tiktok"]}}) + ";\n"
        "const PROFILES = " + js({
            "instagram": f"https://www.instagram.com/{handles['instagram']}/",
            "tiktok": f"https://www.tiktok.com/@{handles['tiktok']}"}) + ";\n"
        f"const PULL_WINDOW_DAYS = {cfg['windowDays']};\n"
        f"const PULLED_AT = {js(cfg['pulledAt'])};\n"
        f"const INSIGHTS = {js(insights)};\n"
        "</script>"
    )
    tpl = TEMPLATE.read_text(encoding="utf-8")
    a, b = script_blocks(tpl)
    if "__SEED_POSTS_JSON__" not in tpl[a:b]:
        die("template's first <script> is not the config block")
    html = tpl[:a] + block + tpl[b:]
    title = str(cfg.get("title") or "Content Performance").replace("&", "&amp;").replace("<", "&lt;")
    html = html.replace("<title>Content Performance</title>", f"<title>{title}</title>", 1)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(html, encoding="utf-8")

    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write("\n".join(scripts))
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    if r.returncode != 0:
        die("node --check failed (check quotes in the insights):\n" + r.stderr[-1200:])
    n = {p: sum(1 for x in posts if x["platform"] == p) for p in ("instagram", "tiktok")}
    print(f"OK  {out_path}  ({len(html)//1024} KB)  Instagram {n['instagram']}, TikTok {n['tiktok']} posts, "
          f"{cfg['windowDays']}-day window, pulled {cfg['pulledAt']}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "reuse":
        reuse(a[1], a[2])
    elif len(a) == 3 and a[0] == "analyze":
        analyze(a[1], a[2])
    elif len(a) == 4 and a[0] == "build":
        build(a[1], a[2], a[3])
    else:
        sys.exit(__doc__)
