---
type: platform_rules
status: active
platform: tiktok
updated: 2026-10-31
---
# TikTok

Specs and rules for TikTok videos. Limits change often. Values marked (verify) must be re-checked against the platform before a publish; log changes in `memory/_system/`.

## Format
- 9:16, 1080x1920, MP4/MOV; length from a few seconds to several minutes (verify). Short, tightly cut videos are the default.
- Keep captions, text and UI-covered areas clear of the right-hand button column and the bottom caption area.
- Caption limit about 2,200 characters (verify).

## Hook and pacing
- The hook must land in the first 1-2 seconds, with spoken, text, visual and audio components aligned. See [[hooks]].
- Pattern changes (cut, zoom, text) every few seconds keep retention; each beat earns the next.

## Data caveats (for analysis)
- Public data returns views, likes, comments, shares and saves; view counts are available for all videos.
- Video length buckets are fit per account, not global. See [[stats_rules]].

## Content rules
- CTA: one clear action, placed per [[cta]]. Story formats: [[storytelling]].
- Trending sound use is a hypothesis to test, not a default; record results in `memory/`.
