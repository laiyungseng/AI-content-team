---
type: plan
status: final            # final -> in-progress -> done
created: 2026-10-31
last-updated: 2026-10-31
owner: user
related: [[CLAUDE]]
---
# Final plan: workflow architecture + skill merge

The single source of truth for building the AI Content Team workflow. Every later session reads this first
and ticks the checklist at the bottom as work lands. Nothing in it is built yet.

---

## 1. Goal and scope
Build the complete, working **competitor-intelligence pipeline** (Phase 1) on top of a memory and self-improvement layer,
and merge three external skill sources into the project so later phases (strategy, production, performance) have their method ready.

**In scope now:** shared foundations, memory layer, URL settings + editor, competitor-intelligence run, 2-page report, Phase 1 agents, end-to-end test.
**Prepared but built later:** Phase 2 strategy, Phase 3 production, Phase 5 performance loop, Phase 6 publishing.
**Deferred by user:** business onboarding / brand knowledge (run after the workflow works).

## 2. Decisions (locked)
| # | Decision |
|---|---|
| D1 | Onboarding is deferred. The workflow is built and tested on a dummy project first. |
| D2 | Two pipelines under one orchestrator: **Intelligence** (research → analysis → insight) and **Production** (strategy → content → publish). |
| D3 | All target URLs live in `sources.md`: one table per platform, Competitors and Ours sections, per-platform **Enabled** switch, per-URL **Active** status. Research reads nothing else. |
| D4 | A `source-manager` skill shows and edits `sources.md` through an artifact; edits are synced back into the file. |
| D5 | Research output is a **2-page artifact**: (1) scraped items sorted Adapt / Copy / Ignore with image + link, (2) us-vs-them comparison with strengths, why, how to implement, strategy and positioning. |
| D6 | Approved reports are saved as dated, never-overwritten run records. |
| D7 | Memory holds validated lessons only; a system-level memory + retrospective step improves the skills over time, with user approval for every skill edit. |
| D8 | External skills are merged by copying method files verbatim, keeping tested build scripts and templates unchanged, and adapting only paths, names and rules. |

## 3. Defaults for the open questions
These hold unless the user changes them; change here, not in code.

| Question | Default |
|---|---|
| Test project name | `demo` (folders only via `init_project.py`, no brand interview) |
| What is collected per platform | Meta = **Ad Library ads**; Instagram, TikTok, XHS = **organic posts** |
| Radar dashboard | Kept as an **optional 3rd page** ("Performance radar") of the report |
| Collection tool | Apify for all platforms. **Apify must be authorised via `/mcp` before step 5 can be tested** |
| Default window / volume | 90 days, 30 posts per account (20 for XHS) |

## 4. Target file structure (new or changed items only)
```
docs/plans/                          this plan
shared/
  frameworks/hooks.md, cta.md, storytelling.md      filled from scriptwriting skill
  frameworks/writing_insights.md                    NEW  house rule for all findings
  frameworks/stats_rules.md                         NEW  merged statistics rulebook
  platform_rules/instagram.md, tiktok.md, linkedin.md, meta.md (NEW), xhs.md (NEW)
memory/
  _template/*.md                                    real block formats
  _system/skill_feedback/<skill>.md                 NEW  per-skill problems + user overrides
  _system/changelog.md                              NEW  approved skill edits
competitor_analysis/projects/[project]/
  sources.md                                        NEW  URL settings
  runs/index.md                                     NEW  list of all runs
  runs/YYYY-MM-DD_HHMM/
    run.md            frontmatter: platforms, counts, status draft|approved
    raw/<platform>/   collector output
    media/            downloaded images
    items.tsv         unified normalised data
    analysis/verdicts.md, ours.md, comparison.md
    report.html       built artifact
.claude/skills/
  source-manager/                                   NEW
    SKILL.md, scripts/sources.py, assets/sources_editor.html
  competitor-intelligence/                          NEW
    SKILL.md
    references/ platform_scraping.md, requirements.md, output_schema.md,
                verdict_rules.md, comparison_method.md, writing_guide.md,
                selection.md, stats_rules.md (link), hook_research.md
    scripts/  collect.py, normalise.py, to_radar_tsv.py, to_perf_tsv.py,
              radar_build.py (copied), perf_build.py (copied), build_report.py
    assets/   radar_template.html (copied), perf_template.html (copied),
              report_template.html (NEW, 2-3 pages)
  business-onboarding/references/                   + interview_rules.md, brand.md, voice.md, platform.md, examples.md
content_creation/skills/scriptwriting/               copied scriptwriting references (Phase 3)
```

