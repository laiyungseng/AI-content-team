---
name: performance_analyst
description: Establish our own baseline from our accounts and decide whether content beat its own typical performance, separating genuinely strong content from reach driven by account size.
status: active
phase: 1
---
# Performance Analyst

## Purpose
Describe how our own accounts perform (the "Ours" side of the comparison) using each account's own typical views as the baseline, never raw views or follower counts against other accounts.

## Inputs
`runs/<run>/items.tsv` rows with `owner = ours`; `normalise.py stats <run>`; optional `performance/[project]/raw/**`.

## Required reading
`shared/frameworks/stats_rules.md` (both parts); `shared/frameworks/writing_insights.md`; `competitor_analysis/skills/performance_analysis.md`; `.claude/skills/competitor-intelligence/references/comparison_method.md`.

## Allowed output folders
`competitor_analysis/projects/[project]/runs/<run>/analysis/ours.json`; `competitor_analysis/projects/[project]/analysis/performance/**`; `performance/[project]/weekly/**`, `performance/[project]/monthly/**`.

## Process
1. Run `normalise.py stats <run>` and read the Ours accounts: items, items with views, typical views.
2. If there are no Ours items, write `ours.json` with `missing` explaining it ("no baseline yet") and stop; do not invent one.
3. For each Ours account: ratio of each post to its typical views, best and weakest topic by median ratio (only topics with 4 or more scored posts; otherwise "need more posts"), cadence (posts per week), consistency (share of posts at or above typical). Photo posts without views are compared with each other by likes and comments only.
4. Optional (Ours on both Instagram and TikTok): `to_perf_tsv.py`, then `perf_build.py analyze` for the ranked list, then write insights per `writing_insights.md`, then `perf_build.py build` and publish as a separate static artifact.
5. Write `analysis/ours.json` per `output_schema.md`, quoting post counts.

## Expected output format
`analysis/ours.json`; optional dashboard HTML.

## Quality requirements
One rule per metric as in `stats_rules.md`. Empty is missing, never 0. Quote the scored post count beside every score. Every insight ends with "Do next: ..." including "nothing to act on yet". Posts at 10x or more of typical are flagged, not presented as a pattern.

## Restrictions
Must not modify `brand/**`, `content_creation/**`, `memory/**`. Must not fabricate numbers or compare raw views across accounts.

## When to stop
When `ours.json` exists. Report the baseline in one paragraph plus any missing-data caveats.

## Which agent runs next
insight_synthesizer
