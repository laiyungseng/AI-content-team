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

## Safe claims (ads)
Keep claims specific but safe. Applies to paid ads and to organic posts that carry an offer.

**Avoid**
- Assuming a personal attribute ("Are you in debt?", "You are blacklisted").
- Guaranteed income, approval, medical or education results.
- Before/after material implying every customer gets the same result.
- Aggressive fear language aimed at a sensitive status.

**Safer patterns**
- Speak to business situations, not identity; "many owners face..." instead of "you are...".
- Use "may help", "designed for", "assessment", "case example". Show proof as an example, never as a guaranteed outcome.
- Results depend on documents, execution, market, budget and assessment; terms and conditions apply.

### Regulated categories
Flag financing, loans, investment, income claims, health, beauty, education outcomes, government-related and approval claims.

**Finance (loans, grants, SME funding, credit-check or approval topics)**
- Never: guaranteed approval, "100% approved", "no rejection", "blacklisted can still get it", an unverified government-backed claim, "instant money", "no documents needed", a misleading link to an official body, promised speed or outcome.
- Use: subject to approval; terms and conditions apply; eligibility depends on documents and assessment; speak to a consultant for assessment; "assess your documents and eligibility first, then see which option fits".
- Angle direction: keep urgency but drop the guaranteed outcome; speak to fear of rejection, confusion, documents and wrong applications; make the assessment the bridge to action; filter out people expecting shortcuts or instant approval.

**Courses and training:** no unrealistic income or outcome promises.
Write each brand's own banned and required wording to `brand/[project]/prohibited_claims.md`. (verify) Platform policies change; re-check before a publish.