## 5. Architecture

### 5.1 Memory and continuous improvement
| Layer | Purpose | Location |
|---|---|---|
| Run history | Every run saved, dated, never overwritten | `runs/<ts>/` + `runs/index.md` |
| Brand memory (validated) | Lessons about this brand. Promoted only with evidence: post count, result, confidence | `memory/[project]/*.md` |
| System memory | How the skills perform across projects: broken actor, missing field, repeated user overrides, platform changes | `memory/_system/` |
| Retrospective | Last step of every run: log problems and overrides. Every 3 runs (or on request): propose concrete edits to reference files, apply only after user approval, log in `changelog.md` | built into each runnable skill |

User overrides of Adapt / Copy / Ignore are the main signal for recalibrating `verdict_rules.md`.

### 5.2 `sources.md` format
```markdown
## Platforms
| Platform  | Enabled | Max posts | Date range |
|-----------|---------|-----------|------------|
| meta      | yes     | 30        | 90d        |
| instagram | yes     | 30        | 90d        |
| tiktok    | no      | 30        | 90d        |
| xhs       | yes     | 20        | 90d        |

## Topics
| Key | Label |                      shared 4-6 topic taxonomy, stable across runs

# Competitors
## Meta
| Name | URL | Profile or page | Active |
|------|-----|-----------------|--------|
## Instagram
## TikTok
## XHS

# Ours
## Meta
## Instagram
## TikTok
## XHS
```
Rule: scrape a URL only when its platform is Enabled **and** its row is Active.

### 5.3 `source-manager` skill
1. `sources.py read` turns `sources.md` into JSON; the editor page is built with it.
2. Page: Competitors / Ours switch, one table per platform, add / remove / Active checkbox, platform Enabled toggles. Edits go to the artifact `db`.
3. Sync: on "save / sync sources" and automatically at the start of every research run, Claude reads the db (ArtifactData), `sources.py write` rewrites `sources.md`, and the page is republished to the same URL.
4. Conflict: if `sources.md` changed by hand since the last sync, ask which version wins.

### 5.4 `competitor-intelligence` skill (one run)
```
sync sources -> collect (enabled platforms, active URLs) -> normalise -> analyse competitors
-> analyse ours -> compare + strategy -> build report -> present -> approval
   approved:  run.md status approved, promote lessons, retrospective
   changes:   revise, re-present at the same URL
```
| Step | Agent | Output |
|---|---|---|
| Sync + collect | competitor_researcher | `raw/<platform>/`, `media/` |
| Normalise | competitor_researcher | `items.tsv` |
| Verdict per competitor item | competitor_analyzer + hook_analyzer | `analysis/verdicts.md` |
| Our baseline | performance_analyst | `analysis/ours.md` |
| Us vs them, strategy, positioning | insight_synthesizer | `analysis/comparison.md` |
| Build + present + approval | artifact-presentation-setup | `report.html` |
| Promote + retrospective | orchestrator | `memory/[project]/`, `memory/_system/` |

