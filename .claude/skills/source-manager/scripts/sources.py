#!/usr/bin/env python3
"""Read, write, check and build the editor for a project's sources.md.

    sources.py read    <sources.md>                 print JSON (adds sha256 of the file)
    sources.py write   <sources.md> <state.json>    rewrite sources.md from JSON, record sync hash
    sources.py status  <sources.md>                 in-sync | changed-by-hand | never-synced
    sources.py targets <sources.md>                 print URLs to scrape (platform Enabled AND row Active)
    sources.py build   <sources.md> <out.html>      editor page fragment seeded from sources.md

State JSON: {"platforms":[{"key","enabled","maxPosts","range"}], "topics":[{"key","label"}],
             "competitors":{platform:[row]}, "ours":{platform:[row]}}; row = {"name","url","type","active"}
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PLATFORMS = {"meta": "Meta", "instagram": "Instagram", "tiktok": "TikTok", "xhs": "XHS"}
DEFAULT_POSTS = {"meta": 30, "instagram": 30, "tiktok": 30, "xhs": 20}
NAME_TO_KEY = {v.lower(): k for k, v in PLATFORMS.items()}
TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "sources_editor.html"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_rows(lines: list[str]) -> list[list[str]]:
    rows = [cells(l) for l in lines if l.strip().startswith("|")]
    return rows[2:] if len(rows) > 2 else []  # drop header + separator


def yes(v: str) -> bool:
    return v.strip().lower() in ("yes", "y", "true", "1", "active")


def empty_state() -> dict:
    return {
        "platforms": [{"key": k, "enabled": False, "maxPosts": DEFAULT_POSTS[k], "range": "90d"} for k in PLATFORMS],
        "topics": [],
        "competitors": {k: [] for k in PLATFORMS},
        "ours": {k: [] for k in PLATFORMS},
    }


def parse(text: str) -> dict:
    state = empty_state()
    top, platform, buf = None, None, []  # top: platforms|topics|competitors|ours

    def flush() -> None:
        rows = table_rows(buf)
        if top == "platforms":
            for r in rows:
                key = NAME_TO_KEY.get(r[0].lower())
                if key and len(r) >= 4:
                    p = next(p for p in state["platforms"] if p["key"] == key)
                    p.update(enabled=yes(r[1]), maxPosts=int(r[2]) if r[2].isdigit() else p["maxPosts"], range=r[3] or p["range"])
        elif top == "topics":
            state["topics"] = [{"key": r[0], "label": r[1]} for r in rows if len(r) >= 2 and r[0]]
        elif top in ("competitors", "ours") and platform:
            state[top][platform] = [
                {"name": r[0], "url": r[1], "type": r[2] if len(r) > 2 else "", "active": yes(r[3]) if len(r) > 3 else True}
                for r in rows if len(r) >= 2 and (r[0] or r[1])
            ]

    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# ") or s.startswith("## "):
            flush()
            buf = []
            title = s.lstrip("#").strip().lower()
            if s.startswith("# "):
                top, platform = (title if title in ("competitors", "ours") else None), None
            elif top in ("competitors", "ours"):
                platform = NAME_TO_KEY.get(title)
            else:
                top, platform = (title if title in ("platforms", "topics") else None), None
        else:
            buf.append(line)
    flush()
    return state


def render(state: dict) -> str:
    out = [
        "---", "type: sources", "status: active", "---", "# Sources", "",
        "All target URLs for research live here and nowhere else. Scrape a URL only when its platform is",
        "Enabled **and** its row is Active. Edit through the `source-manager` page or by hand.", "",
        "## Platforms", "| Platform | Enabled | Max posts | Date range |", "|---|---|---|---|",
    ]
    for p in state["platforms"]:
        out.append(f"| {PLATFORMS[p['key']].lower()} | {'yes' if p['enabled'] else 'no'} | {p['maxPosts']} | {p['range']} |")
    out += ["", "## Topics", "", "| Key | Label |", "|---|---|"]
    out += [f"| {t['key']} | {t['label']} |" for t in state["topics"]]
    for section, title in (("competitors", "Competitors"), ("ours", "Ours")):
        out += ["", f"# {title}"]
        for k, name in PLATFORMS.items():
            out += ["", f"## {name}", "| Name | URL | Profile or page | Active |", "|---|---|---|---|"]
            out += [f"| {r['name']} | {r['url']} | {r.get('type', '')} | {'yes' if r['active'] else 'no'} |" for r in state[section][k]]
    return "\n".join(out) + "\n"


def sync_file(path: Path) -> Path:
    return path.with_name(path.name + ".sync")


def cmd_read(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return {**parse(text), "sha256": sha(text)}


def cmd_write(path: Path, state_path: Path) -> None:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    for k in ("platforms", "topics", "competitors", "ours"):
        if k not in state:
            sys.exit(f"state JSON missing '{k}'")
    for sec in ("competitors", "ours"):
        for k in PLATFORMS:
            state[sec].setdefault(k, [])
    text = render(state)
    path.write_text(text, encoding="utf-8")
    sync_file(path).write_text(sha(text), encoding="utf-8")


def cmd_status(path: Path) -> str:
    sf = sync_file(path)
    if not sf.exists():
        return "never-synced"
    return "in-sync" if sf.read_text().strip() == sha(path.read_text(encoding="utf-8")) else "changed-by-hand"


def cmd_targets(path: Path) -> list[dict]:
    state = parse(path.read_text(encoding="utf-8"))
    out = []
    for p in state["platforms"]:
        if not p["enabled"]:
            continue
        for owner, sec in (("competitor", "competitors"), ("ours", "ours")):
            for r in state[sec][p["key"]]:
                if r["active"] and r["url"]:
                    out.append({"platform": p["key"], "owner": owner, "name": r["name"], "url": r["url"],
                                "maxPosts": p["maxPosts"], "range": p["range"]})
    return out


def cmd_build(path: Path, out: Path) -> None:
    seed = json.dumps(cmd_read(path), ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__SOURCES_JSON__", seed)
    out.write_text(html, encoding="utf-8")


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, path = sys.argv[1], Path(sys.argv[2])
    if cmd == "read":
        print(json.dumps(cmd_read(path), indent=2, ensure_ascii=False))
    elif cmd == "write":
        cmd_write(path, Path(sys.argv[3]))
        print(f"wrote {path}")
    elif cmd == "status":
        print(cmd_status(path))
    elif cmd == "targets":
        print(json.dumps(cmd_targets(path), indent=2, ensure_ascii=False))
    elif cmd == "build":
        cmd_build(path, Path(sys.argv[3]))
        print(f"built {sys.argv[3]}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
