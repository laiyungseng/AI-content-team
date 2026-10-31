#!/usr/bin/env python3
"""Assemble the Competitor Content Radar from config.json + posts.tsv.

Usage:
  python3 build.py --reuse OLD_INDEX.html --out-config config.json
      Pull accounts, topics and title out of an already-published radar
      (refresh runs), so they do not need to be re-asked or re-typed.

  python3 build.py config.json posts.tsv OUT.html
      Validate, expand to the template's JSON schema, inject, syntax-check.

posts.tsv: one post per line, tab-separated, no header, 11 columns:
  accountId  postId  date  views  likes  comments  shares  saves  durationSec  topic  caption
  - empty cell = null (photo/carousel posts have empty views and durationSec)
  - postId: Instagram shortCode, or TikTok numeric video id
  - date: YYYY-MM-DD (UTC)
  - caption: first 150 characters only, tabs and newlines replaced by spaces
"""
import json, re, subprocess, sys, tempfile
from collections import Counter, defaultdict
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "radar_template.html"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MIN_POSTS = 4  # below this per account+topic, a topic cannot be judged


def die(msg):
    sys.exit("BUILD FAILED: " + msg)


def reuse(old_html, out_cfg):
    s = Path(old_html).read_text(encoding="utf-8")
    m = re.search(r"const RAW_DATA = (\{.*?\});\n", s, re.S)
    if not m:
        die("no RAW_DATA found in " + old_html)
    d = json.loads(m.group(1))
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    cfg = {"title": t.group(1).strip() if t else "Competitor Content Radar",
           "pulledAt": "SET_ME", "topics": d["topics"],
           "accounts": [{k: v for k, v in a.items() if k != "pulledAt"} for a in d["accounts"]]}
    Path(out_cfg).write_text(json.dumps(cfg, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_cfg}: {len(cfg['accounts'])} accounts, {len(cfg['topics'])} topics. "
          "Update pulledAt, followers and status, then write posts.tsv.")


def num(cell, where, integer=True):
    cell = cell.strip()
    if cell == "" or cell.lower() in ("null", "none", "-"):
        return None
    try:
        v = float(cell.replace(",", ""))
    except ValueError:
        die(f"{where}: '{cell}' is not a number")
    if v < 0:
        die(f"{where}: negative value {v}")
    return int(round(v)) if integer else round(v, 2)


