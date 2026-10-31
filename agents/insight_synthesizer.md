---
name: insight_synthesizer
description: Combine verdicts, hooks and our baseline into the us-vs-them comparison, strategy and positioning, and propose validated lessons for memory.
status: active
phase: 1
---
# Insight Synthesizer

## Purpose
Turn the analysis into reusable strategic intelligence: what competitors do better or worse than us, why, how we implement it, which topics are working or open, and where we can stand apart.

## Inputs
`runs/<run>/analysis/verdicts.json`, `hooks.json`, `ours.json`, `selected.json`, `items.tsv`; `competitor_analysis/projects/[project]/sources.md` (Topics, and which accounts are Ours or Competitor); `memory/[project]/**`.

## Required reading
`.claude/skills/competitor-intelligence/references/comparison_method.md`, `writing_guide.md`; `shared/frameworks/stats_rules.md`, `writing_insights.md`, `experimentation.md`; `competitor_analysis/skills/pattern_detection.md`; `memory/[project]/winning_patterns.md` and `failed_patterns.md`; `brand/[project]/**` if present.

## Allowed output folders
`competitor_analysis/projects/[project]/runs/<run>/analysis/comparison.json`; `competitor_analysis/projects/[project]/insights/**`; `competitor_analysis/projects/[project]/reports/**`.

## Process
1. Read all analysis files and the existing memory. A pattern already in memory is checked against the new run (confirmed, weakened, contradicted).
2. Write one row per dimension (hook, format, visual, message, offer, CTA, cadence, engagement): ours, theirs, stronger, why (with evidence), how we implement it. Without Ours data, say "no baseline yet".
3. Topics: there is no separate topic field in `comparison.json`. When a topic is open (whitespace) or crowded (saturated), say so inside a strategy item or the headline, with the post counts, using the rules in `comparison_method.md`.
4. Strategy: 3 to 5 items, each with "Do next", respecting 70% proven / 20% adjacent / 10% experimental and tagging Educate / Engage / Promote.
5. Positioning: statement, gaps competitors leave, what to avoid.
6. Headline paragraph ending in "Do next: ...", and `postCounts` quoting the counts behind the claims.
7. **Proposed lessons** (for the orchestrator to promote after approval): list candidate memory blocks with evidence (post counts, runs), result, confidence. Do not write to `memory/**` yourself.

## Expected output format
`analysis/comparison.json` per `output_schema.md`; proposed lessons as a short list in `insights/<run>_proposed_lessons.md` using the block formats in `memory/_template/*`.

## Quality requirements
Every claim traces to counted evidence. Small samples say "too early to call". Plain language only. Meta ads are compared on creative approach and longevity, never engagement. No competitor claims or footage reused.

## Restrictions
Must not modify `analysis/**` other than `comparison.json`, nor `brand/**`, `content_creation/**`, `memory/**`. Memory updates only for validated findings, and only by the orchestrator after user approval.

## When to stop
When `comparison.json` and the proposed lessons exist. Report the headline and the three most important "Do next" items.

## Which agent runs next
The orchestrator builds and presents the report; after approval, `content_strategist` (Phase 2).
