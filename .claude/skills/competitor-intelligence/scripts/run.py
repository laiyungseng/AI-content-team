#!/usr/bin/env python3
"""Create and close research runs.

    run.py init    <project> [--root <workspace>]        new runs/<YYYY-MM-DD_HHMM>/ from _run_template, index row
    run.py approve <run_dir> [--url <report url>]        status approved in run.md and index.md (never reverses)
    run.py list    <project> [--root <workspace>]        print runs/index.md

Run folders are dated and never overwritten.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "source-manager" / "scripts"))
import sources as src  # noqa: E402


def set_fm(text: str, **kv) -> str:
    head, rest = text.split("\n---", 1)
    for k, v in kv.items():
        if re.search(rf"^{k}:", head, re.M):
            head = re.sub(rf"^{k}:.*$", f"{k}: {v}", head, flags=re.M)
        else:
            head += f"\n{k}: {v}"
    return head + "\n---" + rest


def init(project: str, root: Path) -> None:
    proj = root / "competitor_analysis" / "projects" / project
    if not (proj / "runs" / "_run_template").exists():
        sys.exit(f"{proj}/runs/_run_template missing; run init_project.py first")
    sfile = proj / "sources.md"
    if not sfile.exists():
        sys.exit("sources.md missing; copy it from _template (see source-manager)")
    rid = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    dest = proj / "runs" / rid
    if dest.exists():
        sys.exit(f"{dest} exists; wait a minute or use another time")
    shutil.copytree(proj / "runs" / "_run_template", dest)
    for g in dest.rglob(".gitkeep"):
        g.unlink()
    targets = src.cmd_targets(sfile)
    plats = sorted({t["platform"] for t in targets})
    ncomp = sum(1 for t in targets if t["owner"] == "competitor")
    text = (dest / "run.md").read_text(encoding="utf-8").replace("YYYY-MM-DD_HHMM", rid)
    text = set_fm(text, project=project, platforms="[" + ", ".join(plats) + "]",
                  counts=f"{{competitor_items: 0, our_items: 0, failed_accounts: 0}}")
    snap = "\n".join(f"- {t['platform']} / {t['owner']} / {t['name']} / {t['url']}" for t in targets) or "(none active)"
    text = text.replace("(snapshot of the Enabled platforms and Active URLs at run start)", snap)
    (dest / "run.md").write_text(text, encoding="utf-8")
    idx = proj / "runs" / "index.md"
    with idx.open("a", encoding="utf-8") as f:
        f.write(f"| {rid} | {rid[:10]} | {', '.join(plats)} | | draft | | {ncomp} competitor targets |\n")
    print(dest)


def approve(run_dir: Path, url: str) -> None:
    rm = run_dir / "run.md"
    t = rm.read_text(encoding="utf-8")
    if re.search(r"^status: approved", t, re.M):
        sys.exit("already approved")
    rm.write_text(set_fm(t, status="approved", approved_at=dt.datetime.now().isoformat(timespec="minutes"),
                         report_url=url or ""), encoding="utf-8")
    idx = run_dir.parent / "index.md"
    lines = idx.read_text(encoding="utf-8").splitlines()
    for i, l in enumerate(lines):
        if l.startswith(f"| {run_dir.name} |"):
            c = [x.strip() for x in l.strip("|").split("|")]
            c[4], c[5] = "approved", url
            lines[i] = "| " + " | ".join(c) + " |"
    idx.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"approved {run_dir.name}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["init", "approve", "list"])
    ap.add_argument("target")
    ap.add_argument("--root", default=str(HERE.parents[3]))
    ap.add_argument("--url", default="")
    a = ap.parse_args()
    if a.cmd == "init":
        init(a.target, Path(a.root))
    elif a.cmd == "approve":
        approve(Path(a.target), a.url)
    else:
        print((Path(a.root) / "competitor_analysis/projects" / a.target / "runs/index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
