#!/usr/bin/env python3
"""Create the per-project folders in all six places by copying each domain's `_template`.

    python init_project.py <project_name> [--root <workspace>] [--force]

Project names are lowercase snake_case (letters, digits, underscore) so the same name is valid
in every folder and in Obsidian links. Existing project folders are never overwritten unless --force.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

DOMAINS = [
    "brand",
    "competitor_analysis/projects",
    "content_creation/projects",
    "memory",
    "performance",
    "state",
]


def stamp(path: Path, project: str) -> None:
    """Add `project: <name>` to the frontmatter of copied markdown files."""
    for md in path.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if text.startswith("---\n") and "\nproject:" not in text.split("\n---", 1)[0]:
            md.write_text(text.replace("---\n", f"---\nproject: {project}\n", 1), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[4]))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.project):
        sys.exit("Project name must be lowercase snake_case, e.g. penang_cakes")
    root = Path(args.root)

    for rel in DOMAINS:
        base = root / rel
        src, dst = base / "_template", base / args.project
        if not src.exists():
            print(f"SKIP {rel}: no _template (run installation-setup/scripts/scaffold_workspace.py)")
            continue
        if dst.exists():
            if not args.force:
                print(f"EXISTS {dst.relative_to(root)} (left untouched)")
                continue
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        stamp(dst, args.project)
        print(f"CREATED {dst.relative_to(root)}")


if __name__ == "__main__":
    main()
