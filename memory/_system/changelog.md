---
type: memory
status: active
kind: changelog
---
# Skill changelog
Approved edits to skills and reference files. Newest first. Only add a line after the user approved the edit.

| Date | File | Change | Reason (FB ids) | Approved by |
|---|---|---|---|---|
| 2026-11-01 | content_creation/skills/{angle_evaluation,content_strategy,carousel_generation,carousel_recipes,ad_copy_longform,reel_generation,static_post_generation}.md, templates/{content_strategy,content_brief,reel,static_post}.md, tests/angle_eval_cases/*, shared/platform_rules/meta.md, shared/frameworks/cta.md, brand/_template/prohibited_claims.md | UPT staged methods rewritten in English as project methods (angle kill filter and /50 scorecard, claims rules, carousel design rules and audit, long-form copy skeleton, reel plan with keep/replace/drop instead of 1:1 mirror, layout-replace image method with nanobanana); 28 staged `_src_upt_*` files deleted | plan step 8a/8b skill transformation (docs/plans/2026-10-31_remaining-work.md section 6) | user ("execute the skill transformation first") |
| 2026-10-31 | competitor-intelligence/scripts/collect.py | Meta input drops `activeStatus`; XHS actor `zen-studio/rednote-user-profile-scraper` with `profileUrls`/`includeNotes`/`maxNotesPerProfile`; `check` expands XHS notes | FB-001, FB-002 | user (XHS parser approved in chat; the rest reported in chat) |
| 2026-10-31 | competitor-intelligence/scripts/normalise.py | negative counts become empty; `expand_xhs` and XHS field map; Meta ads match on the Facebook page link; non-Latin names use the profile id as accountId | FB-002, FB-003, FB-006 | user (XHS parser approved in chat; the rest reported in chat) |
| 2026-10-31 | competitor-intelligence/references/platform_scraping.md | Meta and XHS rows confirmed against live runs; Meta discovery URL added | FB-001, FB-002 | user (reported in chat) |
| 2026-10-31 | competitor-intelligence/scripts/normalise.py, references/output_schema.md | items.tsv gains runningDays, isActive, variants (Meta ads); durationSec 0 stored empty; Instagram comment 0 caveat; tags.tsv format documented | FB-009 (1, 2, 3) | user ("Apply top 5") |
| 2026-10-31 | competitor-intelligence/scripts/build_report.py, references/selection.md | select adds up to 2 no-view posts per account when room remains, and never drops an anomaly under the cap | FB-009 (4) | user ("Apply top 5") |
| 2026-10-31 | references/verdict_rules.md, competitor_analysis/skills/content_scoring.md, pattern_detection.md, memory/_template/*.md, agents/competitor_analyzer.md | one confidence rule (low under 5, medium 5 to 14, high 15+ with a second run or own validation; one run caps at medium); scored posts need a view count; analyzer may write tags.tsv | FB-009 (3, 5) | user ("Apply top 5") |
| 2026-10-31 | references/verdict_rules.md | duplicate or re-run ads count as one idea; new check for sponsored posts (reach may be bought, confidence at most medium, never Copy on reach alone) | FB-009 (7, 10) | user (approved in chat: "proceed FB009") |
| 2026-10-31 | competitor-intelligence/scripts/normalise.py, references/output_schema.md, SKILL.md, agents/competitor_analyzer.md | items.tsv gains `sponsored`; tags.tsv takes an optional 4th column (yes or empty, anything else stops); sponsored posts are tagged by what they show, never off_topic for being paid | FB-009 (10) | user (approved in chat: "proceed FB009") |
| 2026-10-31 | agents/insight_synthesizer.md, agents/competitor_researcher.md, references/comparison_method.md | synthesizer reads sources.md; researcher gets the exact sources.py command; topic coverage is no longer a separate output (stated inside a strategy item or the headline) | FB-009 (6, 9) | user (approved in chat: "proceed FB009"; step 6 dropped as recommended) |
| 2026-10-31 | shared/frameworks/stats_rules.md, new stats_maintenance.md, writing_insights.md, writing_guide.md, perf/radar_dashboard.md, agents/performance_analyst.md | dashboard maintenance notes moved to stats_maintenance.md; stats_rules keeps the plain-language rules; writing_insights drops emoji and the banned term "outlier score" | FB-009 (8) | user (approved in chat: "proceed FB009") |
