---
type: reference
status: active
source: adapted from competitor-content-radar/SKILL.md Step 1 (Instagram, TikTok); Meta and XHS rows are new
---
# Platform scraping

One Apify actor run **per platform** for all of that platform's active URLs, never one run per account. Start all platform runs in the same turn. `collect.py plan` writes the exact inputs to `raw/<platform>/input.json`; run the actor with that input, then save the dataset items to `raw/<platform>/items.json` (a JSON array).

If an actor rejects its input, call `fetch-actor-details` once, fix the `ACTORS` table in `collect.py`, and log it in `memory/_system/skill_feedback/competitor-intelligence.md`.

| Platform | Actor | Input (built by `collect.py plan`) | Dataset `fields` to request |
|---|---|---|---|
| instagram | `apify/instagram-scraper` | `directUrls` = profile URLs, `resultsType: "posts"`, `resultsLimit` = Max posts, `onlyPostsNewerThan` = window start (YYYY-MM-DD) | `ownerUsername,shortCode,type,productType,timestamp,videoPlayCount,likesCount,commentsCount,videoDuration,caption,displayUrl,url` |
| instagram followers | same actor | same `directUrls`, `resultsType: "details"` | `username,followersCount` |
| tiktok | `clockworks/tiktok-scraper` | `profiles` = handles, `resultsPerPage` = Max posts, `oldestPostDateUnified` = window start | `authorMeta.name,authorMeta.fans,id,createTimeISO,playCount,diggCount,commentCount,shareCount,collectCount,videoMeta.duration,videoMeta.coverUrl,text,webVideoUrl` |
| meta (Ad Library ads) | `apify/facebook-ads-scraper` | `startUrls` = Ad Library URLs, `resultsLimit` = Max posts, active and inactive ads | **verify on first run** with `fetch-actor-details`; `normalise.py` accepts several field spellings |
| xhs | community actor: find with `search-actors` ("xiaohongshu" / "rednote"); pick one with recent runs and a good rating and record its id in `ACTORS` | profile URLs, limit = Max posts | **verify on first run** |

Actor names and the Meta/XHS field spellings are from memory of the Apify store, not yet confirmed against a live run.

## Rules
- Always pass `fields` when reading a dataset, and a `limit` that covers the whole dataset in one call.
- **2-item test pull before every full run on XHS and Meta** (set the limit to 2, run `collect.py check`); stop if mapped fields are missing.
- If a mapped field is missing on every item, the actor's schema changed: stop with a clear message, never guess.
- Fallback for XHS: another community actor from `search-actors`; log the switch in `memory/_system/`.
- Instagram followers are optional context; save as `raw/instagram/followers.json`.
- Private, deleted, failed or empty accounts are kept (see `requirements.md`).
- Download images after normalising: `collect.py media <run>`; platform image links expire.
- Never put API tokens in files or chat. Apify runs through the authorised MCP connector.
