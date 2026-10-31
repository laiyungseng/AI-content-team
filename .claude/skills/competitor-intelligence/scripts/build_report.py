#!/usr/bin/env python3
"""Select report items and build the report page.

    build_report.py select <run_dir> [--max-per-account 8] [--max-total 120]   -> analysis/selected.json
    build_report.py build  <run_dir>                                          -> report.html (page fragment)

`select` ranks competitor items by ratio to the account's own typical views (see references/selection.md).
`build` needs analysis/verdicts.json (one verdict per selected id) and analysis/comparison.json; analysis/ours.json is optional.
It refuses to build on a missing verdict, an invalid value, or a missing comparison dimension, and warns on banned jargon.
Images are referenced as media/<id>.jpg when the file exists; publish report.html with the media files (Artifact `files`).
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import normalise as nz  # noqa: E402

TEMPLATE = HERE.parent / "assets" / "report_template.html"
DIMENSIONS = ["hook", "format", "visual", "message", "offer", "CTA", "cadence", "engagement"]
VERDICTS = ("adapt", "copy", "ignore")
BANNED = ["p-value", "permutation", "bootstrap", "confidence interval", "confidence band", "significant", "statistically", "benjamini",
          "false-discovery", "pearson", "correlation", "variance", "standard deviation", "percentile", "resampling", "sample size",
          "outlier score", "median"]


def safe_id(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", s)


def ratios(rows):
    """itemId -> ratio to the account's own typical views (None when no views)."""
    by_acc = {}
    for r in rows:
        if r["status"] == "ok" and r["views"]:
            by_acc.setdefault((r["platform"], r["accountId"]), []).append(int(r["views"]))
    typical = {k: statistics.median(v) for k, v in by_acc.items()}
    out = {}
    for r in rows:
        t = typical.get((r["platform"], r["accountId"]))
        out[r["itemId"]] = round(int(r["views"]) / t, 2) if (r["views"] and t) else None
    return out, {k: int(v) for k, v in typical.items()}, {k: len(v) for k, v in by_acc.items()}


def select(run: Path, per_acc: int, total: int) -> None:
    rows = [r for r in nz.read_items(run) if r["owner"] == "competitor" and r["status"] == "ok"]
    ratio, _, scored = ratios(rows)
    ids, trimmed = [], []
    accounts = {}
    for r in rows:
        accounts.setdefault((r["platform"], r["accountId"]), []).append(r)
    for (plat, acc), items in accounts.items():
        have = [i for i in items if ratio[i["itemId"]] is not None]
        if have:
            have.sort(key=lambda i: ratio[i["itemId"]], reverse=True)
            pick = have[:6] + have[-2:] + [i for i in have if ratio[i["itemId"]] >= 10]
        else:  # ads, photo-only accounts, XHS without views: recency, then engagement
            items.sort(key=lambda i: (i["date"], int(i["likes"] or 0) + int(i["comments"] or 0)), reverse=True)
            pick = items
        seen, chosen = set(), []
        for i in pick:
            if i["itemId"] not in seen:
                seen.add(i["itemId"])
                chosen.append(i)
        if len(chosen) > per_acc:
            trimmed.append(f"{plat}/{acc}")
            chosen = chosen[:per_acc]
        ids += [i["itemId"] for i in chosen]
    if len(ids) > total:
        trimmed.append("overall cap")
        ids = ids[:total]
    out = run / "analysis" / "selected.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"ids": ids, "trimmed": sorted(set(trimmed)), "ratios": {i: ratio[i] for i in ids}}, indent=1), encoding="utf-8")
    print(f"selected {len(ids)} of {len(rows)} competitor items" + (f"; trimmed: {', '.join(sorted(set(trimmed)))}" if trimmed else ""))


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def die(msg):
    sys.exit(f"BUILD FAILED: {msg}")


