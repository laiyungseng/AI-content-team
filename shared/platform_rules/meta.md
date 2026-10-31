---
type: platform_rules
status: active
platform: meta
updated: 2026-10-31
---
# Meta

Rules for Facebook and Instagram paid ads, and how to read the Meta Ad Library. Limits change often. Values marked (verify) must be re-checked against the platform before a publish; log changes in `memory/_system/`.

## What we collect
- Competitor **ads** from the Meta Ad Library (not organic posts). Each item has itemType `ad`.
- Ad Library shows creative, copy, start date, running status and platforms; **it does not show spend, reach or engagement** for commercial ads.

## How to read an ad
- **Longevity is the only performance signal**: an ad running for weeks (especially with many variants of the same creative) is likely working; one that ran a few days was likely cut. Treat as a hypothesis, state days running and number of variants.
- Leave metric columns in `items.tsv` empty (not 0). Use `date` = ad start date.
- Note format (video, image, carousel), hook, offer and CTA button text.

## Ad creative specs (verify)
- Feed 1:1 or 4:5; Stories/Reels placements 9:16 with safe zones (~14% top, ~20% bottom clear).
- Primary text: keep the first ~125 characters self-sufficient; headline short; one CTA button.

## Rules
- Hook [[hooks]], CTA [[cta]]. Never copy a competitor's creative or claims; extract the angle and rebuild it.
- Comparison with our ads is on creative approach and longevity only, not engagement. See [[stats_rules]].
