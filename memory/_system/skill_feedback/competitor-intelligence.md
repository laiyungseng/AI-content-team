---
type: memory
status: active
kind: skill_feedback
skill: competitor-intelligence
---
# competitor-intelligence feedback log
Append only. Format: `_format.md`.

### FB-001 2026-10-31  run: demo/2026-10-31_1534
- type: tool_failure
- where: meta, apify/facebook-ads-scraper, `collect.py plan`
- what happened: input with `activeStatus: "all"` (and `""`) is rejected by the schema; enum is `active | inactive` only. Omitting the field works. All 3 test pages returned `totalCount: 0` (no ads), one item per page with `results: []`, so `normalise.py` must treat a page with no ads as a status row, not as an error.
- user override: none
- proposed edit: applied in `collect.py` (field omitted). A keyword search on the Ad Library (country MY) returned real ads and confirmed the ad field names; the original 3 pages were swapped for pages that run ads. A no-ads page becomes an `empty` account row.
- status: applied
- repeats: 1

### FB-002 2026-10-31  run: demo/2026-10-31_1534
- type: missing_field
- where: xhs, actor choice, `collect.py` ACTORS and `normalise.py` MAP["xhs"]
- what happened: chose `zen-studio/rednote-user-profile-scraper` (input `profileUrls`, `includeNotes`, `maxNotesPerProfile`). Output is ONE item per profile with `profile{}` and a `notes[]` list, not one item per note, and field names differ from the MAP guesses: `id`, `title`/`display_title`, `desc` (truncated), `likes`, `comments_count`, `collected_count`, `share_count`, `create_time` (epoch seconds), `images_list[].url`. `view_count` is always 0 (treat as missing). No note URL: build `https://www.xiaohongshu.com/explore/<id>`. Free tier preview returned notes for the FIRST profile only (3 profiles requested, 1 returned; "15 free runs remaining"), so each account needs its own run or a paid plan.
- user override: none
- proposed edit: applied. `normalise.expand_xhs` flattens notes, MAP["xhs"] updated, link built from the note id, Chinese-name accounts get the profile id as accountId. Tested on real notes (19 notes, 1 inside the 90-day window). Still open: `collect.py plan` makes one call for all accounts, which on the free tier returns only the first profile.
- status: applied
- repeats: 1

### FB-003 2026-10-31  run: demo/2026-10-31_1534
- type: missing_field
- where: instagram, `normalise.py` to_int
- what happened: `likesCount` is -1 when an account hides likes (Knight Frank). It would have become a count of -1.
- user override: none
- proposed edit: applied in `normalise.py` (negative counts become empty).
- status: applied
- repeats: 1

### FB-004 2026-10-31  run: demo/2026-10-31_1534
- type: other
- where: sources.md target choice (demo project)
- what happened: `landed_properties_ltd` is a Lagos, Nigeria agency, not Malaysian. `malaysiahomie` and `nasrulafiqhamzah` on TikTok post sponsored lifestyle and condo content, and `knightfrankmalaysia` / `propnex_malaysia` post corporate content, so few landed-property ads came back. Instagram, TikTok and Meta field names matched `platform_scraping.md` exactly.
- user override: none
- proposed edit: applied. Targets replaced (see FB-005). Instagram's scraper returned `no_items` for 8 of 11 small Malaysian agent accounts, so only Foreward Realty, PropNex and Knight Frank are scrapeable.
- status: applied
- repeats: 1

### FB-005 2026-10-31  run: demo/2026-10-31_1534
- type: other
- where: sources.md targets (demo), XHS profile urls
- what happened: XHS id 6588923f000000001d00030f ("劉-房地产" in search) resolves to an empty profile (26 fans, 0 posts, Sarawak), so it was dropped; 臻选好房志 is a Singapore account. XHS accounts for Malaysian landed property are scarce and small (83 to 220 fans). TikTok `abangsheldon899` has no videos in the window.
- user override: none
- proposed edit: none; use `meta discovery` (Ad Library keyword URL) in `platform_scraping.md` to find advertisers.
- status: applied
- repeats: 1

### FB-006 2026-10-31  run: demo/2026-10-31_1534
- type: method_gap
- where: meta, `normalise.py` build matching
- what happened: Meta ads were matched to `sources.md` rows by page name or numeric page id only. Page names drift ("OG Property Club - 维亚房界" with a dash vs "OG Property Club 维亚房界" in sources), so 4 ads were skipped. Ads carry the page link in `snapshot.pageProfileUri`.
- user override: none
- proposed edit: applied. Meta ads now also match on the Facebook page vanity or id taken from `snapshot.pageProfileUri` and from the row URL.
- status: applied
- repeats: 1

### FB-007 2026-10-31  run: demo/2026-10-31_1534
- type: other
- where: full pull, volumes and cost notes
- what happened: first full pull on 12 accounts: Instagram 90 posts (30 each, window 90d), TikTok 85 videos (Nizam Property 25), Meta 13 ads (Jessica Ngiam 2, OG Property Club 4, N9 Dream Property 7), XHS 3 notes in the window (Sky Property 2, 范范 1, Rex 0 -> `empty`). XHS free tier needed one call per account. Raw datasets had to be saved through the tool-result file because the Apify dataset API needs a token (403 without one).
- user override: none
- proposed edit: none
- status: applied
- repeats: 1

### FB-008 2026-10-31  run: demo/2026-10-31_1534
- type: other
- where: report approval flow, artifact db `decisions`
- what happened: the live approval flow worked end to end. The page wrote document `report` with `decision: approve` and an empty comment; `run.py approve` marked the run approved. No card verdicts were changed, so there is no override signal for `verdict_rules.md` from this run (1 run of the 3 needed for recalibration).
- user override: none
- proposed edit: none
- status: applied
- repeats: 1