def build(cfg_path, tsv_path, out_path):
    cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
    for k in ("title", "pulledAt", "accounts", "topics"):
        if k not in cfg:
            die(f"config.json is missing '{k}'")
    if not re.match(r"^\d{4}-\d{2}-\d{2}T", str(cfg["pulledAt"])):
        die("pulledAt must be ISO 8601, e.g. 2026-10-01T09:00:00Z")
    accts = {}
    for a in cfg["accounts"]:
        for k in ("id", "displayName", "handle", "platform", "status"):
            if k not in a:
                die(f"account {a} is missing '{k}'")
        if a["platform"] not in ("Instagram", "TikTok"):
            die(f"{a['id']}: platform must be Instagram or TikTok")
        a.setdefault("isMine", False)
        a.setdefault("followers", None)
        a["pulledAt"] = cfg["pulledAt"]
        a["handle"] = a["handle"].lstrip("@")
        accts[a["id"]] = a

    posts, seen, warnings = [], set(), []
    for ln, raw in enumerate(Path(tsv_path).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        c = raw.split("\t", 10)
        if len(c) < 10:
            die(f"posts.tsv line {ln}: expected 11 tab-separated columns, got {len(c)}")
        c += [""] * (11 - len(c))
        aid, pid, date = c[0].strip(), c[1].strip(), c[2].strip()
        w = f"posts.tsv line {ln}"
        if aid not in accts:
            die(f"{w}: accountId '{aid}' is not in config.json")
        a = accts[aid]
        if a["status"] != "ok":
            die(f"{w}: account '{aid}' has status '{a['status']}' but has posts")
        if not DATE_RE.match(date):
            die(f"{w}: date '{date}' must be YYYY-MM-DD")
        topic = c[9].strip()
        if topic not in cfg["topics"]:
            die(f"{w}: topic '{topic}' is not a key in config.json topics")
        if (aid, pid) in seen:
            warnings.append(f"duplicate post {aid}/{pid} dropped")
            continue
        seen.add((aid, pid))
        shares, saves = num(c[6], w), num(c[7], w)
        if a["platform"] == "Instagram":
            shares = saves = None  # Instagram never returns these
        url = (f"https://www.instagram.com/p/{pid}/" if a["platform"] == "Instagram"
               else f"https://www.tiktok.com/@{a['handle']}/video/{pid}")
        posts.append({"id": pid, "accountId": aid, "platform": a["platform"], "date": date,
                      "views": num(c[3], w), "likes": num(c[4], w) or 0,
                      "comments": num(c[5], w) or 0, "shares": shares, "saves": saves,
                      "durationSec": num(c[8], w, integer=False),
                      "caption": re.sub(r"\s+", " ", c[10]).strip()[:150],
                      "topic": topic, "url": url})

    per_acct = Counter(p["accountId"] for p in posts)
    for aid, a in accts.items():
        if a["status"] == "ok" and per_acct[aid] == 0:
            die(f"account '{aid}' is status ok but has no posts; set status 'empty' with an errorNote")
        if a["status"] != "ok" and not a.get("errorNote"):
            die(f"account '{aid}' is status '{a['status']}' but has no errorNote")

    data = {"accounts": list(accts.values()), "posts": posts,
            "topics": cfg["topics"], "pulledAt": cfg["pulledAt"]}
    # "<\/" keeps a caption containing "</script>" from ending the page script
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

    tpl = TEMPLATE.read_text(encoding="utf-8")
    for ph in ("__DATA_JSON__", '"__PULLED_AT__"', "<title>Competitor Content Radar</title>"):
        if tpl.count(ph) != 1:
            die(f"template placeholder {ph} found {tpl.count(ph)} times, expected 1")
    title = cfg["title"].replace("&", "&amp;").replace("<", "&lt;")
    html = (tpl.replace("__DATA_JSON__", blob, 1)
               .replace('"__PULLED_AT__"', json.dumps(cfg["pulledAt"]), 1)
               .replace("<title>Competitor Content Radar</title>", f"<title>{title}</title>", 1))
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(html, encoding="utf-8")

    # syntax check of the page script
    script = html[html.index("<script>") + 8: html.rindex("</script>")]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(script)
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    if r.returncode != 0:
        die("node --check failed:\n" + r.stderr[-1500:])

    # summary for the hand-over message
    print(f"OK  {out_path}  ({len(html)//1024} KB)  title: {cfg['title']}")
    for w_ in warnings:
        print("WARN", w_)
    grid = defaultdict(Counter)
    for p in posts:
        if p["views"] is not None:
            grid[p["accountId"]][p["topic"]] += 1
    print(f"\nVideo posts per account x topic (cells under {MIN_POSTS} cannot be judged):")
    for aid, a in accts.items():
        if a["status"] != "ok":
            print(f"  {aid}: {a['status']} ({a.get('errorNote', '')})")
            continue
        cells = ", ".join(f"{k}={grid[aid][k]}" for k in cfg["topics"])
        print(f"  {aid}: {per_acct[aid]} posts, {sum(grid[aid].values())} with views | {cells}")
    thin = [k for k in cfg["topics"] if all(grid[a][k] < MIN_POSTS for a in grid)]
    print("\nTopics too thin to call for every account:", ", ".join(thin) if thin else "none")


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--reuse" and sys.argv[3] == "--out-config":
        reuse(sys.argv[2], sys.argv[4])
    elif len(sys.argv) == 4:
        build(*sys.argv[1:])
    else:
        sys.exit(__doc__)
