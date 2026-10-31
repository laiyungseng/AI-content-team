---
type: reference
status: active
source: posts.tsv null rules adapted from competitor-content-radar
---
# Output schema

## items.tsv (unified, tab-separated, with header)
`owner accountId platform itemType itemId date views likes comments shares saves durationSec topic pillar caption mediaUrl permalink status runningDays isActive variants sponsored`

| column | rule |
|---|---|
| owner | `ours` or `competitor` |
| accountId | lowercase slug of the source row's Name |
| platform | instagram, tiktok, meta, xhs |
| itemType | `post` or `ad` |
| itemId | shortCode / video id / ad archive id / note id |
| date | YYYY-MM-DD (UTC) |
| views, likes, comments, shares, saves, durationSec | integers. **Empty = missing, never 0.** Photo/carousel posts have no views; Instagram has no shares/saves; ads have no metrics. `durationSec` 0 from an actor is stored empty. Instagram `comments` of 0 can be a true zero or hidden comments, so it is not proof of no engagement |
| topic | key from `sources.md` Topics (assigned in analysis, via `normalise.py tag`) |
| pillar | content pillar, ours only (max 3) |
| caption | tabs/newlines replaced by spaces, first 300 chars; for non-ok rows, the reason |
| mediaUrl | image/thumbnail URL as returned (expires; see `media/`) |
| permalink | link to the original |
| status | ok, private, failed, empty |
| runningDays | Meta ads only: days from the ad's start date to its end date (or the run date if none), minimum 0. Empty for posts |
| isActive | Meta ads only: `yes` or `no` as returned by the Ad Library, empty if unknown |
| sponsored | `yes` when the post is a paid partnership or carries an advert label in its caption (set by the analyzer through tags.tsv), empty otherwise. Meta ads are ads already and stay empty |
| variants | Meta ads only: number of ads from the same page with identical text (first 300 characters), counting itself. A re-run under a new ad id counts as a variant |

## tags.tsv (run folder, written by competitor_analyzer, read by `normalise.py tag`)
Tab-separated, header `itemId<TAB>topic<TAB>pillar<TAB>sponsored`. One row per ok item; `topic` must be a key from `sources.md` Topics; `pillar` is optional (ours only); `sponsored` is optional and is `yes` or empty. Tag a sponsored post by what it shows (a home tour is `listing_tour`), never `off_topic` just because it is paid. Ids are matched on `itemId` alone.

## Analysis files (`runs/<id>/analysis/`, JSON so the report builder can read them)
**verdicts.json**
```json
{"items": [{"id": "<itemId>", "verdict": "adapt|copy|ignore", "reason": "...", "hook": "...",
            "whyItWorks": "...", "howToUse": "...", "confidence": "low|medium|high"}]}
```

**hooks.json** (from hook_analyzer)
```json
[{"id": "<itemId>", "spoken": "", "text": "", "visual": "", "audio": "", "scores": {}, "formula": "", "whyItStopsScroll": "", "howToRebuild": ""}]
```

**ours.json**
```json
{"summary": "...", "accounts": [{"id": "", "posts": 0, "typicalViews": null, "bestTopic": "", "notes": ""}], "missing": ""}
```

**comparison.json**
```json
{"headline": "one paragraph ending in 'Do next: ...'",
 "rows": [{"dimension": "hook", "ours": "", "theirs": "", "stronger": "ours|theirs|similar|unclear", "why": "", "how": ""}],
 "strategy": [{"title": "", "detail": "", "doNext": ""}],
 "positioning": {"statement": "", "gaps": [""], "avoid": [""]},
 "postCounts": "text quoting the post counts behind the claims"}
```
Dimensions: hook, format, visual, message, offer, CTA, cadence, engagement.

## Decisions (artifact db, collection `decisions`)
Per card: document id = itemId with characters outside `A-Za-z0-9_-` replaced by `_`; fields `{item, verdict, comment, at}` (the user's final verdict). Overall: id `report`, `{item: "report", decision: approve|revise|reject, comment, at}`. See `.claude/skills/artifact-presentation-setup/references/approvals.md`.
