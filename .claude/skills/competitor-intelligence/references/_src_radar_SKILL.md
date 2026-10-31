---
source: competitor-content-radar/SKILL.md (staging: adapt into platform_scraping.md, requirements.md, output_schema.md)
copied: 2026-10-31
---
---
name: competitor-content-radar
description: "Build or refresh a competitor content-performance dashboard (Apify-pulled Instagram/TikTok posts, published as a Claude Artifact) that compares one or more accounts. Use whenever asked to build, rebuild, refresh, or clone this multi-account competitor radar dashboard for a new or existing set of accounts."
---

# Competitor content radar (Instagram + TikTok)

The dashboard is finished, working code in `references/dashboard_template.html`.
A run only supplies data. `scripts/build.py` does the assembly and checking.
Below, `$SKILL` means the folder this SKILL.md is in.

**Speed rules for every run:**

- Do NOT open, read or edit `dashboard_template.html`. The build script injects into it. Reading it costs ~20k tokens for nothing.
- Do NOT write JSON by hand. Write the compact `posts.tsv` described in Step 2.
- Do NOT write tagging scripts, jsdom tests, Playwright screenshots or synthetic-data simulations. `build.py` covers what a data-only run needs.
- Do NOT use `write_db` or the `db` capability. The data is baked into the page.
- Make independent tool calls in the same turn (all actor runs at once, all dataset reads at once).

This is not the `content-performance-dashboard` skill (single creator, Instagram vs TikTok, "Pull data" button). This one has one tab per account, plus Head to Head and Topics & Gaps when there are 2+ accounts, and an always-present Playbook tab. There is deliberately no "Pull data" button; do not add one unless asked.

## Step 0: ask, then WAIT

**Refreshing an existing radar?** Skip the questions. Find it with Artifact `list`, `read` it, then run:

```
python3 $SKILL/scripts/build.py --reuse <path to read index.html> --out-config config.json
```

That recovers accounts, topics and title. Reuse the same topic keys so the dashboard stays comparable. Go to Step 1.

**New radar?** Ask in one message, then wait:

1. The accounts to track (any number, any mix of Instagram and TikTok).
2. Whether one is the user's own account (`isMine: true` unlocks "Me vs. the field" and Whitespace). Otherwise all are `isMine: false`.
3. The time window, if not the default of the past 30 days.

In the same message, say plainly: at about 30 posts per account only big differences show up, so a wider window helps if they want conclusions by topic.

## Step 1: pull with Apify (batched, trimmed)

One actor run per platform covering ALL handles, not one run per account. Start them all in the same turn.

- **Instagram posts**: `apify/instagram-scraper`, `directUrls` = every profile URL, `resultsType: "posts"`, `onlyPostsNewerThan` = window start (YYYY-MM-DD).
- **Instagram followers**: same actor, same `directUrls`, `resultsType: "details"`.
- **TikTok**: `clockworks/tiktok-scraper`, `profiles` = every handle, `oldestPostDateUnified` = window start.

Only if an actor rejects the input, call `fetch-actor-details` once to read its schema.

Read results with `get-dataset-items`, always passing `fields` (raw items are mostly fields the page never uses) and a `limit` that covers the whole dataset in one call:

| Run | `fields` |
|---|---|
| IG posts | `ownerUsername,shortCode,timestamp,videoPlayCount,likesCount,commentsCount,videoDuration,caption` |
| IG details | `username,followersCount` |
| TikTok | `authorMeta.name,authorMeta.fans,id,createTimeISO,playCount,diggCount,commentCount,shareCount,collectCount,videoMeta.duration,text` |

If a mapped field is missing on every item, the actor's schema has changed; check one item and adjust the mapping.

An account that is private, deleted, failed, or has zero posts in the window is never dropped. Give it `status` `"private"` / `"failed"` / `"empty"` and a short `errorNote`.

## Step 2: write two small files

**Topics first.** One shared taxonomy across all accounts, 4 to 6 broad topics (never per-account lists, never 8+). Fewer topics means more posts per topic, which is what lets the page conclude anything.

**`config.json`** (on refresh, edit the one `--reuse` produced: set `pulledAt`, update `followers` and `status`):

```json
{
  "title": "Name for the account set (stays stable across refreshes)",
  "pulledAt": "2026-10-01T09:00:00Z",
  "topics": {"company_teardown": "Company & Business Economics"},
  "accounts": [
    {"id": "lowercasehandle", "displayName": "Readable Name", "handle": "handle",
     "platform": "Instagram", "isMine": false, "status": "ok", "followers": 27523},
    {"id": "otherhandle", "displayName": "Other", "handle": "otherhandle",
     "platform": "TikTok", "isMine": false, "status": "private", "followers": null,
     "errorNote": "account is private"}
  ]
}
```

**`posts.tsv`**: one line per post, tab-separated, no header, exactly these 11 columns. Assign the topic as you write each line; there is no separate tagging step.

```
accountId  postId  date  views  likes  comments  shares  saves  durationSec  topic  caption
```

- `postId`: Instagram `shortCode`, TikTok `id`. URLs are built by the script.
- `date`: `YYYY-MM-DD` from `timestamp` / `createTimeISO`.
- `views` <- `videoPlayCount` / `playCount`. **Leave empty** for photo and carousel posts. Never write 0 for a missing number.
- `likes` <- `likesCount` / `diggCount`; `comments` <- `commentsCount` / `commentCount`.
- `shares`, `saves`: TikTok `shareCount`, `collectCount`. Leave empty for Instagram.
- `durationSec` <- `videoDuration` / `videoMeta.duration`, empty for non-video.
- `caption`: **first 150 characters only** (the page never shows more), tabs and newlines replaced by spaces.

Copy numbers exactly as returned. For a very large pull, writing posts in a few chunks and joining them with `cat` is fine.

## Step 3: build

```
python3 $SKILL/scripts/build.py config.json posts.tsv /mnt/user-data/outputs/<slug>/index.html
```

It validates every row, enforces the null rules, builds the URLs, injects the data, sets the title and pulled-at time, and syntax-checks the page. If it prints `BUILD FAILED`, fix the named line and rerun. It finishes by printing post counts per account and topic, which you use in Step 5.

## Step 4: publish

Publish the built file with the Artifact tool and **`capabilities: {}`** (explicitly empty).

- **Refresh**: pass the existing artifact's `url` so the link stays the same. The empty `capabilities` is required here: older radars declared `db`, and a cached copy in that database would otherwise be shown instead of the new data.
- **New radar**: no `url`.

## Step 5: hand over

In plain words, no statistical terms:

- Which accounts are in, and any that could not be pulled and why.
- Which topics have too few posts to judge (from the build summary: under 4 video posts for an account) and what would fix it (a wider window).

## Only when the user asks to change the page's design or logic

Read `references/maintainer-notes.md` first. It holds the analysis rules, the plain-language rules for on-page copy, and the full validation that any template change must pass. None of that applies to a normal data run.
