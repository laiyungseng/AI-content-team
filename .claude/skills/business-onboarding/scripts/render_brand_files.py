#!/usr/bin/env python3
"""Turn interview answers (JSON) into brand/<project>/*.md and artifact data for the guideline page.

    python render_brand_files.py --project penang_cakes --answers answers.json \
        [--root <workspace>] [--artifact-data out.json] [--force]

The answers schema matches the `brand-guideline` artifact template (see assets/answers_example.json),
and loose shapes are accepted (a plain string for positioning, a list of strings for audience, ...).
Existing files are overwritten only if they are still stubs (`status: stub`) or --force is given.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


# ------------------------------------------------------------------ normalizers
def as_list(v):
    return [] if v in (None, "") else (v if isinstance(v, list) else [v])


def norm(a: dict) -> dict:
    n = dict(a)
    b = a.get("brand")
    n["brand"] = {"name": b} if isinstance(b, str) else (b or {})
    p = a.get("positioning")
    n["positioning"] = {"statement": p, "differentiators": []} if isinstance(p, str) else (p or {})
    n["audience"] = [x if isinstance(x, dict) else {"name": "Audience", "description": x} for x in as_list(a.get("audience"))]
    v = a.get("voice")
    n["voice"] = {"traits": v} if isinstance(v, list) else (v or {})
    for key in ("products", "offers"):
        n[key] = [x if isinstance(x, dict) else {"name": x, "description": ""} for x in as_list(a.get(key))]
    n["palette"] = [x if isinstance(x, dict) else {"name": x, "hex": x, "role": ""} for x in as_list(a.get("palette"))]
    n["fonts"] = as_list(a.get("fonts"))
    for key in ("prohibited", "goals", "platforms", "competitors"):
        n[key] = as_list(a.get(key))
    return n


# ------------------------------------------------------------------ markdown helpers
def bullets(items):
    return "\n".join(f"- {i}" for i in items) if items else "_Not provided yet._"


def front(project, kind, extra=""):
    return (f"---\nproject: {project}\ntype: {kind}\nstatus: draft\nupdated: {dt.date.today()}\n{extra}---\n")


def comp_line(c):
    if isinstance(c, dict):
        return " - ".join(str(c[k]) for k in ("name", "handle", "platform", "url") if c.get(k))
    return str(c)


def render(n: dict, project: str) -> dict[str, str]:
    name = n["brand"].get("name", project)
    pos, voice = n["positioning"], n["voice"]
    files: dict[str, str] = {}

    files["positioning.md"] = (front(project, "positioning") + f"# Positioning\n\n{pos.get('statement', '_Not provided yet._')}\n\n"
                               f"## Differentiators\n{bullets(pos.get('differentiators'))}\n")

    aud = "\n\n".join(
        f"### {a.get('name', 'Audience')}\n{a.get('description', '')}\n\n**Pains**\n{bullets(a.get('pains'))}\n\n**Wants**\n{bullets(a.get('desires'))}"
        for a in n["audience"]) or "_Not provided yet._"
    files["audience.md"] = front(project, "audience") + f"# Audience\n\n{aud}\n"

    quotes = "\n".join(f"> {q}" for q in as_list(voice.get("sample_lines")))
    files["brand_voice.md"] = (front(project, "voice") + f"# Brand voice\n\n**Traits:** {', '.join(as_list(voice.get('traits'))) or '_Not provided yet._'}\n\n"
                               f"## We say\n{bullets(as_list(voice.get('do')))}\n\n## We avoid\n{bullets(as_list(voice.get('dont')))}\n\n"
                               f"## Sample lines\n{quotes or '_Not provided yet._'}\n")

    prod = "\n\n".join(f"### {p.get('name')}\n{p.get('description', '')}" + (f"\n\nPrice: {p['price']}" if p.get("price") else "") for p in n["products"])
    files["products_services.md"] = front(project, "products") + f"# Products and services\n\n{prod or '_Not provided yet._'}\n"

    off = "\n\n".join(f"### {o.get('name')}\n{o.get('description', '')}" + (f"\n\nCTA: {o['cta']}" if o.get("cta") else "") for o in n["offers"])
    files["offers.md"] = front(project, "offers") + f"# Offers\n\n{off or '_Not provided yet._'}\n"

    files["prohibited_claims.md"] = front(project, "prohibited") + f"# Prohibited claims\n\nNever say or imply:\n\n{bullets(n['prohibited'])}\n"

    rows = "\n".join(f"| {c.get('name', '')} | `{c.get('hex', '')}` | {c.get('role', '')} |" for c in n["palette"])
    files["assets/colors.md"] = front(project, "colors") + "# Colors\n\n| Name | Hex | Role |\n|---|---|---|\n" + (rows or "| _none yet_ | | |") + "\n"
    frows = "\n".join(f"| {f.get('role', '')} | {f.get('name', '')} | {f.get('sample', '')} |" for f in n["fonts"])
    files["assets/fonts.md"] = front(project, "fonts") + "# Fonts\n\n| Role | Font | Sample |\n|---|---|---|\n" + (frows or "| _none yet_ | | |") + "\n"

    files["brand_guideline.md"] = (
        front(project, "brand_guideline", "tags: [brand]\n") + f"# {name} brand guideline\n\n{n['brand'].get('summary', '')}\n\n"
        f"Tagline: {n['brand'].get('tagline', '-')}\n\n"
        f"## Positioning\n{pos.get('statement', '_Not provided yet._')}\n\nDetails: [[positioning]]\n\n"
        f"## Audience\nSee [[audience]]\n\n## Voice\nTraits: {', '.join(as_list(voice.get('traits'))) or '-'}. See [[brand_voice]]\n\n"
        f"## Products and offers\nSee [[products_services]] and [[offers]]\n\n## Visual identity\nSee [[colors]] and [[fonts]]\n\n"
        f"## Goals\n{bullets(n['goals'])}\n\n## Platforms\n{bullets(n['platforms'])}\n\n## Never say\nSee [[prohibited_claims]]\n")
    return files


def safe_write(path: Path, text: str, force: bool) -> str:
    if path.exists() and not force and "status: stub" not in path.read_text(encoding="utf-8"):
        return f"KEPT    {path} (already written; use --force)"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return f"WROTE   {path}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--answers", required=True)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[4]))
    ap.add_argument("--artifact-data", help="also write normalized data for the brand-guideline artifact template")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    n = norm(json.loads(Path(args.answers).read_text(encoding="utf-8")))
    root = Path(args.root)
    brand_dir = root / "brand" / args.project
    if not (root / "brand" / "_template").exists() and not brand_dir.exists():
        sys.exit("Workspace not scaffolded. Run installation-setup/scripts/scaffold_workspace.py first.")

    for rel, text in render(n, args.project).items():
        print(safe_write(brand_dir / rel, text, args.force))

    if n["competitors"]:
        text = front(args.project, "competitors") + "# Competitors to study\n\n" + bullets([comp_line(c) for c in n["competitors"]]) + "\n"
        print(safe_write(root / "competitor_analysis" / "projects" / args.project / "sources" / "competitors.md", text, args.force))

    if args.artifact_data:
        out = Path(args.artifact_data)
        out.parent.mkdir(parents=True, exist_ok=True)
        data = {k: n[k] for k in ("brand", "positioning", "audience", "voice", "products", "offers", "palette", "fonts", "prohibited")}
        data["project"] = args.project
        data["title"] = f"{n['brand'].get('name', args.project)} Brand Guideline"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"WROTE   {out}")


if __name__ == "__main__":
    main()
