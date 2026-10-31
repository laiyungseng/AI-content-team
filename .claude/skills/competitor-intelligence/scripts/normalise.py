#!/usr/bin/env python3
"""Turn raw actor output into the unified items.tsv, and apply topic tags.

    normalise.py build <run_dir>                 raw/<platform>/items.json + sources.md -> items.tsv
    normalise.py tag   <run_dir> <tags.tsv>      tags.tsv = itemId<TAB>topic<TAB>pillar<TAB>sponsored (last two optional)
    normalise.py stats <run_dir>                 per-account counts and typical views (JSON)

Null rule: empty = missing, never 0. Non-ok accounts are kept as a row with an empty itemId and the reason in `caption`.
Field spellings that differ between actors are listed per field in MAP; the first path that exists wins.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "source-manager" / "scripts"))
import sources as src  # noqa: E402

COLUMNS = ["owner", "accountId", "platform", "itemType", "itemId", "date", "views", "likes", "comments", "shares", "saves",
           "durationSec", "topic", "pillar", "caption", "mediaUrl", "permalink", "status", "runningDays", "isActive", "variants", "sponsored"]

# field -> candidate dotted paths (".0" indexes a list)
MAP = {
    "instagram": {
        "owner": ["ownerUsername"], "id": ["shortCode"], "date": ["timestamp"], "views": ["videoPlayCount"],
        "likes": ["likesCount"], "comments": ["commentsCount"], "shares": [], "saves": [],
        "duration": ["videoDuration"], "caption": ["caption"], "media": ["displayUrl", "images.0"], "link": ["url"],
    },
    "tiktok": {
        "owner": ["authorMeta.name"], "id": ["id"], "date": ["createTimeISO", "createTime"], "views": ["playCount"],
        "likes": ["diggCount"], "comments": ["commentCount"], "shares": ["shareCount"], "saves": ["collectCount"],
        "duration": ["videoMeta.duration"], "caption": ["text"], "media": ["videoMeta.coverUrl", "covers.0"], "link": ["webVideoUrl"],
    },
    "meta": {
        "owner": ["pageName", "page_name", "snapshot.page_name", "snapshot.pageName"],
        "owner_id": ["pageId", "page_id", "snapshot.page_id"],
        "id": ["adArchiveID", "adArchiveId", "ad_archive_id", "adId", "id"],
        "date": ["startDateFormatted", "startDate", "start_date", "startDateString"],
        "end": ["endDateFormatted", "endDate", "end_date"],
        "active": ["isActive", "is_active"],
        "views": [], "likes": [], "comments": [], "shares": [], "saves": [], "duration": [],
        "caption": ["snapshot.body.text", "snapshot.caption", "body.text", "adText", "text"],
        "media": ["snapshot.images.0.original_image_url", "snapshot.images.0.resized_image_url", "snapshot.videos.0.video_preview_image_url",
                  "snapshot.cards.0.original_image_url", "snapshot.cards.0.video_preview_image_url", "imageUrl"],
        "link": ["adLibraryUrl", "url", "ad_library_url"],
    },
    "xhs": {
        "owner": ["user.nickname", "author.nickname", "nickname", "userName", "user.name", "author.name"],
        "owner_id": ["user.userId", "author.userId", "userId", "user_id", "user.user_id"],
        "id": ["noteId", "note_id", "id"],
        "date": ["create_time", "time", "publishTime", "publish_time", "lastUpdateTime", "createTime", "timestamp"],
        "views": ["viewCount", "view_count", "interactInfo.viewCount"],
        "likes": ["likedCount", "likes", "likeCount", "interactInfo.likedCount"],
        "comments": ["comments_count", "commentCount", "comments", "commentsCount", "interactInfo.commentCount"],
        "shares": ["share_count", "sharedCount", "shareCount", "shares", "interactInfo.shareCount"],
        "saves": ["collected_count", "collectedCount", "collectCount", "collects", "interactInfo.collectedCount"],
        "duration": ["video_info_v2.capa.duration", "video.duration", "duration"],
        "caption": ["title", "desc", "displayTitle", "description"],
        "media": ["images_list.0.url", "cover", "cover.url", "coverUrl", "imageList.0.url", "images.0", "imageList.0.urlDefault"],
        "link": ["url", "noteUrl", "note_url"],
    },
}
ITEM_TYPE = {"instagram": "post", "tiktok": "post", "xhs": "post", "meta": "ad"}


def pick(obj, paths):
    for p in paths:
        cur = obj
        for part in p.split("."):
            if isinstance(cur, list):
                if not (part.isdigit() and int(part) < len(cur)):
                    cur = None
                    break
                cur = cur[int(part)]
            elif isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                cur = None
                break
        if cur not in (None, "", [], {}):
            return cur
    return None


def to_int(v):
    if v is None or isinstance(v, bool):
        return ""
    if isinstance(v, (int, float)):
        return str(int(v)) if v >= 0 else ""  # Instagram returns -1 when likes are hidden: missing, never a count
    s = str(v).strip().lower().replace(",", "")
    m = re.fullmatch(r"([\d.]+)\s*([kw万m]?)", s)
    if not m:
        return ""
    n = float(m.group(1)) * {"": 1, "k": 1e3, "w": 1e4, "万": 1e4, "m": 1e6}[m.group(2)]
    return str(int(n))


def to_date(v):
    if v is None:
        return ""
    if isinstance(v, (int, float)) or (isinstance(v, str) and v.strip().isdigit()):
        n = float(v)
        n = n / 1000 if n > 1e11 else n
        return dt.datetime.fromtimestamp(n, dt.timezone.utc).strftime("%Y-%m-%d")
    s = str(v).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    return m.group(0) if m else ""


def clean(s, n=300):
    return re.sub(r"\s+", " ", str(s or "")).strip()[:n]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_") or "account"


def handle_of(platform, url):
    """Identifiers a target may be matched by (lowercase)."""
    ids = set()
    u = url.strip()
    if platform == "instagram":
        m = re.search(r"instagram\.com/([^/?#]+)", u)
    elif platform == "tiktok":
        m = re.search(r"tiktok\.com/@([^/?#]+)", u)
    elif platform == "xhs":
        m = re.search(r"/profile/([^/?#]+)", u)
    else:
        m = re.search(r"view_all_page_id=(\d+)", u) or re.search(r"facebook\.com/(?!ads/)([^/?#]+)", u)
    if m:
        ids.add(m.group(1).lower())
    return ids


def expand_xhs(items: list[dict]) -> list[dict]:
    """zen-studio/rednote-user-profile-scraper returns one row per profile with notes[]; flatten to one row per note.
    Rows that already look like single notes pass through unchanged."""
    out = []
    for it in items:
        if not isinstance(it, dict) or "notes" not in it:
            out.append(it)
            continue
        prof = it.get("profile") or {}
        owner = {"nickname": prof.get("nickname", ""), "userId": prof.get("userid") or it.get("_user_id", "")}
        for n in it.get("notes") or []:
            n = dict(n)
            n["user"] = owner
            n["url"] = f"https://www.xiaohongshu.com/explore/{n.get('id')}" if n.get("id") else ""
            if not n.get("view_count"):  # actor reports 0 views for every note: missing, never 0
                n.pop("view_count", None)
            out.append(n)
    return out


def run_ctx(run_dir: Path):
    project = run_dir.parents[1]
    return project, project / "sources.md"


def build(run_dir: Path) -> None:
    project, sfile = run_ctx(run_dir)
    state = src.parse(sfile.read_text(encoding="utf-8"))
    pcfg = {p["key"]: p for p in state["platforms"]}
    run_date = dt.datetime.strptime(run_dir.name[:10], "%Y-%m-%d").date()
    rows, warnings = [], []
    for platform, m in MAP.items():
        pdir = run_dir / "raw" / platform
        targets = [(o, r) for o, sec in (("competitor", "competitors"), ("ours", "ours")) for r in state[sec][platform]
                   if r["active"] and r["url"]]
        if not pcfg[platform]["enabled"] or not targets:
            continue
        itemsf = pdir / "items.json"
        items = json.loads(itemsf.read_text(encoding="utf-8")) if itemsf.exists() else []
        if platform == "xhs":
            items = expand_xhs(items)
        if not itemsf.exists():
            warnings.append(f"{platform}: raw/{platform}/items.json missing; all accounts marked failed")
        statusf = pdir / "status.json"
        status = {k.lower(): v for k, v in json.loads(statusf.read_text(encoding="utf-8")).items()} if statusf.exists() else {}
        days = int(re.sub(r"\D", "", pcfg[platform]["range"]) or 90)
        cutoff = run_date - dt.timedelta(days=days)
        cap = pcfg[platform]["maxPosts"]
        by_target = {i: [] for i in range(len(targets))}
        for it in items:
            keys = {str(pick(it, m["owner"]) or "").lower(), str(pick(it, m.get("owner_id", [])) or "").lower()} - {""}
            if platform == "meta":  # Facebook page vanity or numeric id from the ad's page link; page names drift (dashes, case)
                keys |= handle_of("meta", str(pick(it, ["snapshot.pageProfileUri"]) or ""))
            hit = next((i for i, (_, r) in enumerate(targets)
                        if keys & (handle_of(platform, r["url"]) | {slug(r["name"]), r["name"].lower()})), None)
            if hit is None and len(targets) == 1:
                hit = 0
            if hit is None:
                warnings.append(f"{platform}: item {pick(it, m['id'])} from '{pick(it, m['owner'])}' matches no active target; skipped")
                continue
            by_target[hit].append(it)
        for i, (owner, r) in enumerate(targets):
            acc = slug(r["name"])
            if len(acc) < 4 or acc == "account":  # Chinese names slug to "account" or "kl": fall back to the profile id so accounts stay distinct
                acc = next(iter(sorted(handle_of(platform, r["url"]))), acc)[:12]
            hs = handle_of(platform, r["url"]) | {acc, r["name"].lower()}
            st = next((status[h] for h in hs if h in status), None)
            out = []
            for it in by_target[i]:
                d = to_date(pick(it, m["date"]))
                if not d:
                    continue
                if platform == "meta":  # a long-running ad that started before the window is the most valuable one
                    end = to_date(pick(it, m["end"]))
                    if end and dt.date.fromisoformat(end) < cutoff:
                        continue
                elif dt.date.fromisoformat(d) < cutoff:
                    continue
                itype = ITEM_TYPE[platform]
                run_days, is_active = "", ""
                if platform == "meta":  # ads have no metrics: how long one has run and whether it is live is the signal
                    end = to_date(pick(it, m["end"]))
                    stop = min(dt.date.fromisoformat(end), run_date) if end else run_date
                    run_days = str(max((stop - dt.date.fromisoformat(d)).days, 0))
                    flag = pick(it, m["active"])
                    is_active = "yes" if flag is True else "no" if flag is False else ""
                views = "" if (platform == "instagram" and str(it.get("type", "")).lower() in ("image", "sidecar")
                               and not it.get("videoPlayCount")) else to_int(pick(it, m["views"]))
                out.append({
                    "owner": owner, "accountId": acc, "platform": platform, "itemType": itype, "itemId": str(pick(it, m["id"]) or ""),
                    "date": d, "views": views, "likes": to_int(pick(it, m["likes"])), "comments": to_int(pick(it, m["comments"])),
                    "shares": to_int(pick(it, m["shares"])), "saves": to_int(pick(it, m["saves"])),
                    "durationSec": (to_int(pick(it, m["duration"])) if to_int(pick(it, m["duration"])) != "0" else ""),  # actors return 0 for photo posts: missing, never 0
                    "topic": "", "pillar": "", "runningDays": run_days, "isActive": is_active, "variants": "", "sponsored": "",
                    "caption": clean(pick(it, m["caption"])), "mediaUrl": str(pick(it, m["media"]) or ""),
                    "permalink": str(pick(it, m["link"]) or ""), "status": "ok",
                })
            out = [o for o in out if o["itemId"]]
            out.sort(key=lambda o: o["date"], reverse=True)
            out = out[:cap]
            if out:
                rows += out
            else:
                reason = st or ("failed" if not items and not itemsf.exists() else "empty")
                note = {"private": "account is private", "failed": "actor error or account not found",
                        "empty": "no posts in the window"}.get(reason, reason)
                rows.append({c: "" for c in COLUMNS} | {"owner": owner, "accountId": acc, "platform": platform,
                             "itemType": ITEM_TYPE[platform], "caption": note, "status": reason if reason in ("private", "failed", "empty") else "failed",
                             "permalink": r["url"]})
    same = {}
    for r in rows:  # ads from one page with identical text: variants counts them all (a re-run under a new ad id counts too)
        if r["platform"] == "meta" and r["status"] == "ok":
            same[(r["accountId"], r["caption"])] = same.get((r["accountId"], r["caption"]), 0) + 1
    for r in rows:
        if r["platform"] == "meta" and r["status"] == "ok":
            r["variants"] = str(same[(r["accountId"], r["caption"])])
    with (run_dir / "items.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writeheader()
        w.writerows(rows)
    ok = sum(1 for r in rows if r["status"] == "ok")
    print(f"items.tsv: {ok} items, {len(rows) - ok} non-ok account rows")
    for w_ in warnings:
        print("WARNING", w_)


def read_items(run_dir: Path) -> list[dict]:
    with (run_dir / "items.tsv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"))


def write_items(run_dir: Path, rows: list[dict]) -> None:
    with (run_dir / "items.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        w.writeheader()
        w.writerows(rows)


def tag(run_dir: Path, tags: Path) -> None:
    allowed = {t["key"] for t in src.parse((run_ctx(run_dir)[1]).read_text(encoding="utf-8"))["topics"]}
    mp = {}
    for line in tags.read_text(encoding="utf-8").splitlines():
        p = line.split("\t")
        if len(p) >= 2 and p[0] and p[0] != "itemId":
            if allowed and p[1] not in allowed:
                sys.exit(f"topic '{p[1]}' for {p[0]} is not in sources.md Topics {sorted(allowed)}")
            sp = p[3].strip().lower() if len(p) > 3 else ""
            if sp not in ("", "yes"):
                sys.exit(f"sponsored for {p[0]} must be yes or empty, got '{sp}'")
            mp[p[0]] = (p[1], p[2] if len(p) > 2 else "", sp)
    rows = read_items(run_dir)
    n = 0
    for r in rows:
        if r["itemId"] in mp:
            r["topic"], r["pillar"], r["sponsored"] = mp[r["itemId"]]
            n += 1
    write_items(run_dir, rows)
    print(f"tagged {n} of {len(mp)} ids")


def stats(run_dir: Path) -> dict:
    out = {}
    for r in read_items(run_dir):
        a = out.setdefault(f"{r['platform']}/{r['accountId']}", {"owner": r["owner"], "status": r["status"], "items": 0, "withViews": 0, "_v": []})
        if r["status"] == "ok":
            a["items"] += 1
            if r["views"]:
                a["withViews"] += 1
                a["_v"].append(int(r["views"]))
    for a in out.values():
        v = a.pop("_v")
        a["typicalViews"] = int(statistics.median(v)) if v else None
    return out


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, run = sys.argv[1], Path(sys.argv[2])
    if cmd == "build":
        build(run)
    elif cmd == "tag":
        tag(run, Path(sys.argv[3]))
    elif cmd == "stats":
        print(json.dumps(stats(run), indent=2))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
