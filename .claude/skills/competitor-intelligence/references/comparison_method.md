---
type: reference
status: active
---
# Us vs them method

Input: `items.tsv`, `analysis/verdicts.json`, `analysis/ours.json`. Output: `analysis/comparison.json` (schema in `output_schema.md`).

## Rules
- Compare like with like: ratio to own typical, engagement per 1,000 viewers (likes + comments), cadence, consistency. Never raw views or followers across accounts ([[stats_rules]]).
- Quote the post counts behind every claim (`postCounts`). Small samples: "too early to call".
- No Ours data: rows say "no baseline yet" and strategy is limited to what competitors do.
- Meta ads: compare creative approach and longevity only.

## Rows (one per dimension)
hook, format, visual, message, offer, CTA, cadence, engagement. Per row: what we do (ours), what they do (theirs), who is stronger (`ours|theirs|similar|unclear`), why, how we implement it. "Why" cites evidence; "how" is something the production team can do.

## Topic coverage
Use the shared topics from `sources.md`. Whitespace = a topic working for competitors and unused by us. Saturated = every competitor with 4+ posts is below its usual. Anything else: "too early to call".

## Strategy and positioning
- Strategy: 3 to 5 items, each with a "Do next". Respect the mix 70% proven / 20% adjacent / 10% experimental ([[experimentation]]) and tag each Educate / Engage / Promote.
- Positioning: one statement of where we can stand apart, the gaps competitors leave, what to avoid.
- Headline: one paragraph, ends with "Do next: ...".
