# AI Content Intelligence & Generation Team

A multi-agent content system that works as a **continuous learning loop**, not a one-shot generator:
`Evidence > Observation > Insight > Pattern > Hypothesis > Strategy > Campaign > Brief > Content > Performance > Learning`.

## First run
Competitor **intelligence** can run without a brand guideline (onboarding was deferred by the user on 2026-10-31; test on the `demo` project).
**Production** (strategy, content, publishing) needs both an approved intelligence run and a brand guideline. If `brand/` has no project folder besides `_template`, run `business-onboarding` before production work, and do not push it earlier unless the user asks. The build plan and progress are in `docs/plans/2026-10-31_architecture-and-skill-merge.md`.

## Two goals
1. **Content Intelligence**: analyse our own and competitor content, find winning/weak patterns, hooks, gaps, opportunities.
2. **Content Strategy & Production**: turn intelligence into strategy, campaigns, schedule, briefs, finished content, publishing.

## Required workflow order
research > analysis > insight > strategy > campaign > schedule > brief > generation > review > publish > measurement > learning

The orchestrator (`agents/orchestrator.md`) enforces this order. Never generate content before intelligence exists. Never skip review.

## Five concepts, kept separate
| Concept | Where |
|---|---|
| Agents (who) | `agents/` |
| Skills (how) | `.claude/skills/` (runnable), `competitor_analysis/skills/` and `content_creation/skills/` (methodology docs agents read) |
| Brand knowledge (who we are) | `brand/[project]/` |
| Project data (the work) | `competitor_analysis/projects/`, `content_creation/projects/`, `performance/`, `state/` |
| Memory (validated lessons) | `memory/[project]/` |

Use the **same project name** in every folder. Start a new project with `business-onboarding` (or `python .claude/skills/business-onboarding/scripts/init_project.py <name>`).
Folders named `_template` are copy sources; never write project data into them.

## Routing
| Request | Route |
|---|---|
| "update sources", "add a competitor", "show my URLs" | `source-manager` skill (`sources.md` is the only place research reads URLs from) |
| "research competitors", "run analysis", "refresh intelligence" | `competitor-intelligence` skill, driven by the orchestrator through the Phase 1 agents |
| Strategy / content / publish | Production pipeline, blocked until an approved intelligence run exists (`runs/index.md`) |

## Agent routing
| Request | Agent |
|---|---|
| Collect competitor/own content | competitor_researcher |
| Analyse a piece / hooks / performance | competitor_analyzer, hook_analyzer, performance_analyst |
| Combine into patterns, gaps, opportunities | insight_synthesizer |
| Strategy / campaign / schedule | content_strategist, campaign_planner, schedule_planner |
| Write content | reel_creator, carousel_creator, static_content_creator (one brief each) |
| Review | content_reviewer (creators never approve their own work) |
| Publish | publishing_agent (Phase 6 only) |

Phase 1 agents (orchestrator, competitor_researcher, competitor_analyzer, hook_analyzer, performance_analyst, insight_synthesizer) are `status: active`; the rest of `agents/` are stubs until their phases.

## Memory rules
Memory holds **validated** findings only: a pattern needs evidence (count of posts), our own validation if available, a result and a confidence level.
Raw observations stay in project folders (every research run is saved under `runs/<date>/`, never overwritten). Never keep one giant memory file; use the files in `memory/[project]/`.
`memory/_system/` holds how the skills perform (tool failures, user overrides, approved skill edits). After each run, log problems there; skill edits need user approval.
Strategy mix: 70% proven, 20% adjacent, 10% experimental.

## Publishing rules
Only content with `status: approved` **and** `publish_authorized: true` may be published. The user must approve in chat or in an approval artifact. Never publish on inference.

## Presenting work to the user
Outputs and approval requests are shown as interactive Claude Artifacts via the `artifact-presentation-setup` skill (themeable; honours a user reference design).

## Reusable code (do not rewrite; reuse these)
When a task needs code, first look here. If you must write new code, save it in the owning skill's `scripts/` folder and add a row below.

| Script | Purpose |
|---|---|
| `setup.ps1`, `setup.sh` (root) | Fresh-machine launchers: install uv, then `setup.py all` |
| `.claude/skills/installation-setup/scripts/setup.py` | Cross-platform `check` / `install` (winget, brew, apt) / `python` / `scaffold` / `smoke` / `all`; writes `state/installation_status.md` |
| `.claude/skills/installation-setup/scripts/smoke_test.py` | Offline end-to-end pipeline test on a throwaway project (deleted afterwards) |
| `.claude/skills/installation-setup/scripts/scaffold_workspace.py` | Create base folders, agent and methodology stubs (idempotent) |
| `.claude/skills/business-onboarding/scripts/init_project.py` | Copy `_template` folders into a new project in all six places |
| `.claude/skills/business-onboarding/scripts/render_brand_files.py` | Turn interview answers (JSON) into `brand/[project]/*.md` |
| `.claude/skills/artifact-presentation-setup/scripts/build_artifact.py` | Combine template + data + theme into a single HTML artifact file |
| `.claude/skills/source-manager/scripts/sources.py` | `read` / `write` / `status` / `targets` / `build` for `sources.md` and its editor page |
| `.claude/skills/competitor-intelligence/scripts/run.py` | `init` a dated run folder, `approve` it |
| `.claude/skills/competitor-intelligence/scripts/collect.py` | Actor inputs (`plan`), field check (`check`), image download (`media`); Apify itself runs via MCP |
| `.claude/skills/competitor-intelligence/scripts/normalise.py` | Raw actor output -> `items.tsv`; `tag` topics; `stats` baseline |
| `.claude/skills/competitor-intelligence/scripts/build_report.py` | `select` items, `build` the 2-page report |
| `.claude/skills/competitor-intelligence/scripts/to_radar_tsv.py`, `to_perf_tsv.py` | Adapters from `items.tsv` to the radar / performance dashboard inputs |
| `.claude/skills/competitor-intelligence/scripts/radar_build.py`, `perf_build.py` | Copied dashboard builders (optional extra pages) |
| `.claude/skills/competitor-intelligence/scripts/make_test_fixtures.py` | Fake raw data to test a run folder (delete the run afterwards) |

## Conventions
- Major files carry YAML frontmatter and Obsidian `[[links]]`; schema in `shared/schemas/frontmatter.md`.
- Python runs through `uv` (`uv run python ...`), configured in `pyproject.toml`.
- Keep this file short; detailed methodology belongs in skills.
