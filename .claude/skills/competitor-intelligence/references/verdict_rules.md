---
type: reference
status: active
---
# Verdict rules: Adapt / Copy / Ignore

Applies to **competitor items only**. Decide from evidence, in this order. Write reasons in plain words ([[writing_insights]]).

| Verdict | Use when | Meaning |
|---|---|---|
| **Copy** | The item clearly worked (ratio >= 2 to that account's typical, or an ad running 30+ days or with many variants) **and** the idea is brand-neutral or fits us as is (format, structure, pacing, hook type). | Reuse the structure nearly as is, with our content. Never copy their claims, footage, music or text. |
| **Adapt** | It worked, but the angle, product, audience or tone differs from ours. | Keep the mechanism, rebuild it for our offer and voice. State what changes. |
| **Ignore** | Did not work (ratio < 1), no repeatable idea, off-brand, a one-off anomaly (ratio >= 10), or too little data. | Do not act on it. Say which reason. |

## Checks before assigning
1. Use the ratio to the account's own typical views, never raw views. Missing views: say so, judge on likes and comments only, confidence low.
2. Account with under 5 scored posts (posts that have a view count): at most Adapt with confidence low, or Ignore "need more posts".
3. Anomaly (ratio >= 10): Ignore as a pattern; mention it as something to look at.
4. Ads (Meta): no metrics. Use `runningDays`, `isActive` and `variants` from items.tsv (a long-running live ad, or one with several variants, worked); confidence at most medium.
5. Brand fit: if `brand/<project>/` has a guideline, check voice and prohibited claims; otherwise judge on the audience and offer the user described.

## Confidence levels (one rule for verdicts, patterns and memory)
Count the posts behind the finding. Fewer than 5 is low, 5 to 14 is medium, 15 or more is high. One run caps the result at medium: high also needs a second run or our own posts that confirm it. For an account's own verdicts, only posts with a view count are scored.

## Recalibration
User overrides in the report (verdict changed, with a comment) are logged to `memory/_system/skill_feedback/competitor-intelligence.md`. After 3 runs, propose threshold edits to this file; apply only after approval and log them in `memory/_system/changelog.md`.
