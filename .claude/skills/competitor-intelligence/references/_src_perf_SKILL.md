---
source: content-performance-dashboard/SKILL.md (staging: Ours baseline method)
copied: 2026-10-31
---
---
name: content-performance-dashboard
description: "Build or refresh an Instagram + TikTok content performance dashboard from a one-off Apify pull, published as a Claude Artifact, for a personal-brand creator account. Use whenever asked to build, rebuild, refresh, or clone this specific IG+TikTok analytics dashboard for a (new) creator account."
---

# Content performance dashboard (Instagram + TikTok)

`assets/dashboard_template.html` is a finished, debugged page. A run supplies
data and written insights; `scripts/build.py` does the assembly and checks.
Below, `$SKILL` means the folder this SKILL.md is in.

**Speed rules for every run:**

- Do NOT open, read or edit `dashboard_template.html`. `build.py` writes the config block for you.
- Do NOT write post data as Python or JSON. Write the compact `posts.tsv` in Step 2.
- Do NOT write your own analysis code. `build.py analyze` prints what the insights need, computed exactly as the page computes it.
- Do NOT render or screenshot the page when only data and insights changed. `build.py` syntax-checks it.
- Make independent tool calls in the same turn (both actor runs at once, both dataset reads at once).

The page is a **static snapshot**: pull once, bake the posts in, publish. No
cache, no refresh button, no capabilities (a published page cannot reach
Apify; see `references/design-notes.md`). Fresh numbers mean a new pull
republished to the same URL.

## What it shows

Instagram and TikTok tabs (stats, best and weakest post, a reach vs engagement
quadrant with click-through, hit rate vs the prior period, video length, a bar
per post, performance by topic, a sortable table) and an All tab (platform
head-to-head only). A **What to do next** card at the top carries the one
authored paragraph. Numbers are computed by the page; the sentences that make
it worth reading are the insights you write in Step 3.

## Step 0: ask, then wait

**Refreshing an existing dashboard?** Skip the questions. Find it with Artifact `list`, `read` it, then:

```
python3 $SKILL/scripts/build.py reuse <path to read index.html> config.json
```

This recovers handles, window, title and the topics **verbatim, colors included**. Keeping the topics identical is what keeps topic performance comparable across snapshots; only add a topic when the creator has genuinely started making something new. Go to Step 1.

**New dashboard?** Ask both in one question (use a structured question tool if the session has one) and wait:

1. The Instagram and TikTok handles or profile URLs.
2. **How many days: 7, 30 or 90** (suggest 30). This window is the dashboard's window until it is rebuilt. Longer costs more credits and scrape time; 7 days on a low-volume account leaves too few posts and no prior period for the hit-rate comparison.

## Step 1: pull via Apify (date-filtered, trimmed)

Start both runs in the same turn:

- **Instagram**: `apify/instagram-scraper`, `directUrls` = [profile URL], `resultsType: "posts"`, `onlyPostsNewerThan` = window start (YYYY-MM-DD).
- **TikTok**: `clockworks/tiktok-scraper`, `profiles` = [handle], `oldestPostDateUnified` = window start.

Only if an actor rejects the input, call `fetch-actor-details` once for its schema.

Read each dataset with `get-dataset-items` in one call, always passing `fields` and a `limit` that covers the whole dataset:

| Run | `fields` |
|---|---|
| Instagram | `shortCode,timestamp,videoPlayCount,likesCount,commentsCount,videoDuration,caption` |
| TikTok | `id,createTimeISO,playCount,diggCount,commentCount,shareCount,collectCount,videoMeta.duration,text` |

If a mapped field is missing on every item, the actor's schema has changed; check one item and adjust.

## Step 2: write two small files

**Topics.** Read the captions first, then settle 4 or 5 themes that match what this creator actually posts about, plus `uncategorized` (added automatically if missing). There are 5 validated topic colors, so 5 themes is the maximum; `build.py` assigns colors itself.

**`config.json`** (on refresh, edit the one `reuse` produced: set `pulledAt`, keep everything else):

```json
{
  "title": "Content Performance",
  "pulledAt": "2026-10-01T09:00:00Z",
  "windowDays": 30,
  "handles": {"instagram": "their_ig_handle", "tiktok": "their_tt_handle"},
  "topics": {
    "brand_demos": {"label": "Brand & Client AI Demos",
                    "description": "Work built for a named brand or client, shown as a before/after or live demo."}
  },
  "insights": {}
}
```

**`posts.tsv`**: one line per post, tab-separated, no header, 11 columns. Assign the topic as you write each line.

```
platform  postId  timestamp  views  likes  comments  shares  saves  durationSec  topic  caption
```

- `platform`: `instagram` or `tiktok`.
- `postId`: Instagram `shortCode`, TikTok `id`. IDs and URLs are built by the script.
- `timestamp`: as returned (`timestamp` / `createTimeISO`).
- `views` <- `videoPlayCount` / `playCount`. **Leave empty for Instagram photo and carousel posts** (they have no view count). The page keeps them out of every view-based number and lists them in the table only.
- `likes` <- `likesCount` / `diggCount`; `comments` <- `commentsCount` / `commentCount`.
- `shares`, `saves`: TikTok `shareCount`, `collectCount`. Leave empty for Instagram (it never returns them). Never write 0 for a missing number.
- `durationSec` <- `videoDuration` / `videoMeta.duration`.
- `caption`: **first 120 characters only** (the page never shows more), no tabs, line breaks written as `\n` (the page uses the first line as the hook).

Copy numbers exactly as returned.

## Step 3: analyze, then write the insights

```
python3 $SKILL/scripts/build.py analyze config.json posts.tsv
```

It validates the rows and prints, per platform, every post with a view count ranked by outlier score with its quadrant and topic, the quadrant counts, the topics in the order the page ranks them, and any photo or carousel posts separately. Never compare a photo post's reach with a video's; photos can only be compared with each other, by likes and comments. The top and bottom of each list are your top-five vs bottom-five comparison. Read the full captions of those posts (already in context from Step 1) and find what actually separates them; no code can see that.

**Read `references/writing-insights.md` before writing.** Then fill `insights` in `config.json`:

```json
"insights": {
  "headline": "One paragraph: the single most useful thing you found, ending in what to do this week.",
  "quadrants": {
    "instagram": {"both": "", "reach_only": "", "eng_only": "", "neither": ""},
    "tiktok":    {"both": "", "reach_only": "", "eng_only": "", "neither": ""}
  },
  "topics": {"instagram": "Why the top topic wins here.", "tiktok": ""}
}
```

An empty string falls back to the page's generic copy, which is the right answer when you have nothing grounded to say. These strings are scoped to the full pulled window; the page hides them when the viewer narrows the range.

## Step 4: build

```
python3 $SKILL/scripts/build.py build config.json posts.tsv /mnt/user-data/outputs/<slug>/index.html
```

It writes the page and syntax-checks it. If it prints `FAILED`, fix the row or field it names and rerun.

## Step 5: publish and hand over

Publish with the Artifact tool, favicon 📈, **no capabilities**.

- **Refresh**: pass the existing artifact's `url` (you read it in Step 0, which a republish requires) so the creator's saved link keeps working. Never hand over a second link.

When handing over, say it is a snapshot of that window taken today, and that fresh numbers mean asking you to pull again (the link stays the same).

## Only when asked to change the page itself

Read `references/design-notes.md` first. After any template edit, render the page once (no console errors; tabs, quadrant modal, table and insights hold real data), fix what that shows, and stop. No screenshot-and-tweak loop.