### 5.5 Report artifact
- **Page 1, Scraped content:** cards grouped Adapt / Copy / Ignore; image, original link, platform, metrics, reason; per-card override + comment.
- **Page 2, Us vs them:** rows hook, format, visual, message, offer, CTA, cadence, engagement; columns ours, theirs, stronger, why, how we implement; then a strategy and positioning section.
- **Page 3 (optional), Performance radar:** the copied radar dashboard fed from `items.tsv`.
- Images are downloaded and uploaded as artifact assets (platform image links expire and block hotlinking).
- Decisions are stored in the artifact db (`decisions` collection), as in `artifact-presentation-setup/references/approvals.md`.

### 5.6 Unified data schema (`items.tsv`)
`owner(ours|competitor)  accountId  platform  itemType(post|ad)  itemId  date  views  likes  comments  shares  saves  durationSec  topic  pillar  caption  mediaUrl  permalink  status`

Null rules from the radar apply: empty = missing, never 0; photo posts have no views; Instagram has no shares/saves;
private / failed / empty accounts are kept with a `status` and note, never dropped.
Adapters (`to_radar_tsv.py`, `to_perf_tsv.py`) convert to each dashboard's 11-column format so their scripts stay untouched.

### 5.7 Routing
| Request | Route |
|---|---|
| "update sources", "add a competitor", "show my URLs" | source-manager |
| "research competitors", "run analysis", "refresh intelligence" | competitor-intelligence (orchestrator drives the agents) |
| strategy / content / publish requests | Production pipeline (later phases), blocked until an approved intelligence run exists |

## 6. Merge map
Legend: **copy** verbatim · **adapt** copy then change paths/names/rules · **new** written fresh · **later** prepared for a later phase.

### 6.1 competitor-content-radar (`D:\Document\A22A\competitor-content-radar.zip`)
| Piece | Destination | How |
|---|---|---|
| Actor inputs, `fields` lists, batching (one run per platform for all handles) | `platform_scraping.md` | adapt; add Meta + XHS rows |
| Account status rules | `requirements.md`, `normalise.py` | copy rule |
| `posts.tsv` null rules | `output_schema.md` | adapt into 5.6 |
| Topic taxonomy 4-6, stable keys | `sources.md` Topics table, `comparison_method.md` | adapt |
| `build.py` + template | `radar_build.py`, `radar_template.html` | copy unchanged |
| `maintainer-notes.md` | `shared/frameworks/stats_rules.md` | copy; plain-language and "Do next:" rules apply to our report too |
| Template statistical upgrade (target spec) | backlog | later |
| `python3`, `/mnt/user-data/outputs/` | `uv run python`, `runs/<ts>/` | adapt |

### 6.2 content-performance-dashboard (`D:\Document\A22A\content-performance-dashboard.zip`)
| Piece | Destination | How |
|---|---|---|
| `build.py analyze` (outlier score, quadrants, topic ranking) | `perf_build.py`, used for the "Ours" baseline | copy unchanged |
| Template | `perf_template.html`; Phase 5 weekly/monthly snapshot | copy unchanged |
| `writing-insights.md` | `shared/frameworks/writing_insights.md`, required reading for every analyst | copy |
| `design-notes.md` statistics | merged into `stats_rules.md` | adapt; record where the radar and dashboard differ |
| 7/30/90 window | `sources.md` Date range | adapt |

