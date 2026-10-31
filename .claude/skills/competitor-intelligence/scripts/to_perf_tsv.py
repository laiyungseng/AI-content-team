#!/usr/bin/env python3
"""items.tsv (ours only) -> config.json + posts.tsv for perf_build.py (Instagram and TikTok).

    to_perf_tsv.py <run_dir> <out_dir>
    then: perf_build.py analyze <out_dir>/config.json <out_dir>/posts.tsv
          perf_build.py build   <out_dir>/config.json <out_dir>/posts.tsv <out_dir>/performance.html

Uses the first Ours account per platform. The dashboard supports at most 5 topics plus `uncategorized`.
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


def main() -> None:
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    state = src.parse((run.parents[1] / "sources.md").read_text(encoding="utf-8"))
    rows = [r for r in nz.read_items(run) if r["owner"] == "ours" and r["platform"] in ("instagram", "tiktok") and r["status"] == "ok"]
    if not rows:
        sys.exit("No Ours items on Instagram or TikTok in this run")
    handles = {}
    for p in ("instagram", "tiktok"):
        first = next((x for x in state["ours"][p] if x["active"]), None)
        if first:
            handles[p] = next(iter(nz.handle_of(p, first["url"])), nz.slug(first["name"]))
    missing = [p for p in ("instagram", "tiktok") if p not in handles]
    if missing:
        sys.exit(f"perf dashboard needs an active Ours account on both Instagram and TikTok (missing: {', '.join(missing)}). "
                 "Skip the dashboard; use `normalise.py stats` for the Ours baseline.")
    first_acc = {}
    for r in rows:
        first_acc.setdefault(r["platform"], r["accountId"])
    rows = [r for r in rows if r["accountId"] == first_acc[r["platform"]]]
    days = int(re.sub(r"\D", "", next(p for p in state["platforms"] if p["key"] == rows[0]["platform"])["range"]) or 30)
    window = min((7, 30, 90), key=lambda d: abs(d - days))
    topics = {t["key"]: {"label": t["label"], "description": t["label"]} for t in state["topics"][:5]}
    cfg = {"title": f"{run.parents[1].name} content performance", "pulledAt": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "windowDays": window, "handles": handles, "topics": topics, "insights": {}}
    (out / "config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = []
    for r in rows:
        topic = r["topic"] if r["topic"] in topics else "uncategorized"
        cap = re.sub(r"[\t\r]+", " ", r["caption"]).replace("\n", "\\n")[:120]
        lines.append("\t".join([r["platform"], r["itemId"], r["date"], r["views"], r["likes"], r["comments"], r["shares"], r["saves"],
                                r["durationSec"], topic, cap]))
    (out / "posts.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} posts, window {window}d -> {out}")


if __name__ == "__main__":
    main()
