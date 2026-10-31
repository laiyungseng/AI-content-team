#!/usr/bin/env python3
"""Prepare and check collection. Apify itself is called by Claude through the authorised MCP connector.

    collect.py plan  <run_dir> [--test]    write raw/<platform>/input.json for every enabled platform (--test: limit 2)
    collect.py check <run_dir>             verify raw/<platform>/items.json has the mapped fields; non-zero exit if not
    collect.py media <run_dir>             download images for the report's selected items into media/ (or all if none selected)
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "source-manager" / "scripts"))
import sources as src  # noqa: E402
import normalise as nz  # noqa: E402

# Actor ids come from memory of the Apify store: confirm with fetch-actor-details on first use (see platform_scraping.md).
ACTORS = {
    "instagram": "apify/instagram-scraper",
    "tiktok": "clockworks/tiktok-scraper",
    "meta": "apify/facebook-ads-scraper",
    "xhs": "zen-studio/rednote-user-profile-scraper",
}
FIELDS = {
    "instagram": "ownerUsername,shortCode,type,productType,timestamp,videoPlayCount,likesCount,commentsCount,videoDuration,caption,displayUrl,url",
    "tiktok": "authorMeta.name,authorMeta.fans,id,createTimeISO,playCount,diggCount,commentCount,shareCount,collectCount,videoMeta.duration,videoMeta.coverUrl,text,webVideoUrl",
    "meta": "",
    "xhs": "",
}


def plan(run_dir: Path, test: bool) -> None:
    project = run_dir.parents[1]
    targets = src.cmd_targets(project / "sources.md")
    if not targets:
        sys.exit("No Enabled platform with an Active URL in sources.md")
    run_date = dt.datetime.strptime(run_dir.name[:10], "%Y-%m-%d").date()
    for platform in sorted({t["platform"] for t in targets}):
        ts = [t for t in targets if t["platform"] == platform]
        limit = 2 if test else ts[0]["maxPosts"]
        days = int(re.sub(r"\D", "", ts[0]["range"]) or 90)
        since = (run_date - dt.timedelta(days=days)).isoformat()
        urls = [t["url"] for t in ts]
        if platform == "instagram":
            inp = {"directUrls": urls, "resultsType": "posts", "resultsLimit": limit, "onlyPostsNewerThan": since}
        elif platform == "tiktok":
            inp = {"profiles": [re.sub(r".*@", "", u).strip("/") for u in urls], "resultsPerPage": limit, "oldestPostDateUnified": since}
        elif platform == "meta":
            inp = {"startUrls": [{"url": u} for u in urls], "resultsLimit": limit}  # activeStatus omitted = active and inactive (the enum rejects "all" and "")
        else:
            inp = {"profileUrls": urls, "includeNotes": True, "maxNotesPerProfile": limit}
        d = run_dir / "raw" / platform
        d.mkdir(parents=True, exist_ok=True)
        (d / "input.json").write_text(json.dumps({"actor": ACTORS[platform], "fields": FIELDS[platform], "input": inp}, indent=2), encoding="utf-8")
        note = "  (actor id not chosen yet: use search-actors)" if ACTORS[platform].startswith("TODO") else ""
        print(f"{platform}: {len(ts)} targets, limit {limit}, actor {ACTORS[platform]}{note}")


def check(run_dir: Path) -> int:
    bad = 0
    for platform, m in nz.MAP.items():
        f = run_dir / "raw" / platform / "items.json"
        if not f.exists():
            continue
        items = json.loads(f.read_text(encoding="utf-8"))
        if platform == "xhs":
            items = nz.expand_xhs(items)
        if not items:
            print(f"{platform}: items.json is empty")
            continue
        for field in ("owner", "id", "date", "likes", "caption"):
            if not m.get(field):
                continue
            hits = sum(1 for it in items if nz.pick(it, m[field]) is not None)
            if hits == 0:
                bad += 1
                print(f"{platform}: field '{field}' missing on every item (tried {m[field]}); schema changed? stop and inspect one item")
        print(f"{platform}: {len(items)} items checked")
    return 1 if bad else 0


def media(run_dir: Path) -> None:
    sel = run_dir / "analysis" / "selected.json"
    ids = set(json.loads(sel.read_text(encoding="utf-8"))["ids"]) if sel.exists() else None
    out = run_dir / "media"
    out.mkdir(exist_ok=True)
    ok = fail = 0
    for r in nz.read_items(run_dir):
        if r["status"] != "ok" or not r["mediaUrl"] or (ids is not None and r["itemId"] not in ids):
            continue
        name = re.sub(r"[^A-Za-z0-9_-]", "_", r["itemId"]) + ".jpg"
        dest = out / name
        if dest.exists():
            continue
        try:
            req = urllib.request.Request(r["mediaUrl"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 500 or len(data) > 5_000_000:
                raise ValueError(f"unexpected size {len(data)}")
            dest.write_bytes(data)
            ok += 1
        except Exception as e:  # expired link, hotlink block, timeout: the card shows without an image
            fail += 1
            print(f"media failed {r['itemId']}: {e}")
    print(f"media: {ok} saved, {fail} failed")


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, run = sys.argv[1], Path(sys.argv[2])
    if cmd == "plan":
        plan(run, "--test" in sys.argv)
    elif cmd == "check":
        sys.exit(check(run))
    elif cmd == "media":
        media(run)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