### 6.3 social-media-automation plugin 0.2.0 (`D:\Document\A22A\Social Media Automation\skills & plugins\`)
| Piece | Destination | How |
|---|---|---|
| `writing-a-hook.md`, `hook-examples.md`, `psychology.md` | `shared/frameworks/hooks.md` + hook_analyzer method (4-component model: spoken, text, visual, audio) | copy |
| `hook-research.md` | `competitor-intelligence/references/hook_research.md`, `competitor_analysis/skills/hook_analysis.md` | adapt; sortfeed step replaced by our Apify pull ranked by ratio |
| `ctas.md` | `shared/frameworks/cta.md`, `content_creation/skills/CTA_generation.md` | copy |
| `formats.md`, `writing-a-script.md` | `shared/frameworks/storytelling.md`, `content_creation/skills/reel_generation.md` | copy, later |
| `diagnosing.md` | content_reviewer method, Phase 5 "why did this flop" | copy, later |
| `production-notes.md` | reel_creator reference | copy, later |
| Scriptwriting router SKILL | `agents/reel_creator.md` routing section | adapt, later |
| `content-strategist` + interview guide, pillar patterns, output templates | `agents/content_strategist.md`, `content_creation/skills/content_strategy.md`, `templates/content_strategy.md` | adapt, later; reads intelligence first, interviews only for gaps |
| Intent mix Educate / Engage / Promote | strategy rules | kept alongside 70/20/10 proven/adjacent/experimental; every planned post gets both tags |
| Pillars (max 3, series, tagging rule) | strategy + `items.tsv` `pillar` column | adopt; links strategy to measurement |
| `initial-brand-folder-setup` rules + `brand.md`, `voice.md`, `platform.md`, `examples.md` | `business-onboarding/references/` | adapt; 01-brand → `brand_guideline/positioning/audience/products_services.md`, 02-guidelines → `brand_voice.md` + `prohibited_claims.md`, 03-platforms → `brand/[project]/platforms/<platform>.md` |

Every copied file gets frontmatter `source: <origin>` and `copied: 2026-10-31` so its origin stays traceable.

## 7. Conflicts and resolutions
| Conflict | Resolution |
|---|---|
| Plugin and radar are installed globally as `social-media-automation:*` skills and would compete with project skills | User disables the plugin after step 9 |
| Radar forbids db; report and editor need db | Dashboard pages stay static; report and source-manager use db |
| Plugin folder layout (`01-brand/`…`04-strategy/`) | This project's layout wins; paths rewritten |
| Topics (4-6) vs pillars (max 3) | Competitors: shared topics. Ours: topic + pillar both recorded |
| 50/20/30 intent mix vs 70/20/10 | Different axes, both kept |
| Dashboards support IG + TikTok only | Collector adds Meta + XHS; dashboards show IG/TikTok until extended |
| Radar vs dashboard stats differ (engagement definition, baseline) | `stats_rules.md` states one rule per metric and which page uses which |

## 8. Build steps
| Step | Work | Done when |
|---|---|---|
| 1 | Copy sources into the project per section 6, with `source:` frontmatter | All files in place; build scripts run unchanged on the sources' own sample data |
| 2 | Shared foundations: `writing_insights.md`, `stats_rules.md`, `hooks.md`, `cta.md`, `storytelling.md`, platform rules incl. `meta.md`, `xhs.md` | No `status: stub` left in `shared/` |
| 3 | Memory layer: block formats for `memory/_template/*`, `memory/_system/`, run folder layout, `runs/index.md` template | Templates exist; `init_project.py` copies them |
| 4 | `sources.md` + `sources.py` + `source-manager` skill and editor artifact with db sync | Add / remove / toggle in the page, sync, and the change appears in `sources.md` (and the reverse) |
| 5 | `competitor-intelligence`: collector, normaliser, adapters, method files, verdict rules, report template, approval → save → promote → retrospective | A run on `demo` produces a run folder and a 2-page report; approval marks it approved |
| 6 | Fill Phase 1 agents: orchestrator, competitor_researcher, competitor_analyzer, hook_analyzer, performance_analyst, insight_synthesizer | No TODO sections; each names its inputs, outputs and method files |
| 7 | End-to-end test on `demo` with real URLs (needs Apify) | Full run, user override recorded in `_system`, lesson promoted to `memory/demo/` |
| 8 | Later phases: Phase 2 strategy, Phase 3 production, Phase 5 performance, Phase 6 publishing, using the material prepared in step 1 | Separate plans per phase |
| 9 | Update `CLAUDE.md` (routing, folders, reusable-code table); user disables the duplicate plugin | `CLAUDE.md` matches the built system |

