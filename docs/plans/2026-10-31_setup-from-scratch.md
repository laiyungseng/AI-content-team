---
type: plan
status: in-progress      # final -> in-progress -> done
created: 2026-10-31
last-updated: 2026-10-31
owner: user
related: [[CLAUDE]], [[2026-10-31_architecture-and-skill-merge]]
---
# Plan: install the AI Content Team from scratch

Goal: set this project up **fast, on any PC (Windows, macOS, Linux), from nothing**. Every install step that needs code is a
script saved in the `installation-setup` skill and documented there, so a Claude session on the new machine can read the skill
and run the setup itself. The user-facing guide lives in `README.md` on GitHub.

---

## 1. The core problem
Skills live in `.claude/skills/` inside the project, so a skill cannot install itself before the project is on the machine.
Setup has three layers; only the last one needs Claude:

| Layer | Runs | Job |
|---|---|---|
| 0 Distribution | git clone (or GitHub ZIP) | Get the system (not client data) onto the machine |
| 1 Bootstrap | `setup.ps1` (Windows) / `setup.sh` (macOS, Linux) | Install uv, then hand over to `setup.py` |
| 2 `installation-setup` | `setup.py` + Claude Code | Tools, Python, folders, connectors, smoke test |

## 2. Decisions (locked)
| # | Decision |
|---|---|
| D1 | Private repo `https://github.com/laiyungseng/AI-content-team.git`; clone (or ZIP) is the install path. |
| D2 | The repo holds the system only. Client data (`brand/<project>`, runs, project memory, state) never enters git. `memory/_system/` **does** travel. |
| D3 | All setup logic is one cross-platform Python script (`setup.py`), run by uv, which also downloads Python itself. The `.ps1`/`.sh` launchers only install uv. The old PowerShell-only scripts are replaced. |
| D4 | Connectors come in two kinds. **Account connectors** (Apify, Zernio, Notion, Figma) follow the user's Claude login; they only need authorising. **Local servers** (Perplexity, nanobanana, NotebookLM) are declared in a project `.mcp.json` and read API keys from environment variables. Keys never go in files, git or chat. |
| D5 | Requirements are tiered by goal; intelligence-only users are never asked for production connectors. |
| D6 | "Installed" means the offline smoke test passed. |
| D7 | Every phase checks before acting and records its result, so re-running setup is safe and resumes. |

## 3. Layer 0: distribution
- **Committed:** `.claude/skills/`, `agents/`, all `_template` folders, `shared/`, `docs/`, `memory/_system/`, `CLAUDE.md`, `README.md`, `pyproject.toml`, `uv.lock`, `.mcp.json`, `setup.ps1`, `setup.sh`.
- **Ignored:** `.venv/`, every non-`_template` project folder in the six domains, `state/installation_status.md`, `.env`, downloaded media.
- Empty template folders carry `.gitkeep` so git keeps them (already written by `scaffold_workspace.py`).

## 4. Layer 1: launchers
`setup.ps1` / `setup.sh`: if `uv` is missing, install it (winget on Windows when present, otherwise the official astral.sh installer),
then run `uv run python .claude/skills/installation-setup/scripts/setup.py all`.

## 5. Layer 2: `setup.py` phases
State is written to `state/installation_status.md` (tools table + phase table).

| Phase | Command | Gate | Done when |
|---|---|---|---|
| 1 Check | `setup.py check` | none | table written; required tools present |
| 2 Tools | `setup.py install <tool...> [--yes]` (winget / brew / apt) | user yes | re-check passes |
| 3 Python | `setup.py python [--media]` (`uv sync`) | user yes for media (large) | imports succeed |
| 4 Workspace | `setup.py scaffold` | none | template folders intact |
| 5 Connectors | Claude follows `references/connectors.md` | user authorises / sets keys | one cheap read-only call works |
| 6 Smoke test | `setup.py smoke` (fixtures -> run -> normalise -> select -> report, then deletes the test project) | none | `report.html` built, test project removed |
| 7 Handoff | point to `source-manager`; `business-onboarding` when production starts | none | summary shown |

`setup.py all` runs 1, 3, 4, 6 and lists what still needs the user (tools to install, connectors).

**Tool tiers:** required = uv, git; needed for Perplexity = node; needed for reels = ffmpeg (with `--media`).
**Connector tiers:** Intelligence MVP = Apify, Perplexity; + nanobanana for images; + Zernio for publishing; NotebookLM, Notion, Figma optional.

## 6. Build order and checklist
- [x] 1. `.gitignore`, `.mcp.json`, launchers
- [x] 2. `setup.py` (check / install / python / scaffold / smoke / all) and `smoke_test.py`; remove the replaced `.ps1` scripts
- [x] 3. `installation-setup/SKILL.md`, `references/connectors.md`, `references/manual_install.md` (per OS), evals; `CLAUDE.md` table
- [x] 4. Test: fresh clone into an empty temp folder, run the launcher, smoke test passes (Windows: setup.ps1 and setup.sh via Git Bash pass; long grader filenames shortened after a "Filename too long" checkout failure)
- [x] 5. `README.md` beginner install guide
- [ ] 6. `git init`, first commit, push to the GitHub repo
- [ ] 7. Later, user: run the guide on a second PC (macOS path untested until then)
