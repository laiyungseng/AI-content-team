#!/usr/bin/env python3
"""items.tsv -> config.json + posts.tsv for radar_build.py (Instagram and TikTok accounts only, ours and competitors).

    to_radar_tsv.py <run_dir> <out_dir>
    then: radar_build.py <out_dir>/config.json <out_dir>/posts.tsv <out_dir>/radar.html

Items with no topic go to `uncategorized`. Followers are read from raw/instagram/followers.json when present.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "source-manager" / "scripts"))
import normalise as nz  # noqa: E402
import sources as src  # noqa: E402

DISPLAY = {"instagram": "Instagram", "tiktok": "TikTok"}


def main() -> None:
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    state = src.parse((run.parents[1] / "sources.md").read_text(encoding="utf-8"))
    rows = [r for r in nz.read_items(run) if r["platform"] in DISPLAY]
    followers = {}
    ff = run / "raw/instagram/followers.json"
    if ff.exists():
        followers = {str(x.get("username", "")).lower(): x.get("followersCount") for x in json.loads(ff.read_text(encoding="utf-8"))}
    topics = {t["key"]: t["label"] for t in state["topics"]}
    if any(not r["topic"] for r in rows if r["status"] == "ok"):
        topics.setdefault("uncategorized", "Uncategorized")
    accounts, seen = [], set()
    for r in rows:
        k = (r["platform"], r["accountId"])
        if k in seen:
            continue
        seen.add(k)
        section = state["ours" if r["owner"] == "ours" else "competitors"][r["platform"]]
        row = next((x for x in section if nz.slug(x["name"]) == r["accountId"]), {"name": r["accountId"], "url": ""})
        handle = next(iter(nz.handle_of(r["platform"], row["url"])), r["accountId"])
        accounts.append({"id": f"{r['accountId']}_{r['platform']}", "displayName": row["name"], "handle": handle,
                         "platform": DISPLAY[r["platform"]], "isMine": r["owner"] == "ours",
                         "status": r["status"], "followers": followers.get(handle.lower()),
                         **({"errorNote": r["caption"]} if r["status"] != "ok" else {})})
    cfg = {"title": f"{run.parents[1].name} competitor radar", "pulledAt": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "topics": topics, "accounts": accounts}
    (out / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = []
    for r in rows:
        if r["status"] != "ok":
            continue
        cap = re.sub(r"[\t\r\n]+", " ", r["caption"])[:150]
        lines.append("\t".join([f"{r['accountId']}_{r['platform']}", r["itemId"], r["date"], r["views"], r["likes"], r["comments"], r["shares"], r["saves"],
                                r["durationSec"], r["topic"] or "uncategorized", cap]))
    (out / "posts.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(accounts)} accounts, {len(lines)} posts -> {out}")


if __name__ == "__main__":
    main()
