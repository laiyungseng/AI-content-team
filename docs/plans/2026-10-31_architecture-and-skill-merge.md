---
type: plan
status: in-progress      # final -> in-progress -> done
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
and merge four external skill sources into the project so later phases (strategy, production, performance) have their method ready.
The fourth source, the UPT course bundle (section 6.4), was added on 2026-10-31 after a review; it mostly feeds Phase 2 and 3 and adds competitor discovery to Phase 1.
The agent-by-agent workflow with tools and human checkpoints is drawn in `docs/diagrams/agent-workflow.html` (artifact: https://claude.ai/artifact/5VYzVNaxHczm7hZTy3gPn2).

**In scope now:** shared foundations, memory layer, URL settings + editor, competitor-intelligence run, 2-page report, Phase 1 agents, end-to-end test, Phase 1 upgrades from the UPT bundle (step 11).
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
| D9 | The UPT bundle is merged by **method only**: its installer is never run (it writes to the global `~/.claude/skills` and `settings.json`), its client data and personal paths are stripped, and Lovart is not adopted (nanobanana covers images). |
| D10 | Competitor material is never cloned 1:1. Where a source says "mirror the original structure", we keep our rule: extract the reusable formula, never copy claims, footage, music or text. |

## 3. Defaults for the open questions
These hold unless the user changes them; change here, not in code.

| Question | Default |
|---|---|
| Test project name | `demo` (folders only via `init_project.py`, no brand interview) |
| What is collected per platform | Meta = **Ad Library ads**; Instagram, TikTok, XHS = **organic posts** |
| Radar dashboard | Kept as an **optional 3rd page** ("Performance radar") of the report |
| Collection tool | Apify for all platforms. **Apify must be authorised via `/mcp` before step 5 can be tested** |
| Default window / volume | 90 days, 30 posts per account (20 for XHS) |
| Competitor discovery | Either the official Meta Ads connector (`ads_library_search`, added at claude.ai/settings/connectors; needs a Facebook ad account) or the Apify Ad Library keyword URL already in `platform_scraping.md`; whichever is available. Apify stays the collector |
| Carousel / static rendering | `carousel-html` templates rendered by headless Chrome to exact 1080×1350 PNG (needs Chrome) |
| Image generation | nanobanana; Higgsfield optional for video; Lovart not used |
| Video download for hooks | Meta ads: direct video URL from the actor. TikTok / Instagram: `yt-dlp` first (free), Apify downloader actor only if it fails |
| Transcription | `faster-whisper` locally (step 10 choice); Groq Whisper is an optional faster fallback that needs a key |
| Market-specific copy rules | UPT's Malaysian-Chinese (Rojak) style rules apply only when `brand/[project]/` names that market; otherwise they stay as examples |

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
docs/diagrams/agent-workflow.html                     NEW  workflow block diagram
--- added by the UPT bundle merge (6.4) ---
.claude/skills/source-manager/references/competitor_discovery.md      NEW  census method (step 11)
.claude/skills/competitor-intelligence/scripts/transcribe.py          NEW  download, frames, transcript (step 10)
content_creation/skills/carousel_render/                               NEW  assets/{templates,brand-kits,scripts/render.py} in the original layout so render.py runs; docs/; brand_kit.py still to build (8b)
content_creation/skills/{angle_source,ad_copy_source,reel_source,static_source}/   NEW  staged `_src_upt_*.md`, rewritten in steps 8a / 8b
content_creation/skills/angle_evaluation.md                            NEW  UPT rubric + kill filter + generic detector
content_creation/skills/ad_copy_longform.md                            NEW  SNICK.C + 6-part skeleton
content_creation/skills/reel_generation.md                             + shot list, anti-slop rules, Higgsfield phases
content_creation/tests/angle_eval_cases/                               NEW  UPT eval cases, de-branded
shared/platform_rules/meta.md                                          + safe-claims rules
brand/_template/prohibited_claims.md                                   + finance / sensitive claims checklist
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

### 6.4 UPT course bundle (`C:\Users\PC\Downloads\UPT-course-setup-v2.skill`, reviewed 2026-10-31)
An installer (`course-setup-v2`) carrying 10 Chinese-language course skills. Safety review: no malicious code; network calls go only to Lovart and Groq;
SSL checks on by default. Not usable as-is: it installs globally, contains other people's client data (UPT, Jayden, `coachjayden`, First N Ever and others),
hard-coded paths (`~/Downloads/fb_ad_research`, `100_Todo/drafts`) and points to skills that are not in the bundle (`ugc-ad-ref`, `creative-director`, `design-critic`, `viral-video-teardown`).

| Piece | Destination | How | Phase |
|---|---|---|---|
| `fb-competitor-census-mcp-15m`: query grid, Page ID dedupe, per-Page active-ad count, saturation check | `source-manager/references/competitor_discovery.md`; new `discover` mode shows candidates as "suggested" in the editor page, user ticks to add | adapt | 1 (step 11) |
| `fb-ad-intelligence-mcp` method: 50-result cap so narrow keywords first, hook reverse search + snowball, coverage audit (estimate %, never "100%") | `competitor_discovery.md`, Meta section of `platform_scraping.md` | adapt; drop its 6-subagent orchestration and its own HTML report (our orchestrator and report win) | 1 (step 11) |
| `fb-ad-intelligence-mcp` report ideas: Devil's Advocate section, winning hooks ranked by ad volume × days running | `comparison_method.md`, report page 2 | adapt | 1 (step 11) |
| `ad-copywriter/hook-library.md`: 15 hook types | `shared/frameworks/hooks.md` type list; `hook_analyzer` writes `hookType` in `hooks.json` | adapt (English labels, Chinese examples kept) | 1 (step 11) |
| `viral-sales-video-clone/scripts/download-and-prep.sh`: yt-dlp → ffmpeg frames → transcript | `transcribe.py` (Python rewrite for Windows), frames feed the visual hook | adapt | 1 (step 10) |
| `upt-ad-angle` rubrics: brutal evaluation (10 × 5), weak-idea kill filter, generic-output detector, evaluation + acceptance checklists | `content_creation/skills/angle_evaluation.md`, read by content_strategist and content_reviewer | copy (already English); UPT brand files and sample outputs dropped | 2 |
| `upt-ad-angle` compliance: Meta safe claims, finance safe claims, sensitive claims | `shared/platform_rules/meta.md`, `brand/_template/prohibited_claims.md` | adapt | 2 |
| `upt-ad-angle` eval cases (AI course, home custom, SME financing) | `content_creation/tests/angle_eval_cases/` | adapt, de-branded | 2 |
| `carousel-html` templates 01-11, `_base.css`, `render.py`, presets | `content_creation/skills/carousel_render/` | copy unchanged; client brand kits dropped | 3 |
| `carousel-html` SKILL, `design-rules.md`, max-chars table, `industry-recipes.md`, `content-ideas.md` | `carousel_generation.md`, `static_post_generation.md`; new `brand_kit.py` builds the kit from `brand/[project]/` | adapt; GPT-image-2 path replaced by nanobanana; missing `design-critic` check done by content_reviewer | 3 |
| `ad-copywriter`: SNICK.C checklist, 6-part long-form skeleton, CTA templates, Rojak style guide | `ad_copy_longform.md` (Meta ad copy), `cta.md`, a content_reviewer check | adapt; style guide is an example only (section 3) | 3 |
| `viral-sales-video-clone`: six-column shot list, UGC anti-slop rules, 5 required inputs | `reel_generation.md`, `agents/reel_creator.md` | adapt; "mirror 1:1" replaced by D10 | 3 |
| `higgsfield-script-to-video`: preflight cost, one sample shot, batch, stitch, pitfalls list | `reel_generation.md` video section | adapt, only if the Higgsfield connector is used | 3 |
| `lovart-sample-clone` idea: a good sample ad as the template + a text replacement table | `static_post_generation.md`, done with nanobanana edit | adapt idea only | 3 |
| `lovart-api`, `01portrait-ai-creator`, `course-setup-v2` installer, Groq / Lovart key setup | none | skip (duplicate service, off-scope, duplicates `installation-setup`) | - |

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
| UPT `viral-sales-video-clone` mirrors a viral video 1:1; our rule is "reuse the formula" | D10: keep its method (frames, transcript, shot list), drop the 1:1 rule |
| UPT angle rubric scores /50; content_reviewer scores /100 with fixed weights | Reviewer keeps /100; UPT checks become caps inside the categories (generic idea caps originality, risky claim caps brand) |
| `fb-ad-intelligence-mcp` runs its own 6 subagents and HTML report | Our orchestrator, agents and 2-page report win; only the search method is taken |
| Groq transcription (UPT) vs local `faster-whisper` (step 10) | `faster-whisper` default, Groq optional fallback |
| Lovart (UPT) vs nanobanana | nanobanana; Lovart skipped |
| UPT copy skills write Malaysian Chinese only | Market comes from `brand/[project]/`; the style rules apply only to that market |
| Census output path `100_Todo/drafts/...` | Candidates go to the source-manager page; only ticked rows enter `sources.md` |

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
| 1b | Stage the UPT bundle pieces from 6.4 as `_src_upt_*.md` (and assets/scripts) beside their destinations, with `source:` frontmatter; strip client data and personal paths | A search for UPT, Jayden, coachjayden and the client names finds nothing in the copies; `render.py` renders one preset slide unchanged |
| 8 | Later phases, one plan each, built in order 8a → 8d, using step 1 and 1b material | Separate plans per phase |
| 8a | Phase 2 strategy: content_strategist, campaign_planner, schedule_planner; `strategist_source` + `angle_evaluation.md` + compliance rules; one approval board | For `demo`: a strategy, campaign map and calendar presented and approved; every angle scored and weak ones killed |
| 8b | Phase 3 production: briefs (content_strategist), reel / carousel / static creators, content_reviewer; `carousel_render`, `ad_copy_longform.md`, shot list + anti-slop rules | One brief per format gives drafts and rendered carousel PNGs; reviewer scores /100; approval board sets `status: approved` and `publish_authorized: true` |
| 8c | Phase 5 performance loop: performance_analyst on Zernio analytics + `perf_build.py`; retrospective promotes lessons | A weekly snapshot for `demo` and at least one lesson proposed for approval |
| 8d | Phase 6 publishing: publishing_agent through Zernio | Needs social accounts connected in Zernio; one approved test post scheduled, never published on inference |
| 9 | Update `CLAUDE.md` (routing, folders, reusable-code table); user disables the duplicate plugin | `CLAUDE.md` matches the built system |
| 10 | Future: video transcription (see section 10). Download the video of each selected item (Meta direct URL; TikTok / IG via `yt-dlp`), extract audio and key frames with ffmpeg, transcribe locally, feed text and frames to `hook_analyzer` and the verdicts | A `transcribe.py` in the skill; the 12 Meta ads transcribed as the first test; verdicts say whether they used a transcript |
| 11 | Phase 1 upgrades from the UPT bundle: (a) hook types in `hooks.md` + `hookType` in `hooks.json`; (b) Devil's Advocate + winning-hooks-by-ad-volume in the comparison; (c) narrow-keyword + coverage rules for Meta; (d) `source-manager discover` (needs the Meta Ads connector) | Next `demo` run shows a hook type on every hook and a Devil's Advocate row; if the connector is on, a discover run suggests competitors with Page IDs and active-ad counts and ticked ones land in `sources.md` |

Recommended order from here: 1b → 11 (a-c) → 10 → 8a → 8b → 11 (d) when the Meta Ads connector is connected → 8c → 8d. Onboarding (deferred) must happen before 8a produces real strategy.

## 9. Risks
| Risk | Mitigation |
|---|---|
| XHS scrapers on Apify are community-built and less reliable | 2-item test pull before every full run; fallback actor listed in `platform_scraping.md`; failures logged to `_system` |
| Actor output fields change | Collector checks mapped fields on the test pull; missing fields stop the run with a clear message |
| Small samples (20-40 posts) give weak conclusions | `stats_rules.md`: "too early to call", never fabricate, quote post counts |
| Artifact cannot write to disk directly | Explicit sync step + automatic sync at run start + conflict check |
| Platform images expire | Download to `media/` at collection time, upload as artifact assets |
| Meta Ads connector needs a Facebook ad account the user may not have | Step 11(d) is optional; steps 11(a-c) do not depend on it |
| Other people's client data copied from the UPT bundle | Step 1b check: name search must come back empty before anything is committed |
| Carousel rendering needs Chrome; Chinese glyphs can render as boxes on Windows | `installation-setup` checks Chrome; first render is read back and checked for □ before use |
| Higgsfield and video generation cost credits | Preflight cost shown and one sample shot approved before any batch |
| UPT compliance rules are written for Malaysia (finance, health claims) | Kept as defaults in `meta.md`; brand onboarding confirms the market and adds local rules |

## 10. Progress checklist
- [x] Plan written and finalised (2026-10-31)
- [x] Step 1 sources copied (2026-10-31). Build scripts/templates byte-identical and start cleanly; the zips ship no sample data, so a build on sample data is deferred to step 5. Adapt-type sources are staged as `_src_*.md` beside their destination (`competitor-intelligence/references/`, `content_creation/skills/strategist_source|scriptwriting/`) and get rewritten in steps 2/5; `business-onboarding/references/` got brand/voice/platform/examples/interview_rules.
- [x] Step 2 shared foundations (2026-10-31). No stubs left in `shared/`. `stats_rules.md` now opens with a per-metric table of radar vs dashboard differences. Platform specs for Instagram/TikTok/LinkedIn/Meta/XHS are written from general knowledge; numeric limits marked "(verify)" need checking before first publish.
- [x] Step 3 memory layer (2026-10-31). Block formats in `memory/_template/*`; `memory/_system/` (README, changelog, skill_feedback/_format.md); `runs/index.md` + `runs/_run_template/` in the competitor_analysis template (copied by the unchanged `init_project.py`). `demo` project folders created in all six places.
- [x] Step 4 sources.md + source-manager (2026-10-31). `sources.md` template in `competitor_analysis/projects/_template/`; `source-manager` skill with `sources.py` (read/write/status/targets/build) and `sources_editor.html`. Tested on `demo`: file -> page build, simulated page edit in db -> `sources.md`, hand-edit conflict detected, `targets` honours Enabled + Active. Demo editor: https://claude.ai/artifact/PdLsCUVnbKJC4c7pFYrfMx. NOT yet tested: clicking add/remove/toggle in the live page (only the JS syntax and db path were checked).
- [x] Step 5 competitor-intelligence (2026-10-31), tested on fake fixtures only (no Apify yet). Built: SKILL.md, 8 reference files, scripts `run.py` (init/approve), `collect.py` (plan/check/media), `normalise.py` (build/tag/stats), `build_report.py` (select/build), `to_radar_tsv.py`, `to_perf_tsv.py`, `report_template.html`. Verified on fixtures: all 4 platforms normalise, radar adapter output builds with unchanged `radar_build.py`, report builds and renders (27 cards, 8 comparison rows, no overflow), approve is idempotent-safe. Fixture run deleted afterwards. Deviations from plan: analysis files are JSON (`verdicts.json`, `ours.json`, `comparison.json`), not `.md`; page 3 radar is a separate linked artifact, not an in-report tab; `collect.py` prepares inputs/checks, Apify is called via MCP (no REST/token code); the two dashboard scripts' template path lines were edited to the new asset names. Not verified: real actor field names (Meta/XHS are guesses, XHS actor not chosen), `to_perf_tsv.py` end to end (fixtures had no Ours TikTok), the approval flow clicked in the live artifact, `media` download on real URLs. Test report artifact (fixture data): https://claude.ai/artifact/HrMxvY22LFPKQowiHWWuyM
- [x] Step 6 Phase 1 agents (2026-10-31). orchestrator, competitor_researcher, competitor_analyzer, hook_analyzer, performance_analyst, insight_synthesizer now `status: active` with inputs, outputs, method files and stop conditions; no TODO left in them. Also filled the four methodology files they read (`content_scoring`, `hook_analysis`, `performance_analysis`, `pattern_detection`); `hooks.json` added to `output_schema.md`. Agents were checked by path scan only, never run as subagents; the other 8 agents in `agents/` remain stubs (later phases).
- [x] Step 7 end-to-end test (2026-10-31), project `demo`, run `2026-10-31_1534`: 12 real Malaysian landed-property accounts (3 per platform), 191 items, 57-card report approved in the live artifact (https://claude.ai/artifact/P4UntJqoJawWjd5ohmmqx9), lessons PAT-001, PAT-002, FAIL-001 in `memory/demo/`, findings FB-001 to FB-008 in `memory/_system/`. Confirmed on live data: actor field names for Instagram, TikTok, Meta (ads) and XHS (`zen-studio/rednote-user-profile-scraper`, one profile per call on the free tier); `media` download (44 of 44 images); approval flow. NOT covered: no Ours accounts, so `to_perf_tsv.py` and the us-vs-them baseline were not exercised; no user override was recorded, so recalibration of `verdict_rules.md` has no data yet; hooks were read from captions only, not from video; the Instagram/TikTok pulls hit the 30-post cap.
- [x] UPT bundle reviewed and merge map written (2026-10-31): section 6.4, D9-D10, new defaults, conflicts, risks; steps 1b, 8a-8d and 11 added. Workflow diagram published (`docs/diagrams/agent-workflow.html`).
- [x] Step 1b stage UPT bundle pieces (2026-10-31). 52 files staged and uncommitted: 33 text files as `_src_upt_*.md` (frontmatter `source`, `copied`, `status: staged`, `destination`; original skill frontmatter dropped) beside their destinations, plus `carousel_render/` (11 templates, `_base.css`, `_template.json` + 5 presets byte-identical; `render.py` with 5 text edits and 1 fix: UTF-8 stdout, because it crashed on Windows consoles). Names and paths scrubbed to `[brand]`, `[owner]`, `[client]`, `[creator-handle]` and project paths; the name search finds only the provenance lines (`source:` / `original-skill:`). Checked: no phone numbers, emails or keys; 6 URLs (Groq, Lovart, Facebook, Google), all documentation examples. Test render of 2 slides with the `modern-minimal` preset in Windows Chrome: both PNGs correct, Chinese text renders without boxes. Skipped on purpose: UPT brand files (`upt-marketing`, `offer-positioning`, `language-style`), sample outputs, golden/bad examples, `ad-copywriter/_prompt.md`, client brand kits, creator templates, `gpt-image2-path.md`, `lovart-api`, `01portrait-ai-creator`, installer scripts. NOT done: the staged text is scrubbed, not adapted or translated; Chinese remains in the staged files and many still mention `/ugc-ad-ref`, `/creative-director`, `/course-setup-v2` (dead references until rewritten in 8a/8b). `_src_upt_download_and_prep.sh.txt` is a reference copy and must not be run.
- [x] Step 11 Phase 1 upgrades from the UPT bundle (2026-10-31), built and tested on a scratch copy of the `demo` run plus the offline smoke test (passes). NOT tested live: no real run has used the new fields yet, and no discovery search was run. Details:
  - (a) hook types: 15 types + `other` added to `shared/frameworks/hooks.md` ("Hook types"); `hookType` added to `hooks.json` and `verdicts.json` (schema, `hook_analysis.md`, `hook_analyzer`, `competitor_analyzer`); `build_report.py` warns when a hook has no type or an unknown one; the report shows a type badge on each card.
  - (b) `build_report.py winning <run>` ranks Meta ads by copies x days running into `analysis/winning_ads.json` (checked on the real demo run: 9 ad texts ranked); `comparison.json` gets optional `winningHooks` and `devilsAdvocate`, with method in `comparison_method.md`, writing steps in `insight_synthesizer`, and two new report sections. Old runs still build (warning only). Note: the demo run's `items.tsv` predates the `runningDays` / `variants` columns, so it needs `normalise.py build` again before `winning` works on it.
  - (c) Meta search rules (narrow keywords first, partial vs complete, hook reverse search, coverage audit, "never 100%") in `platform_scraping.md`; coverage statement rule in `comparison_method.md`.
  - (d) `source-manager/references/competitor_discovery.md` (two query routes: Meta Ads connector, or Apify keyword URL, so the connector is not required); `sources.py suggest` adds candidates as Competitors > Meta rows with Active = no (tested: duplicates skipped, hand-edit refused, suggestions not returned by `targets`). The editor page needed no change. Also fixed: `sources.py` crashed printing Chinese names on a Windows console.
  - Still open for a real run: have `hook_analyzer` and `insight_synthesizer` actually write the new fields; try one discovery on `demo` (small test first, log the actor's real result count in `_system`).
- [ ] Step 8 later phases: [ ] 8a strategy [ ] 8b production [ ] 8c performance [ ] 8d publishing
- [ ] Step 10 (future, added 2026-10-31 at the user's request): video transcription. Today hooks and verdicts use captions and cover images only, so `spoken` and `audio` in `hooks.json` are "not visible from the data". Findings so far: 12 of 13 Meta ads in the demo run carry direct video URLs (`snapshot.videos[].videoHdUrl` / `videoSdUrl`); the TikTok actor returns no download links (`mediaUrls` empty, so the video download option or a downloader actor is needed, which costs Apify credits); Instagram returns post links and cover images only. ffmpeg is installed; no speech-to-text library is. Chosen engine: `faster-whisper` run locally (free, one-off model download, handles mixed Chinese/Malay/English better with a larger model). Wispr Flow is dictation by microphone and is not a fit. Alternatives if needed: an Apify transcription actor, the NotebookLM connector (untested), a hosted API (needs a key). Plan: (1) `transcribe.py` writes `media/<itemId>.txt`; (2) test on the 12 Meta ads, then about 5 top TikToks; (3) `hook_analyzer` and `verdict_rules.md` read the transcript when it exists and the report marks which verdicts used one, otherwise confidence stays capped at medium; (4) add the library to `pyproject.toml` and the changelog. Transcribe only the selected items (about 57 of 191) to keep cost down.
- [~] Step 9 CLAUDE.md + plugin cleanup (2026-10-31): `CLAUDE.md` updated (first-run rule, routing, memory/_system, reusable-code table). STILL OPEN, user action: disable the global `social-media-automation` plugin and the standalone `competitor-content-radar` / `content-performance-dashboard` skills so they do not compete with the project skills. Step 8 also open (step 7 done).

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
6. Later: video transcription (step 10); business onboarding / brand guideline (deferred by the user); verify the "(verify)" platform limits in `shared/platform_rules/`.
7. Leftovers: fixture test report artifact (https://claude.ai/artifact/HrMxvY22LFPKQowiHWWuyM) can be deleted on request; demo editor artifact (https://claude.ai/artifact/PdLsCUVnbKJC4c7pFYrfMx) holds stale test data in its db until the real sources are synced.

**Verification 2026-10-31 (session 2)**
- On disk: steps 1-6 confirmed (6 Phase 1 agents active, no stubs in `shared/`, all skill scripts compile).
- Step 9 plugin cleanup appears done: no `social-media-automation` / radar / dashboard skills load in this session.
- Apify: the claude.ai Apify connector answers (FREE tier); step 7 now waits only on real URLs. XHS actor candidates: `zhorex/rednote-xiaohongshu-scraper` (profile URLs), `socialdatax/socialdatax-xhs-data-api`.
- Zernio: connected, one `Default` profile, **no social accounts connected**.
- Gaps (fixed same day): the 3 stub method files in `competitor_analysis/skills/` and 5 stub templates in `competitor_analysis/templates/` are now `status: active` pointer files to the competitor-intelligence references (kept so the scaffold does not recreate them). `_src_radar_SKILL.md` / `_src_perf_SKILL.md` were rewritten as `references/radar_dashboard.md` and `references/perf_dashboard.md` (paths adapted to `uv run`, the adapters and `runs/<id>/`) and the staged copies removed. The two `_src_*` files in `content_creation/skills/` stay for step 8.
- `2026-10-31_setup-from-scratch.md`: being reworked in another session (now a 7-item, `setup.py`-based checklist); none ticked when checked.

**Update 2026-10-31 (session 3): UPT bundle merged into this plan**
- Steps 1b and 11 done. Next work: step 10 (transcription), then a first real run using the new fields and a small discovery test on `demo`. Phase 2 (8a) waits on brand onboarding.
- New user actions: connect the Meta Ads connector only if step 11(d) is wanted (needs a Facebook ad account); install Chrome if missing (carousel rendering); `yt-dlp` gets added to `installation-setup` with step 10.
- The unpacked bundle is in the session scratchpad only; step 1b copies from the original `.skill` file in Downloads.
