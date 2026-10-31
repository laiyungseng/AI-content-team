---
source: social-media-automation 0.2.0 / social-media-scriptwriting/references/hook-research.md (adapt: sortfeed -> Apify pull ranked by ratio)
copied: 2026-10-31
---
# Hook Research Method

How to find and validate hook patterns that work in a specific niche.

## Why do this

Most people will not open a database when trying to write a fresh hook. It takes too long and generic examples are rarely applicable to a specific niche. The point of research is to train pattern recognition so that pulling the right structure becomes second nature.

Hooks found this way are the best kind, because they have already been proven on the exact audience being targeted.

## The process

**1. Build a creator list of 20 to 30 accounts in the niche** that target the same ideal viewer. Look for accounts with at least 50K followers and at least 50 posts.

*Where to find them:*
- If you follow the space at all, you already have one in mind. Open their "Following" list and scan it. That usually yields 20 more.
- Starting from scratch: open a fresh account on a new email, type niche-relevant terms into search, then scroll and like on-topic posts. Within 15 minutes the Explore feed will be full of them.

Keep the list in a note.

**2. Sort their videos by performance.**
In this project the Apify pull replaces a feed-sorting tool. `items.tsv` already holds each competitor's recent posts; rank them **by ratio to that account's own typical views** (see `shared/frameworks/stats_rules.md`), not raw views, so a small account's best post is not buried under a big account's average one. Study the top-ratio posts per account, and treat anything at 10x or more as an anomaly, not a pattern. For a deeper look at one account, raise its Max posts in `sources.md` (up to 200) and run again.

**3. Analyse the hooks.**
Open the top performers in new tabs. For each one, note any hook that caught your eye and document *what* about it caught your eye, using the four component buckets: spoken, text, visual, audio. Pattern recognition comes from doing this in aggregate, not from any single video.

**4. Log the patterns.**
Keep a simple table: creator, video link, spoken hook structure, text hook, visual hook, audio hook, why it worked.

**5. Repeat every 2 to 4 weeks.**
Formats decay. Re-running the list surfaces what is working now that was not before.

## Reference

An example of a creator catalogue worth studying this way: https://www.instagram.com/orenmeetsworld/reels/

## What to do with the findings

Feed validated structures back into the structures library in `writing-a-hook.md` section 4 as niche-specific additions. When writing, "easy mode" means starting from one of these proven structures rather than inventing from scratch.

---

**Where to go next:** `writing-a-hook.md` to use what the research turned up.
