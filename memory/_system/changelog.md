---
type: memory
status: active
kind: changelog
---
# Skill changelog
Approved edits to skills and reference files. Newest first. Only add a line after the user approved the edit.

| Date | File | Change | Reason (FB ids) | Approved by |
|---|---|---|---|---|
| 2026-10-31 | competitor-intelligence/scripts/collect.py | Meta input drops `activeStatus`; XHS actor `zen-studio/rednote-user-profile-scraper` with `profileUrls`/`includeNotes`/`maxNotesPerProfile`; `check` expands XHS notes | FB-001, FB-002 | user (XHS parser approved in chat; the rest reported in chat) |
| 2026-10-31 | competitor-intelligence/scripts/normalise.py | negative counts become empty; `expand_xhs` and XHS field map; Meta ads match on the Facebook page link; non-Latin names use the profile id as accountId | FB-002, FB-003, FB-006 | user (XHS parser approved in chat; the rest reported in chat) |
| 2026-10-31 | competitor-intelligence/references/platform_scraping.md | Meta and XHS rows confirmed against live runs; Meta discovery URL added | FB-001, FB-002 | user (reported in chat) |
| 2026-10-31 | competitor-intelligence/scripts/normalise.py, references/output_schema.md | items.tsv gains runningDays, isActive, variants (Meta ads); durationSec 0 stored empty; Instagram comment 0 caveat; tags.tsv format documented | FB-009 (1, 2, 3) | user ("Apply top 5") |
| 2026-10-31 | competitor-intelligence/scripts/build_report.py, references/selection.md | select adds up to 2 no-view posts per account when room remains, and never drops an anomaly under the cap | FB-009 (4) | user ("Apply top 5") |
| 2026-10-31 | references/verdict_rules.md, competitor_analysis/skills/content_scoring.md, pattern_detection.md, memory/_template/*.md, agents/competitor_analyzer.md | one confidence rule (low under 5, medium 5 to 14, high 15+ with a second run or own validation; one run caps at medium); scored posts need a view count; analyzer may write tags.tsv | FB-009 (3, 5) | user ("Apply top 5") |