def build(run: Path) -> None:
    an = run / "analysis"
    for f in ("selected.json", "verdicts.json", "comparison.json"):
        if not (an / f).exists():
            die(f"analysis/{f} missing")
    sel = json.loads((an / "selected.json").read_text(encoding="utf-8"))
    verdicts = {v["id"]: v for v in json.loads((an / "verdicts.json").read_text(encoding="utf-8"))["items"]}
    comp = json.loads((an / "comparison.json").read_text(encoding="utf-8"))
    ours = json.loads((an / "ours.json").read_text(encoding="utf-8")) if (an / "ours.json").exists() else None
    for k in ("headline", "rows", "strategy", "positioning", "postCounts"):
        if k not in comp:
            die(f"comparison.json missing '{k}'")
    have = {r["dimension"] for r in comp["rows"]}
    if missing := [d for d in DIMENSIONS if d not in have]:
        die(f"comparison.json rows missing dimensions: {missing}")
    for r in comp["rows"]:
        if r.get("stronger") not in ("ours", "theirs", "similar", "unclear"):
            die(f"row '{r['dimension']}': stronger must be ours|theirs|similar|unclear")
    rows = nz.read_items(run)
    byid = {r["itemId"]: r for r in rows if r["itemId"]}
    ratio, _, scored = ratios([r for r in rows if r["owner"] == "competitor"])
    cards = []
    for i in sel["ids"]:
        v = verdicts.get(i)
        if not v:
            die(f"no verdict for selected item {i}")
        if v["verdict"] not in VERDICTS:
            die(f"item {i}: verdict must be one of {VERDICTS}")
        for k in ("reason",):
            if not v.get(k):
                die(f"item {i}: missing {k}")
        r = byid[i]
        img = f"media/{safe_id(i)}.jpg"
        cards.append({
            "id": i, "did": safe_id(i), "verdict": v["verdict"], "account": r["accountId"], "platform": r["platform"], "type": r["itemType"],
            "date": r["date"], "views": r["views"], "likes": r["likes"], "comments": r["comments"], "shares": r["shares"], "saves": r["saves"],
            "ratio": ratio.get(i), "caption": r["caption"][:200], "permalink": r["permalink"],
            "image": img if (run / img).exists() else "", "reason": v["reason"], "hook": v.get("hook", ""),
            "why": v.get("whyItWorks", ""), "how": v.get("howToUse", ""), "confidence": v.get("confidence", "low"),
            "anomaly": bool(ratio.get(i) and ratio[i] >= 10),
        })
    unread = [{"account": r["accountId"], "platform": r["platform"], "owner": r["owner"], "status": r["status"], "note": r["caption"]}
              for r in rows if r["status"] != "ok"]
    meta = {"project": run.parents[1].name, "run": run.name, "trimmed": sel.get("trimmed", []),
            "counts": {"competitor": sum(1 for r in rows if r["owner"] == "competitor" and r["status"] == "ok"),
                       "ours": sum(1 for r in rows if r["owner"] == "ours" and r["status"] == "ok")}}
    data = {"meta": meta, "cards": cards, "comparison": comp, "ours": ours, "unread": unread}
    bad = sorted({b for s in strings({"c": comp, "v": [c["reason"] + c["why"] + c["how"] for c in cards]}) for b in BANNED if b in s.lower()})
    if bad:
        print(f"WARNING plain-language rule: found {bad}; rewrite per writing_guide.md")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__REPORT_JSON__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    (run / "report.html").write_text(html, encoding="utf-8")
    n_img = sum(1 for c in cards if c["image"])
    print(f"report.html: {len(cards)} cards ({n_img} with images), {len(unread)} unreadable accounts")


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, run = sys.argv[1], Path(sys.argv[2])
    args = sys.argv[3:]
    def opt(name, default):
        return int(args[args.index(name) + 1]) if name in args else default
    if cmd == "select":
        select(run, opt("--max-per-account", 8), opt("--max-total", 120))
    elif cmd == "build":
        build(run)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