## 9. Risks
| Risk | Mitigation |
|---|---|
| XHS scrapers on Apify are community-built and less reliable | 2-item test pull before every full run; fallback actor listed in `platform_scraping.md`; failures logged to `_system` |
| Actor output fields change | Collector checks mapped fields on the test pull; missing fields stop the run with a clear message |
| Small samples (20-40 posts) give weak conclusions | `stats_rules.md`: "too early to call", never fabricate, quote post counts |
| Artifact cannot write to disk directly | Explicit sync step + automatic sync at run start + conflict check |
| Platform images expire | Download to `media/` at collection time, upload as artifact assets |

## 10. Progress checklist
- [x] Plan written and finalised (2026-10-31)
- [x] Step 1 sources copied (2026-10-31). Build scripts/templates byte-identical and start cleanly; the zips ship no sample data, so a build on sample data is deferred to step 5. Adapt-type sources are staged as `_src_*.md` beside their destination (`competitor-intelligence/references/`, `content_creation/skills/strategist_source|scriptwriting/`) and get rewritten in steps 2/5; `business-onboarding/references/` got brand/voice/platform/examples/interview_rules.
- [x] Step 2 shared foundations (2026-10-31). No stubs left in `shared/`. `stats_rules.md` now opens with a per-metric table of radar vs dashboard differences. Platform specs for Instagram/TikTok/LinkedIn/Meta/XHS are written from general knowledge; numeric limits marked "(verify)" need checking before first publish.
- [x] Step 3 memory layer (2026-10-31). Block formats in `memory/_template/*`; `memory/_system/` (README, changelog, skill_feedback/_format.md); `runs/index.md` + `runs/_run_template/` in the competitor_analysis template (copied by the unchanged `init_project.py`). `demo` project folders created in all six places.
- [x] Step 4 sources.md + source-manager (2026-10-31). `sources.md` template in `competitor_analysis/projects/_template/`; `source-manager` skill with `sources.py` (read/write/status/targets/build) and `sources_editor.html`. Tested on `demo`: file -> page build, simulated page edit in db -> `sources.md`, hand-edit conflict detected, `targets` honours Enabled + Active. Demo editor: https://claude.ai/artifact/PdLsCUVnbKJC4c7pFYrfMx. NOT yet tested: clicking add/remove/toggle in the live page (only the JS syntax and db path were checked).
- [x] Step 5 competitor-intelligence (2026-10-31), tested on fake fixtures only (no Apify yet). Built: SKILL.md, 8 reference files, scripts `run.py` (init/approve), `collect.py` (plan/check/media), `normalise.py` (build/tag/stats), `build_report.py` (select/build), `to_radar_tsv.py`, `to_perf_tsv.py`, `report_template.html`. Verified on fixtures: all 4 platforms normalise, radar adapter output builds with unchanged `radar_build.py`, report builds and renders (27 cards, 8 comparison rows, no overflow), approve is idempotent-safe. Fixture run deleted afterwards. Deviations from plan: analysis files are JSON (`verdicts.json`, `ours.json`, `comparison.json`), not `.md`; page 3 radar is a separate linked artifact, not an in-report tab; `collect.py` prepares inputs/checks, Apify is called via MCP (no REST/token code); the two dashboard scripts' template path lines were edited to the new asset names. Not verified: real actor field names (Meta/XHS are guesses, XHS actor not chosen), `to_perf_tsv.py` end to end (fixtures had no Ours TikTok), the approval flow clicked in the live artifact, `media` download on real URLs. Test report artifact (fixture data): https://claude.ai/artifact/HrMxvY22LFPKQowiHWWuyM
- [x] Step 6 Phase 1 agents (2026-10-31). orchestrator, competitor_researcher, competitor_analyzer, hook_analyzer, performance_analyst, insight_synthesizer now `status: active` with inputs, outputs, method files and stop conditions; no TODO left in them. Also filled the four methodology files they read (`content_scoring`, `hook_analysis`, `performance_analysis`, `pattern_detection`); `hooks.json` added to `output_schema.md`. Agents were checked by path scan only, never run as subagents; the other 8 agents in `agents/` remain stubs (later phases).
- [ ] Step 7 end-to-end test (needs Apify authorised)
- [ ] Step 8 later phases
- [~] Step 9 CLAUDE.md + plugin cleanup (2026-10-31): `CLAUDE.md` updated (first-run rule, routing, memory/_system, reusable-code table). STILL OPEN, user action: disable the global `social-media-automation` plugin and the standalone `competitor-content-radar` / `content-performance-dashboard` skills so they do not compete with the project skills. Steps 7 and 8 also open.

