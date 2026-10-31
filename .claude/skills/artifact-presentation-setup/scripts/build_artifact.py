#!/usr/bin/env python3
"""Build a single-file HTML artifact from a template, a data JSON and a theme.

    python build_artifact.py --template approval-board --data data.json --out out.html \
        [--project my_project] [--theme theme.json] [--title "Name"] [--standalone]

Theme lookup order: --theme, then brand/<project>/assets/artifact_theme.json (when --project is
given and the file exists), then assets/themes/default.json.

The output has no <html>/<head>/<body>: the Artifact tool adds the skeleton at publish time.
Use --standalone to wrap it in a full document for a local browser preview.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "assets" / "templates"
DEFAULT_THEME = SKILL / "assets" / "themes" / "default.json"
WORKSPACE = SKILL.parent.parent.parent  # <root>/.claude/skills/<skill>

REQUIRED = {
    "approval-board": ["items"],
    "content-preview": ["items"],
    "intelligence-report": ["summary"],
    "publishing-calendar": ["items"],
    "brand-guideline": ["brand"],
}
TOKEN_KEYS = ["bg", "surface", "surface-2", "fg", "muted", "line", "accent", "accent-fg",
              "good", "warn", "bad", "info"]


def tokens(d: dict) -> str:
    return "".join(f"--{k}:{d[k]};" for k in TOKEN_KEYS if k in d)


def theme_css(theme: dict) -> str:
    f = theme["fonts"]
    base = (f"--font-display:{f['display']};--font-body:{f['body']};--font-mono:{f['mono']};"
            f"--radius:{theme.get('radius', '10px')};")
    light, dark = tokens(theme["light"]), tokens(theme["dark"])
    return (f":root{{{base}{light}}}\n"
            f"@media (prefers-color-scheme: dark){{:root:not([data-theme=\"light\"]){{{dark}color-scheme:dark}}}}\n"
            f":root[data-theme=\"dark\"]{{{dark}color-scheme:dark}}\n")


def load_theme(args) -> tuple[dict, Path]:
    candidates = []
    if args.theme:
        candidates.append(Path(args.theme))
    if args.project:
        candidates.append(WORKSPACE / "brand" / args.project / "assets" / "artifact_theme.json")
    candidates.append(DEFAULT_THEME)
    for p in candidates:
        if p.exists():
            theme = json.loads(p.read_text(encoding="utf-8"))
            missing = [k for k in ("fonts", "light", "dark") if k not in theme]
            if missing:
                sys.exit(f"Theme {p} is missing: {', '.join(missing)}")
            return theme, p
    sys.exit("No theme found")


def safe_json(obj) -> str:
    s = json.dumps(obj, ensure_ascii=False)
    return s.replace("</", "<\\/").replace("<!--", "<\\!--").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", help="template name (e.g. approval-board) or path")
    ap.add_argument("--data", help="data JSON file")
    ap.add_argument("--out", help="output .html path")
    ap.add_argument("--project")
    ap.add_argument("--theme")
    ap.add_argument("--title")
    ap.add_argument("--standalone", action="store_true", help="wrap in a full HTML document for local preview")
    ap.add_argument("--list", action="store_true", help="list templates and exit")
    args = ap.parse_args()

    if args.list:
        for p in sorted(TEMPLATES.glob("*.html")):
            print(p.stem)
        return
    if not (args.template and args.data and args.out):
        ap.error("--template, --data and --out are required")

    tpl_path = Path(args.template)
    if not tpl_path.exists():
        tpl_path = TEMPLATES / f"{args.template}.html"
    if not tpl_path.exists():
        sys.exit(f"Template not found: {args.template}. Use --list.")

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    for key in REQUIRED.get(tpl_path.stem, []):
        if key not in data:
            sys.exit(f"Data is missing required key '{key}' for {tpl_path.stem} (see references/data_schemas.md)")

    theme, theme_path = load_theme(args)
    title = args.title or data.get("title") or tpl_path.stem.replace("-", " ").title()
    data.setdefault("title", title)
    if args.project:
        data.setdefault("project", args.project)

    html = tpl_path.read_text(encoding="utf-8")
    fonts = f'<link rel="stylesheet" href="{theme["fonts_url"]}">' if theme.get("fonts_url") else ""
    shared_css = (TEMPLATES / "_shared.css").read_text(encoding="utf-8")
    shared_js = (TEMPLATES / "_shared.js").read_text(encoding="utf-8")
    html = (html.replace("<!--__FONTS__-->", fonts)
                .replace("/*__THEME__*/", theme_css(theme))
                .replace("/*__SHARED_CSS__*/", shared_css)
                .replace("/*__SHARED_JS__*/", shared_js)
                .replace("__TITLE__", re.sub(r"[<>&]", "", title))
                .replace("__DATA__", safe_json(data)))

    if args.standalone:
        html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                '<style>:root{color-scheme:light}body{margin:0}[hidden]{display:none!important}</style>'
                f'</head><body>{html}</body></html>')

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Built {out} ({out.stat().st_size / 1024:.0f} KB) template={tpl_path.stem} theme={theme_path.name}")


if __name__ == "__main__":
    main()
