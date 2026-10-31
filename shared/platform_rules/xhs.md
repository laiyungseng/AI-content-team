---
type: platform_rules
status: active
platform: xhs
updated: 2026-10-31
---
# XHS

Rules for Xiaohongshu (RedNote). Limits change often. Values marked (verify) must be re-checked against the platform before a publish; log changes in `memory/_system/`.

## Formats
| Format | Spec | Notes |
|---|---|---|
| Image note | up to 18 images (verify), 3:4 preferred | Cover image carries the hook: big title text, clear subject |
| Video note | 9:16 or 3:4 | Cover frame and title matter as much as the first second |

## Text
- Title short (limit about 20 characters, verify) and curiosity or benefit led; body is practical and personal, list-style ("N tips", step-by-step).
- Topic tags (#) drive search discovery; use a few relevant ones. XHS behaves like a search engine: keywords in title/body matter.
- Saves and comments are the key engagement signals; likes are cheap.

## Data caveats (for analysis)
- Community Apify scrapers are less reliable: run a 2-item test pull first and log failures to `memory/_system/`.
- Fields vary by actor; missing = empty, never 0. Default volume is 20 posts per account.
- Tone and compliance rules differ in mainland China; check regulations before adapting claims.

## Content rules
- Hooks [[hooks]], CTA [[cta]] (soft: "save this", "follow for part 2"). Metrics treatment: [[stats_rules]].
