---
type: framework
status: active
source: competitor-content-radar/references/maintainer-notes.md + content-performance-dashboard/references/design-notes.md (maintenance parts moved to stats_maintenance.md)
copied: 2026-10-31
---
# Statistics rules (one rule per metric)

Required reading for every analyst agent. Findings are written following [[writing_insights]]. Plain-language and "Do next:" rules below apply to **our report** as well as the dashboards. Changing a dashboard page or its analysis logic: read [[stats_maintenance]] first; a normal run never needs it.

## Rules that apply everywhere in this project
- Empty = missing, never 0. Photo posts have no views; Instagram has no shares or saves. Exclude, never zero-fill.
- Quote the post count beside every score. Small samples (20-40 posts): say "too early to call", never fabricate a pattern.
- Compare within an account first (ratio to its own typical), across accounts only with like-for-like measures.
- Posts at 10x+ their own typical are flagged, never presented as a pattern to copy.
- Every insight ends with "Do next: ...", including "nothing to act on yet".
- No jargon on the page (banned words and replacements below).

## Where the two dashboards differ (and which one the report uses)
| Metric | Radar (competitors, page 3) | Performance dashboard (ours, baseline) | Report rule |
|---|---|---|---|
| Baseline | account median of the pulled window | platform all-time (unfiltered) median, stable under filters | competitors: window median; ours: stable all-time median |
| Engagement | (likes + comments) / views x 1000 | (likes + comments + shares + saves) / views; core (likes + comments) on the cross-platform tab | always core (likes + comments) when comparing ours vs theirs or IG vs TikTok |
| Hit | ratio >= 2 | views >= 2x stable median | ratio >= 2 |
| Anomaly | ratio >= 10, flagged | not flagged | ratio >= 10, flagged |
| Topic verdict | median of ratios, with a check (target spec; shipped template still uses fixed cutoffs) | topic ranking by outlier score | median of ratios; fewer than 4 posts = "need more posts" |
| Recency | Date range from `sources.md` | 7/30/90 window; prior period = equal window before | Date range from `sources.md` |

Platform coverage: both dashboards support Instagram + TikTok only. Meta Ad Library and XHS data appear on report pages 1-2 but not yet in the dashboards.

## Words that never appear on the page
The reader is a marketer
deciding what to film next week. Banned in user-facing strings (code comments
only): p-value, `p=`, permutation, bootstrap, confidence band/interval,
significant/statistically, Benjamini-Hochberg, FDR, false-discovery,
correlation/Pearson, variance, standard deviation, percentile, resampling,
sample size, distinguishable, "random variation", "random draws", "evidence
bar", "holds up", "could be luck", and the bare words median, outlier score,
scorable.

| Instead of | Write |
|---|---|
| median views | typical views |
| outlier score 2.5x | 2.5x their usual reach |
| statistically significant | worth acting on |
| not significant | too early to call |
| n < 4 | need more posts |
| p = 0.03, confidence band | (omit) |
| within random variation | inside the normal swing between their posts |
| minimum detectable effect | how much this window can show |

## Definitions in plain words
- Ratio to own typical = a post's views divided by that account's own median views in the window. Empty for posts with no views.
- Topic or dimension score = the median of those ratios.
- Engagement per 1,000 viewers = (likes + comments) / views x 1000. Shares and saves are never added in.
- Hit = ratio of 2 or more. Anomaly = ratio of 10 or more. Consistency = share of video posts at or above their usual (ratio 1 or more). Ceiling = best ratio. Cadence = mean posts per week over the pulled history.
- Topics: Proven = clearly ahead for 2 or more accounts. Owned = clearly ahead for exactly one. Whitespace = clearly working for a competitor and unused by us. Saturated = every account with enough posts is below its usual, with 4 or more posts across the field. Too early to call = everything else, with the reason.

# Part B - Performance dashboard statistics (ours)


- **Posts with no view count never enter view-based numbers.** Instagram
  returns no `videoPlayCount` for photo and carousel posts, so their `views`
  is null. `hasViews()` / `withViews()` keep them out of the baseline, outlier
  scores, hit rate, quadrants, length buckets, the bar chart, topics and the
  All tab's view and engagement comparisons. They still count in "Posts in
  view" and appear in the table with "-" for views and score, and the tab
  says how many were left out. An earlier version treated null as 0, which
  dragged the typical post down and inflated every video's score. Any new
  section that uses views must take `withViews(posts)`.
- **Stable baseline**: outlier scores and hit-rate thresholds use each
  platform's all-time (unfiltered) median, never the filtered subset's. The
  baseline should not shift under the user as they change filters.
- **Outlier score** = post views / stable median views. **Hit** = at or above
  2x that median.
- **Prior period** = the equal-length window immediately before the current
  filter's start. On a 7-day pull it is always empty, so the hit-rate section
  falls back to a no-comparison message - correct behavior, and the argument
  for pulling 30 or 90 days.
- **Reach** = views >= stable median views. **Engagement** = (likes +
  comments + shares + saves) / views >= the stable median of that rate.
  Instagram structurally has no shares or saves, so the cross-platform "All"
  tab uses core engagement (likes + comments) for both platforms, labeled as
  such, to keep the comparison fair.
- **Video length buckets**: <45s / 45-70s / >70s, fit to one account's
  distribution. Re-derive them if a new creator's data clusters differently.
