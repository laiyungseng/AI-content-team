---
type: platform_rules
status: active
platform: linkedin
updated: 2026-10-31
---
# LinkedIn

Specs and rules for LinkedIn posts, document carousels and video. Limits change often. Values marked (verify) must be re-checked against the platform before a publish; log changes in `memory/_system/`.

## Formats
| Format | Spec | Notes |
|---|---|---|
| Text post | up to 3,000 characters | First ~210 characters show before "see more": put the hook there |
| Document carousel (PDF) | one slide per page, 1:1 or 4:5 | Large type, one point per slide, CTA on the last slide |
| Video | 16:9, 1:1 or 9:16 | Captions on; most viewing is silent |

## Tone and rules
- Professional but human: concrete numbers, specific stories, a clear point of view.
- Avoid external links in the post body when reach matters (put in first comment; treat as hypothesis).
- Hook rules: [[hooks]]. CTA: [[cta]] (prefer comment or DM prompts over hard sells).

## Data caveats
- Competitor data is not collected on LinkedIn in Phase 1 (not in `sources.md`).
