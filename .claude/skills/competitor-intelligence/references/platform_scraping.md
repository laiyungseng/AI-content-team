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
| meta (Ad Library ads) | `apify/facebook-ads-scraper` | `startUrls` = Facebook page URLs (or Ad Library URLs), `resultsLimit` = Max posts. Leave `activeStatus` out: it only accepts `active` or `inactive`, omitted returns both | `pageName,pageId,adArchiveID,startDateFormatted,endDateFormatted,isActive,snapshot.body.text,snapshot.displayFormat,snapshot.ctaText,snapshot.images.originalImageUrl,snapshot.cards.originalImageUrl,snapshot.videos.videoPreviewImageUrl,snapshot.pageProfileUri`. A page with no ads returns one row with `totalCount: 0` and no ad fields |
| meta discovery | same actor | one Ad Library keyword URL: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=MY&q=<keywords>&search_type=keyword_unordered&media_type=all`; use it to find advertisers, then add their pages to `sources.md` (full method and the `suggest` step: `source-manager/references/competitor_discovery.md`) | same |
| xhs | `zen-studio/rednote-user-profile-scraper` | `profileUrls`, `includeNotes: true`, `maxNotesPerProfile` = Max posts. Returns ONE row per profile with `profile{}` and `notes[]`; `normalise.expand_xhs` flattens it. Free tier returns notes for the FIRST profile only (20 notes max), so run one account per call | `notes.id,title,desc,type,create_time,likes,comments_count,collected_count,share_count,images_list,video_info_v2.capa.duration`; `view_count` is always 0 (treated as missing) and notes have no link (built as `/explore/<id>`) |

Checked against live runs on 2026-10-31 (Instagram, TikTok, Meta, XHS). Instagram returns `likesCount: -1` when likes are hidden and `no_items` for many small accounts (treated as failed/empty). TikTok profiles with no recent videos return a `note` row instead of items. Fallback XHS actors: `zhorex/rednote-xiaohongshu-scraper`, `socialdatax/socialdatax-xhs-data-api`.

## Rules
- Always pass `fields` when reading a dataset, and a `limit` that covers the whole dataset in one call.
- **2-item test pull before every full run on XHS and Meta** (set the limit to 2, run `collect.py check`); stop if mapped fields are missing.
- If a mapped field is missing on every item, the actor's schema changed: stop with a clear message, never guess.
- Fallback for XHS: another community actor from `search-actors`; log the switch in `memory/_system/`.
- Instagram followers are optional context; save as `raw/instagram/followers.json`.
- Private, deleted, failed or empty accounts are kept (see `requirements.md`).
- Download images after normalising: `collect.py media <run>`; platform image links expire.
- Never put API tokens in files or chat. Apify runs through the authorised MCP connector.

## Meta searches (keyword and Page lookups)
Adapted from the UPT ad-intelligence method; applies to any Ad Library query, by connector or by actor.
- The Ad Library returns the newest ads first. A broad keyword therefore shows only the newest ads and misses the rest. Use narrow keywords first (service, problem, local-language and place words, tool plus industry) and broad ones last.
- Record, per search, the total the tool reports (if any) and how many were read: **complete** or **partial (n of N)**. A partial result means older ads of that advertiser may be missing; say so wherever ad counts are quoted.
- To read one advertiser fully, query by Page (its Page link or Page ID), never by keyword.
- After a discovery pass, search again with the distinct headlines of the biggest advertisers' ads (hook reverse search) to find advertisers the keywords missed. Stop when two rounds in a row find nothing new.
- Run the three-search coverage audit and report coverage as an estimate ("about 85%, audits 4% / 8% / 12% new"), never "complete" or "100%". Steps are in `source-manager/references/competitor_discovery.md`.
- The Ad Library has no spend, reach or results for commercial ads: longevity and copies are the only signals.
