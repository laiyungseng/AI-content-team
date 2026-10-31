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
