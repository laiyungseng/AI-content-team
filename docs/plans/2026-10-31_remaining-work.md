---
type: plan
status: in-progress
created: 2026-10-31
last-updated: 2026-10-31
owner: user
related: [[2026-10-31_architecture-and-skill-merge]], [[CLAUDE]]
---
# Remaining work (after PR #3)

Everything still to do, in one place. The full design, decisions and history stay in `2026-10-31_architecture-and-skill-merge.md`; tick items there and here as they land.

## 1. Is the UPT skill transformation done?
**No, only the Phase 1 part is.** 32 text files were staged from the UPT bundle as `_src_upt_*.md`. Three have been rewritten into project methods; 29 are still raw staged copies waiting for Phase 2 and 3, which cannot start until the brand onboarding is done (strategy and content need a brand guideline).

| State | Meaning | Count |
|---|---|---|
| Adapted | Method rewritten into the project, tested on a scratch copy of `demo`, not yet used in a real run | 3 |
| Staged | Cleaned of client names and paths only; still Chinese, still points to tools we do not have | 29 |
| Usable as copied | Carousel templates, presets and `render.py` (rendered a test slide in Windows Chrome) | 19 files |

## 2. Transformation tracker
| Staged file (`_src_upt_*`) | Becomes | State | Step |
|---|---|---|---|
| `fb_competitor_census` | `source-manager/references/competitor_discovery.md` + `sources.py suggest` | Adapted | 11d |
| `fb_ad_intelligence` | Meta rules in `platform_scraping.md`, winning hooks + Devil's Advocate in `comparison_method.md` and the report | Adapted | 11b, 11c |
| `hook_library` | Hook types in `shared/frameworks/hooks.md`, `hookType` in `hooks.json` | Adapted | 11a |
| `download_and_prep.sh.txt` | `competitor-intelligence/scripts/transcribe.py` (Python, Windows-safe) | Staged | 10 |
| `ad_angle_SKILL`, `brutal_evaluation`, `weak_idea_kill_filter`, `generic_output_detector` | `content_creation/skills/angle_evaluation.md`, read by `content_strategist` and `content_reviewer` | Staged | 8a |
| `evaluation_checklist`, `acceptance_checklist` | `content_reviewer` checks | Staged | 8a / 8b |
| `output_format_template`, `input_brief_template` | `content_creation/templates/content_strategy.md`, `content_brief.md` | Staged | 8a |
| 3 `eval_case_*` | `content_creation/tests/angle_eval_cases/`, de-branded | Staged | 8a |
| `meta_ads_safe_claims`, `finance_ads_safe_claims`, `sensitive_claims` | `shared/platform_rules/meta.md`, `brand/_template/prohibited_claims.md` | Staged | 8a |
| `carousel_SKILL`, 3 `docs/_src_upt_*` | `carousel_generation.md`, `static_post_generation.md`; new `brand_kit.py` builds a kit from `brand/[project]/` | Staged | 8b |
| `ad_copywriter_SKILL`, `framework`, `snickc_checklist`, `style_guide` | `ad_copy_longform.md`, `shared/frameworks/cta.md`, a `content_reviewer` check; style guide is a market example only | Staged | 8b |
| `viral_video_clone_SKILL`, `ugc_anti_slop_rules`, `seedance_prompt_formula`, `shot_list_template` | `reel_generation.md`, `reel_creator`; drop the "mirror 1:1" rule (D10) | Staged | 8b |
| `higgsfield_script_to_video` | video section of `reel_generation.md`, only if Higgsfield is used | Staged | 8b |
| `sample_clone` | `static_post_generation.md` (idea only, done with nanobanana) | Staged | 8b |

Rule for each row when it is adapted: rewrite in English, remove references to tools we do not have (`/ugc-ad-ref`, `/creative-director`, `/course-setup-v2`, Lovart), then **delete the staged file** and log it in `memory/_system/changelog.md`. Not yet applied to the 3 adapted files: their staged originals are still in the repo as reference and can be deleted once the first real run confirms the new methods.

## 3. Remaining steps
| Step | Work | Done when | Needs |
|---|---|---|---|
| R1 | Real run on `demo` with the new fields: `normalise.py build` again (old `items.tsv` lacks `runningDays` / `variants`), agents write `hookType`, `winningHooks`, `devilsAdvocate`; approve in the live report | Approved run shows hook-type badges, a winning-hooks table and a Devil's Advocate section; any override logged in `_system` | Apify authorised |
| R2 | Small discovery test on `demo` (Meta connector or Apify keyword URL) | `candidates.json` produced; `suggest` adds rows; real result count per search logged in `_system`; method doc corrected if reality differs | Apify or Meta Ads connector |
| 10 | Video transcription: `transcribe.py` (Meta direct URL; TikTok / Instagram via `yt-dlp`), audio + key frames with ffmpeg, local `faster-whisper`; `hook_analyzer` and `verdict_rules.md` read the transcript; add `yt-dlp` to `installation-setup` | The 12 Meta ads in `demo` transcribed; verdicts say whether they used a transcript | ffmpeg (installed), `faster-whisper` download |
| 0 | **Brand onboarding** (deferred): `business-onboarding` interview, brand guideline approved | `brand/<project>/` filled and approved | You, about one session |
| 8a | Phase 2 strategy: fill `content_strategist`, `campaign_planner`, `schedule_planner`; add `angle_evaluation.md`, compliance rules, strategy approval board | For `demo`: strategy, campaign map and calendar approved; every angle scored, weak ones killed | Step 0 and an approved intelligence run |
| 8b | Phase 3 production: briefs, `reel_creator`, `carousel_creator`, `static_content_creator`, `content_reviewer`; `brand_kit.py`; ad-copy and shot-list methods | One brief per format gives a draft and a rendered carousel; reviewer scores /100; approval board sets `status: approved` and `publish_authorized: true` | 8a, Chrome, nanobanana |
| 8c | Phase 5 performance loop: `performance_analyst` on Zernio analytics + `perf_build.py`; retrospective promotes lessons | Weekly snapshot for `demo` and one lesson proposed for approval | Zernio accounts connected, published content |
| 8d | Phase 6 publishing: `publishing_agent` through Zernio | One approved test post scheduled; never published on inference | Social accounts connected in Zernio |

Order: R1 → R2 → 10 → step 0 → 8a → 8b → 8c → 8d. R1 and R2 can run any time; step 0 must come before 8a.

## 4. Open user actions
- Brand onboarding session (step 0) and your real competitor and own URLs (the `demo` project uses placeholders).
- Connect social accounts in Zernio (none connected yet) before 8c and 8d.
- Connect the Meta Ads connector only if you want it for R2; the Apify route works without it.
- Disable the global `social-media-automation` plugin and the standalone radar / dashboard skills if they still load (plan step 9; looked done on 2026-10-31).
- Verify the numeric limits marked "(verify)" in `shared/platform_rules/` before the first publish.
- Decide whether to delete the leftover test artifacts (fixture report, demo editor) listed in section 11 of the main plan.

## 5. Risks specific to what is left
| Risk | Mitigation |
|---|---|
| Staged files are Chinese, written for one Malaysian-Chinese agency | Rewrite in English; market rules apply only when `brand/<project>/` names that market |
| New fields exist only in method and tests, not in a real run | R1 comes first and is the gate for trusting steps 11a-b |
| Strategy built before onboarding would be generic | 8a is blocked until step 0 is done |
| Many staged files left in the repo are mistaken for finished methods | Tracker above; delete each staged file when adapted |
