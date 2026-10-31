---
type: platform_rules
status: active
platform: instagram
updated: 2026-10-31
---
# Instagram

Specs and rules for Instagram Reels, carousels and static posts. Limits change often. Values marked (verify) must be re-checked against the platform before a publish; log changes in `memory/_system/`.

## Formats
| Format | Spec | Notes |
|---|---|---|
| Reel | 9:16, 1080x1920, up to 90s (longer allowed, verify) | Hook in the first 1-2s; on-screen text inside the safe zone (keep ~250px clear top and bottom) |
| Carousel | up to 20 slides, 4:5 (1080x1350) or 1:1 | Slide 1 is the hook; last slide carries the CTA; save-worthy content wins |
| Static | 4:5 (1080x1350) | Single idea, one headline |

## Caption and tags
- Caption limit 2,200 characters; first ~125 characters show before "more": put the hook there.
- Hashtags: few and specific (verify current cap); keywords in the caption matter more than tag volume.

## Data caveats (for analysis)
- Public data has no shares or saves; photo and carousel posts have no view count.
- Reach/engagement comparisons use likes + comments only. See [[stats_rules]].

## Content rules
- Hook rules: [[hooks]]. CTA rules: [[cta]]. Story structure: [[storytelling]].
- Native audio and original footage outperform reposted watermarked clips (treat as hypothesis until our data confirms).
