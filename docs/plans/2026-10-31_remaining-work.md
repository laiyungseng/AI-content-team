---
type: plan
status: in-progress      # final -> in-progress -> done
created: 2026-10-31
last-updated: 2026-10-31
owner: user
related: [[CLAUDE]], [[2026-10-31_setup-from-scratch]]
---
# Plan: AI Content Team, what is built and what is left

The single plan for the project. It replaces `2026-10-31_architecture-and-skill-merge.md` (removed; its history is in git, last at commit `9ca8259`). Every session reads this first and ticks section 11 as work lands. The separate install plan is `2026-10-31_setup-from-scratch.md`.

The agent-by-agent workflow with tools and human checkpoints is drawn in `docs/diagrams/agent-workflow.html` (https://claude.ai/artifact/5VYzVNaxHczm7hZTy3gPn2).

## 1. Goal and scope
A multi-agent content system that works as a continuous learning loop (see [[CLAUDE]]): **Intelligence** (research, analysis, insight) feeds **Production** (strategy, content, publishing), and measured results feed back into memory.

- **Built and tested:** Phase 1, the competitor-intelligence pipeline, on a memory and self-improvement layer. Plus method staged from four external sources (competitor-content-radar, content-performance-dashboard, the social-media-automation plugin, the UPT course bundle).
- **Left:** transcription (step 10), brand onboarding (step 0), Phase 2 strategy, Phase 3 production, Phase 5 performance loop, Phase 6 publishing, and a first real run using the newest fields.

## 2. Decisions (locked)
| # | Decision |
|---|---|
| D1 | Brand onboarding is deferred. The workflow was built and tested on a dummy project (`demo`) first. It must happen before Phase 2. |
| D2 | Two pipelines under one orchestrator: **Intelligence** and **Production**. Production is blocked until an approved intelligence run exists. |
| D3 | All target URLs live in `sources.md` (a table per platform, Competitors and Ours, per-platform Enabled switch, per-URL Active status). Research reads nothing else. |
| D4 | `source-manager` shows and edits `sources.md` through an artifact; edits are synced back into the file. Discovery only suggests rows (Active = no); the user ticks Active. |
| D5 | Research output is a 2-page artifact: scraped items sorted Adapt / Copy / Ignore, and an us-vs-them comparison with strategy and positioning. |
| D6 | Approved reports are saved as dated, never-overwritten run records. |
| D7 | Memory holds validated lessons only. A system-level memory plus a retrospective improves the skills; every skill edit needs user approval. |
| D8 | External skills are merged by copying method files, keeping tested scripts and templates unchanged, and adapting only paths, names and rules. |
| D9 | The UPT bundle is merged by method only: its installer is never run, client data and personal paths are stripped, Lovart is not adopted (nanobanana covers images). |
| D10 | Competitor material is never cloned 1:1: extract the reusable formula, never copy claims, footage, music or text. |

## 3. Defaults (hold unless the user changes them; change here, not in code)
| Question | Default |
|---|---|
| Test project | `demo` (folders only, no brand interview) |
| Collected per platform | Meta = Ad Library ads; Instagram, TikTok, XHS = organic posts |
| Collection tool | Apify for all platforms (authorised through the claude.ai connector) |
| Window / volume | 90 days, 30 posts per account (20 for XHS) |
| Competitor discovery | Meta Ads connector (`ads_library_search`) or the Apify Ad Library keyword URL, whichever is available |
| Carousel / static rendering | `carousel_render` HTML templates rendered by headless Chrome to 1080x1350 PNG |
| Image generation | nanobanana; Higgsfield optional for video; Lovart not used |
| Video download for hooks | Meta ads: direct video URL from the actor. TikTok / Instagram: `yt-dlp` first, an Apify downloader only if it fails |
| Transcription | `faster-whisper` locally; Groq Whisper an optional fallback that needs a key |
| Strategy mix | 70% proven / 20% adjacent / 10% experimental, and every post tagged Educate / Engage / Promote |
| Market-specific copy rules | Apply the UPT Malaysian-Chinese style only when `brand/[project]/` names that market |

## 4. Where the design lives (not repeated here)
| Topic | File |
|---|---|
| `sources.md` format, editor sync | `.claude/skills/source-manager/SKILL.md`, `competitor_analysis/projects/_template/sources.md` |
| One intelligence run, steps, approval | `.claude/skills/competitor-intelligence/SKILL.md` |
| `items.tsv`, analysis JSON schemas | `.claude/skills/competitor-intelligence/references/output_schema.md` |
| Report pages | `competitor-intelligence/assets/report_template.html`, `build_report.py` |
| Statistics rules | `shared/frameworks/stats_rules.md` |
| Memory layers, retrospective, skill edits | `memory/_system/README.md` |
| Agents, inputs, outputs | `agents/*.md` |

## 5. Built so far (all merged; PR #1 to #3)
- Shared foundations (`shared/`), memory layer, `demo` project folders.
- `source-manager` (editor page, `sources.py` with `suggest`), `competitor-intelligence` (collect, normalise, select, winning, build, approve), six Phase 1 agents active.
- End-to-end test on `demo`, run `2026-10-31_1534`: 12 real Malaysian landed-property accounts, 191 items, 57-card report approved in the live artifact, lessons PAT-001, PAT-002, FAIL-001 in `memory/demo/`, findings FB-001 to FB-008 in `memory/_system/`.
- Step 1b: 32 UPT text files staged as `_src_upt_*.md`, plus the working carousel renderer (`content_creation/skills/carousel_render/`).
- Step 11: hook types, winning hooks, Devil's Advocate, Meta search rules, competitor discovery method and `sources.py suggest`. Tested on a scratch copy of `demo` and the offline smoke test; not yet used in a real run.
- `CLAUDE.md` updated; workflow diagram published.

**Known gaps**
- No Ours accounts in `demo`, so `to_perf_tsv.py` and the us-vs-them baseline were never exercised.
- No user override recorded yet, so `verdict_rules.md` has no data to recalibrate from.
- Hooks are read from captions and cover images only (step 10 fixes this).
- Instagram and TikTok pulls hit the 30-post cap.
- Add / remove / toggle clicks in the live source editor were never tested (only the JS and db path).
- Numeric platform limits marked "(verify)" in `shared/platform_rules/` are unchecked.
- Zernio is connected with one `Default` profile and no social accounts.

## 6. Is the UPT skill transformation done?
**Methods: yes (2026-11-01). Agents and one script: no.** The 28 staged text files for Phase 2 and 3 were rewritten in English into project methods and deleted. Only `download_and_prep.sh.txt` (step 10) is still staged. The 3 Phase 1 adapted originals stay until R1 confirms them. The methods are written but untested in a real run, and the agent files still need filling.

| State | Meaning | Count |
|---|---|---|
| Adapted in Phase 1 | Method in the project; original kept until R1 | 3 |
| Adapted 2026-11-01 | Rewritten in English, staged original deleted, logged in `memory/_system/changelog.md`; not yet used in a real run | 28 |
| Still staged | `download_and_prep.sh.txt`, waits for step 10 | 1 |
| Usable as copied | Carousel templates, presets and `render.py` | 19 files |

| Staged file | Became | State |
|---|---|---|
| `fb_competitor_census` | `source-manager/references/competitor_discovery.md` + `sources.py suggest` | Adapted, original kept |
| `fb_ad_intelligence` | Meta rules in `platform_scraping.md`; winning hooks and Devil's Advocate in `comparison_method.md` | Adapted, original kept |
| `hook_library` | `shared/frameworks/hooks.md`, `hookType` in `hooks.json` | Adapted, original kept |
| `download_and_prep.sh.txt` | `competitor-intelligence/scripts/transcribe.py` | Staged (step 10) |
| `ad_angle_SKILL`, `brutal_evaluation`, `weak_idea_kill_filter`, `generic_output_detector`, `evaluation_checklist` | `content_creation/skills/angle_evaluation.md` | Done |
| `acceptance_checklist`, 3 `eval_case_*` | `content_creation/tests/angle_eval_cases/` (README + 3 de-branded cases) | Done |
| `output_format_template`, `input_brief_template` | `templates/content_strategy.md`, `templates/content_brief.md`; process in `skills/content_strategy.md` | Done |
| `meta_ads_safe_claims`, `finance_ads_safe_claims`, `sensitive_claims` | `shared/platform_rules/meta.md` (safe claims), `brand/_template/prohibited_claims.md` | Done |
| `carousel_SKILL`, 3 `docs/_src_upt_*` | `skills/carousel_generation.md`, `carousel_recipes.md` | Done |
| `ad_copywriter_SKILL`, `framework`, `snickc_checklist`, `style_guide` | `skills/ad_copy_longform.md`; CTA block in `shared/frameworks/cta.md`; style guide kept as a market example inside it | Done |
| `viral_video_clone_SKILL`, `ugc_anti_slop_rules`, `seedance_prompt_formula`, `shot_list_template`, `higgsfield_script_to_video` | `skills/reel_generation.md`, `templates/reel.md` (1:1 mirror dropped, D10) | Done |
| `sample_clone` | `skills/static_post_generation.md`, `templates/static_post.md` (nanobanana) | Done |

Still to do for the transformation: `brand_kit.py` (builds a carousel kit from `brand/[project]/`), filling the agent files (`content_strategist`, `campaign_planner`, `schedule_planner`, the three creators, `content_reviewer`) so they read these methods, and `content_reviewer`'s /100 rubric in `skills/content_review.md`. The English filler-phrase list and the Malaysian-Chinese style notes are examples; per-brand wording goes in `brand/[project]/brand_voice.md`.

Two staged-source copies remain for Phase 2 and 3: `content_creation/skills/strategist_source/` and `scriptwriting/` (from the social-media-automation plugin).

## 7. Remaining steps
| Step | Work | Done when | Needs |
|---|---|---|---|
| R1 | Real run on `demo` with the new fields: `normalise.py build` again (old `items.tsv` lacks `runningDays` / `variants`), agents write `hookType`, `winningHooks`, `devilsAdvocate`; approve in the live report | Approved run shows hook-type badges, a winning-hooks table and a Devil's Advocate section; any override logged in `_system` | Apify authorised |
| R2 | Small discovery test on `demo` (Meta connector or Apify keyword URL) | `candidates.json` produced; `suggest` adds rows; real result count per search logged in `_system`; method doc corrected if reality differs | Apify or Meta Ads connector |
| 10 | Video transcription: `transcribe.py` (Meta direct URL; TikTok / Instagram via `yt-dlp`), audio and key frames with ffmpeg, local `faster-whisper`; `hook_analyzer` and `verdict_rules.md` read the transcript (confidence stays capped at medium without one); add `yt-dlp` to `installation-setup`; transcribe only the selected items (about 57 of 191) | The 12 Meta ads in `demo` transcribed; verdicts say whether they used a transcript | ffmpeg (installed), `faster-whisper` model download |
| 0 | **Brand onboarding** (deferred): `business-onboarding` interview, brand guideline approved | `brand/<project>/` filled and approved | You, about one session |
| 8a | Phase 2 strategy: fill `content_strategist`, `campaign_planner`, `schedule_planner`; add `angle_evaluation.md`, compliance rules, strategy approval board | For `demo`: strategy, campaign map and calendar approved; every angle scored, weak ones killed | Step 0 and an approved intelligence run |
| 8b | Phase 3 production: briefs, `reel_creator`, `carousel_creator`, `static_content_creator`, `content_reviewer`; `brand_kit.py`; ad-copy and shot-list methods | One brief per format gives a draft and a rendered carousel; reviewer scores /100; approval board sets `status: approved` and `publish_authorized: true` | 8a, Chrome, nanobanana |
| 8c | Phase 5 performance loop: `performance_analyst` on Zernio analytics and `perf_build.py`; retrospective promotes lessons | Weekly snapshot for `demo` and one lesson proposed for approval | Zernio accounts connected, published content |
| 8d | Phase 6 publishing: `publishing_agent` through Zernio | One approved test post scheduled; never published on inference | Social accounts connected in Zernio |

Order: R1 → R2 → 10 → step 0 → 8a → 8b → 8c → 8d. R1 and R2 can run any time; step 0 must come before 8a. Each of 8a to 8d gets its own short plan file when it starts.

## 8. Conflicts and resolutions still relevant
| Conflict | Resolution |
|---|---|
| Topics (4-6, competitors) vs pillars (max 3, ours) | Competitors: shared topics. Ours: topic and pillar both recorded |
| Intent mix 50/20/30 (Educate / Engage / Promote) vs 70/20/10 (proven / adjacent / experimental) | Different axes; both kept, every planned post gets both tags |
| Dashboards support Instagram and TikTok only | Collector also pulls Meta and XHS; dashboards show IG / TikTok until extended |
| UPT `viral-sales-video-clone` mirrors a viral video 1:1 | D10: keep the method (frames, transcript, shot list), drop the 1:1 rule |
| UPT angle rubric scores /50; `content_reviewer` scores /100 | Reviewer keeps /100; UPT checks become caps inside its categories (generic idea caps originality, risky claim caps brand) |
| `fb-ad-intelligence-mcp` runs its own subagents and HTML report | Our orchestrator, agents and 2-page report win; only the search method was taken |
| Groq transcription (UPT) vs local `faster-whisper` | `faster-whisper` default, Groq optional fallback |
| UPT copy skills write Malaysian Chinese only | Market comes from `brand/[project]/` |

## 9. Open user actions
- Brand onboarding session (step 0), and your real competitor and own URLs (`demo` uses placeholders).
- Connect social accounts in Zernio before 8c and 8d.
- Connect the Meta Ads connector only if you want it for R2; the Apify route works without it.
- Check that the global `social-media-automation` plugin and standalone radar / dashboard skills no longer load (looked done on 2026-10-31).
- Verify the "(verify)" platform limits before the first publish.
- Leftover test artifacts you may delete: the fixture report https://claude.ai/artifact/HrMxvY22LFPKQowiHWWuyM, and the demo editor https://claude.ai/artifact/PdLsCUVnbKJC4c7pFYrfMx (stale test data until real sources are synced).

## 10. Risks
| Risk | Mitigation |
|---|---|
| XHS scrapers on Apify are community-built and less reliable | 2-item test pull before every full run; fallback actors listed in `platform_scraping.md`; failures logged to `_system` |
| Actor output fields change | The collector checks mapped fields on the test pull; missing fields stop the run |
| Small samples (20-40 posts) give weak conclusions | `stats_rules.md`: "too early to call", quote post counts |
| Artifact cannot write to disk directly | Explicit sync step, automatic sync at run start, conflict check |
| New fields exist only in method and tests, not in a real run | R1 comes first and gates trust in step 11 |
| Strategy built before onboarding would be generic | 8a is blocked until step 0 is done |
| Staged files mistaken for finished methods | Tracker in section 6; delete each staged file when adapted |
| Staged Chinese text and market rules are specific to one Malaysian agency | Rewrite in English; market rules apply only when the brand names that market |
| Carousel rendering needs Chrome; Chinese glyphs can show as boxes | `installation-setup` checks Chrome; first render is read back and checked |
| Higgsfield and video generation cost credits | Preflight cost shown and one sample shot approved before any batch |
| Meta Ads connector needs a Facebook ad account | Discovery works through Apify without it |

## 11. Progress checklist
- [x] Steps 1-7: sources copied, shared foundations, memory layer, source-manager, competitor-intelligence, Phase 1 agents, end-to-end test on `demo` (2026-10-31)
- [x] Step 9: `CLAUDE.md` updated; duplicate plugin cleanup looked done
- [x] Step 1b: UPT bundle staged (PR #3)
- [x] Step 11: hook types, winning hooks, Devil's Advocate, Meta search rules, discovery (PR #3)
- [ ] R1 real run on `demo` with the new fields
- [ ] R2 small discovery test
- [ ] Step 10 video transcription
- [ ] Step 0 brand onboarding
- [x] Skill transformation of the staged UPT methods (2026-11-01): methods written, agents, `brand_kit.py` and `content_review.md` still open
- [ ] 8a strategy · [ ] 8b production · [ ] 8c performance · [ ] 8d publishing
