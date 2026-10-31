---
type: framework
status: active
source: competitor-content-radar/references/maintainer-notes.md + content-performance-dashboard/references/design-notes.md
copied: 2026-10-31
---
# Statistics rules (one rule per metric)

Required reading for every analyst agent and for anyone changing the report or dashboards. Findings are written
following [[writing_insights]]. Plain-language and "Do next:" rules below apply to **our report** as well as the dashboards.

## Rules that apply everywhere in this project
- Empty = missing, never 0. Photo posts have no views; Instagram has no shares or saves. Exclude, never zero-fill.
- Quote the post count beside every score. Small samples (20-40 posts): say "too early to call", never fabricate a pattern.
- Compare within an account first (ratio to its own typical), across accounts only with like-for-like measures.
- Posts at 10x+ their own typical are flagged, never presented as a pattern to copy.
- Every insight ends with "Do next: ...", including "nothing to act on yet".
- No jargon on the page (banned-word list and replacements in the radar notes below).

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

# Part A - Radar notes (competitors)
## Maintainer notes (read only when changing the template)

A normal data run never needs this file. It applies when the user asks to change
the page's design, copy, or analysis logic.

## Current state of the template (read this before planning any change)

The shipped `dashboard_template.html` is the original version. It works and has
been published many times, but it does NOT yet meet the target spec below:

- Topics & Gaps still uses fixed cutoffs on the AVERAGE per-post ratio (>= 1.2 with a 1.4x gap for "Owned", < 0.95 for "Saturated", >= 1 for "Proven").
- Head to Head names a posting-cadence direction from a Pearson value above 0.25.
- On-page copy uses "Median views", "outlier score" and "median" in many places.
- `computeStats` writes fields onto the shared post objects.
- A hero recommendation still claims the most-used topic is "where the biggest hit came from" without checking it.

None of these exist yet: `assess`, `applyFDR`, `rngFor`, `EVIDENCE`, `DIMENSIONS`,
`detectableLift`, `compareSamples`, `renderDecisionSummary`, a "What to act on"
card, or "too early to call" labels.

Upgrading the template to the target spec is a one-time project. Only do it when
the user explicitly asks for that upgrade. When done, save the result as the new
`dashboard_template.html` (keeping the three placeholders: `__DATA_JSON__`,
`"__PULLED_AT__"`, and `<title>Competitor Content Radar</title>`), and delete this
"current state" section.

## Target spec: the two rules that matter most

**1. The page only recommends what the data supports.** With 20 to 40 posts per
account there is very little signal. Every difference (a topic ahead, a length
working, reach moving) is checked against that account's own posts before it is
shown. Differences that do not hold up show as "too early to call". The page
states how big a difference this window could even reveal.

**2. None of that machinery is named on the page.** The reader is a marketer
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

## Why fixed thresholds are wrong

Measured on simulated accounts with no real effect: "Proven" fired on 84% of
noise topics, "Owned" on 52%, "Saturated" on 1%, "heating up / cooling down" gave
a direction on 77% of flat accounts, and the cadence read named a direction on
80% of accounts with no relationship.

Two root causes:

1. **Averaging per-post ratios is upward-biased** (views are roughly lognormal, so a no-effect topic averages about 1.65x). Use the median of per-post ratios; it centres at 1.0.
2. **Hit rate measures spread, not level.** Period-over-period growth must compare typical views between the two windows. Hit rate stays as a shape check only.

Target behaviour: about 5% of pure-noise accounts get any recommendation, while a
real 3x topic lift is caught about 77% of the time at 60 posts per account.

## Target spec: non-negotiable rules

- Never fabricate a number. A metric a platform did not return does not appear, not as 0 and not as blank. Instagram never returns shares or saves. A metric available for only some accounts is excluded from cross-account views.
- Never state a relationship the code did not test.
- Medians, per account, never pooled. Every ratio is a post's views over that same account's typical views for the window.
- No recommendation without a check, corrected for the number of questions asked (about 20 per account: topic, length, day, caption length, opener). New analyses go into `DIMENSIONS`, never as a bespoke card with its own threshold.
- Flag confounded findings that rest on 60%+ of the same posts.
- Always state how much the window can show.
- Cross-account comparisons use like-for-like measures only (ratio to own typical, engagement per 1,000 viewers, cadence, consistency), never raw views or followers. Example posts are picked by ratio, not raw likes.
- Quote the scored post count (video posts only) beside a score.
- Every insight ends with "Do next: ...", including "nothing to act on yet".
- Posts at 10x+ their own typical are flagged for inspection and never presented as a pattern to copy.
- Never mutate `LIVE_DATA.posts`; work on copies.
- Verdicts are deterministic: all resampling uses a generator seeded from the data.

## Metric definitions (internal vocabulary)

- Ratio to own typical = views / the account's own median views in the window. Null for posts with no views.
- Topic or dimension score = median of those ratios.
- Engagement per 1,000 viewers = (likes + comments) / views x 1000. Shares and saves never folded in.
- The check = two-sided permutation test of a subset's median against the account's own pool, plus a bootstrap interval. `real` maps to "worth acting on", `unproven` to "too early to call", fewer than 4 posts to "need more posts". Alpha 0.10. Actionable = `real` AND the interval clears 1x.
- Correction = Benjamini-Hochberg across one account's scan.
- How much the window can show = 90th percentile of medians from resampled groups of typical size.
- Hit = ratio >= 2. Anomaly = ratio >= 10. Hit rate = hits / video posts (shape check only).
- Period-over-period = permutation comparison of median views, current vs prior equal-length window.
- Consistency = share of video posts with ratio >= 1. Ceiling = best ratio. Cadence = mean posts per week over full pulled history; a direction is named only with 8+ weeks and a passing check.
- Reach vs engagement quadrants use a +/-15% display band around the account's own typical values; describe the split, never diagnose a cause.
- Topics & Gaps: Proven = clearly ahead for 2+ accounts. Owned = clearly ahead for exactly one. Whitespace = clearly working for a competitor, unused by the `isMine` account. Saturated = every judgeable account clearly below its usual, 4+ posts across the field. Too early to call = everything else, listed with the reason.

## Validation required after ANY template change

Build a test page with `scripts/build.py` first. For a design or copy change,
run checks 1, 2 and 5. Checks 3 and 4 also apply to any change to the analysis
logic, and to the upgrade (the current template fails both by design, see above).

1. **Syntax**: `build.py` already runs `node --check`.
2. **Smoke test (jsdom)**: load with `runScripts: 'dangerously'`, stub `window.claude.use` to throw, listen for errors, click every `.tab-btn`, each date range (7d, 30d, custom), the account and platform filters, and a table sort. Assert zero errors and no `NaN`, `undefined` or `[object Object]` in `.wrap` text. Render the same tab twice and assert identical text. If real data has one account, add synthetic data with 2+ accounts, mixed platforms, one with shares/saves, one `private`.
3. **Plain-language scan**: every leaf element in `.wrap`, all tabs, narrow and wide ranges, against the banned list above.
4. **Behaviour on synthetic data**: about 200 lognormal accounts with random topics must get a recommendation well under 10% of the time; a planted lift on one topic must be found and attributed correctly.
5. **One visual pass (Playwright)**: topbar, an account tab, Head to Head, Topics & Gaps, Playbook. Fix what is wrong once, re-shoot only the fixed area. Blocked Google Fonts locally is expected.

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


