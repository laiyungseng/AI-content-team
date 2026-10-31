---
type: methodology
name: performance_analysis
status: active
---
# performance_analysis

**Purpose:** Decide whether content beat its own baseline rather than just having big reach. Statistics rules: [[stats_rules]].

## Metrics
Views, likes, comments, shares, saves, followers, engagement per 1,000 viewers, ratio to own typical views, cadence, consistency. Raw views and follower counts are context only, never a comparison between accounts.

## Process
1. **Baseline**: typical views = median views of the account's scored posts in the window (`normalise.py stats`). Fewer than 4 scored posts: "need more posts".
2. **Per post**: ratio to typical; engagement per 1,000 viewers; flag ratio >= 10 as anomaly.
3. **Per topic** (ours): median ratio for topics with 4 or more scored posts; others "too early to call".
4. **Cadence**: posts per week over the window; name a direction only with 8 or more weeks of history.
5. **Consistency**: share of scored posts at or above typical.
6. Photo/carousel posts without views are compared with each other by likes and comments only.
7. Optional dashboard for Ours on both Instagram and TikTok: `perf_build.py analyze` then write the insights.

## Output schema
`analysis/ours.json` (see `output_schema.md`): summary, per-account posts, typicalViews, bestTopic, notes, missing.

## Good / bad examples
- Good: "Their reels run 1.6x their usual reach on 'tips' (6 posts), ours 0.9x (5 posts). Do next: test one tips reel."
- Bad: "Rival has 20x our views." (account size, not performance).