## 11. Setup status snapshot (2026-10-31, end of session 1)

**Built and checked (on fixtures / dry runs)**
- Source material copied from the radar, performance dashboard and plugin (step 1).
- `shared/` foundations: stats rules, writing insights, hooks, CTA, storytelling, experimentation, 5 platform rules.
- Memory layer: block formats, `memory/_system/`, run folder layout, `demo` project folders.
- `source-manager`: `sources.md` template, `sources.py`, editor page (demo editor artifact published; add/remove/toggle clicks not tested in the live page).
- `competitor-intelligence`: SKILL, references, scripts, report template; tested on fake data only.
- 6 Phase 1 agents and 4 methodology files filled in.
- `CLAUDE.md` updated.

**Pending**
1. User: authorise Apify via `/mcp` (in progress).
2. User: provide real competitor and own URLs (and optional topics); decide whether to keep project name `demo`.
3. Step 7 end-to-end run: confirm Meta and XHS actor/field names, choose the XHS actor, test `media` download, click through the live approval flow, test `to_perf_tsv.py` (needs Ours on Instagram and TikTok), record an override and promote a lesson.
4. Step 8: separate plans for Phase 2 strategy, Phase 3 production, Phase 5 performance, Phase 6 publishing. The 8 agents still `status: stub`: content_strategist, campaign_planner, schedule_planner, reel_creator, carousel_creator, static_content_creator, content_reviewer, publishing_agent.
5. Step 9 remainder, user: disable the global `social-media-automation` plugin and the standalone radar/dashboard skills.
6. Later: business onboarding / brand guideline (deferred by the user); verify the "(verify)" platform limits in `shared/platform_rules/`.
7. Leftovers: fixture test report artifact (https://claude.ai/artifact/HrMxvY22LFPKQowiHWWuyM) can be deleted on request; demo editor artifact (https://claude.ai/artifact/PdLsCUVnbKJC4c7pFYrfMx) holds stale test data in its db until the real sources are synced.

**Verification 2026-10-31 (session 2)**
- On disk: steps 1-6 confirmed (6 Phase 1 agents active, no stubs in `shared/`, all skill scripts compile).
- Step 9 plugin cleanup appears done: no `social-media-automation` / radar / dashboard skills load in this session.
- Apify: the claude.ai Apify connector answers (FREE tier); step 7 now waits only on real URLs. XHS actor candidates: `zhorex/rednote-xiaohongshu-scraper` (profile URLs), `socialdatax/socialdatax-xhs-data-api`.
- Zernio: connected, one `Default` profile, **no social accounts connected**.
- Gaps: `competitor_analysis/skills/` `competitor_analysis.md`, `competitor_research.md`, `report_generation.md` and the 5 files in `competitor_analysis/templates/` are still stubs and no agent links them (superseded by `competitor-intelligence/references/`); `_src_radar_SKILL.md` and `_src_perf_SKILL.md` still sit in `competitor-intelligence/references/`.
- `2026-10-31_setup-from-scratch.md`: 0 of 9 items done (no git repo, `.gitignore`, `.mcp.json`, `setup.ps1`, smoke test).
