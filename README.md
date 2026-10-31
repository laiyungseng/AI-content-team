# AI Content Team

A Claude-driven content intelligence and production system. This folder is also an Obsidian vault.

## Get started
Open this folder in Claude Code and say: **"Set up my business"** (runs `business-onboarding`).
It will check your tools, install anything missing, interview you one question at a time, and write your brand guideline.

## Skills (`.claude/skills/`)
| Skill | What it does |
|---|---|
| `installation-setup` | Checks and installs uv, ffmpeg, Python libraries; guides connector setup |
| `business-onboarding` | Studies your business, interviews you, writes `brand/[project]/` |
| `artifact-presentation-setup` | Interactive Claude Artifact pages to present output and collect approval |

## Layout
See `CLAUDE.md` for the full map. Short version: `agents/` (who), `.claude/skills/` (how), `brand/` (identity),
`competitor_analysis/` and `content_creation/` (work), `memory/` (lessons), `performance/`, `state/`, `shared/`.

## Roadmap
1. Intelligence MVP  2. Strategy engine  3. Content generation  4. Obsidian dashboards  5. Performance loop  6. Publishing automation.
Agents and methodology files are stubs until their phase.
