---
type: reference
status: active
---
# Which items go into the report

Page 1 shows a limited set so the page stays usable and the published file count stays under the artifact limit.

1. Per competitor account: top 6 by ratio to its own typical views, the 2 weakest, up to 2 posts with no views (most likes and comments first), and every anomaly (ratio >= 10, flagged). The cap of 8 per account never drops an anomaly.
2. Ads: active ads running longest first, then most recent, up to 8 per advertiser.
3. Items with no metrics (ads, photo posts with no views) are ranked by recency and likes/comments, and labelled so.
4. Maximum 120 cards in total (images are published as files; the limit is 255 files). If the cap bites, the page says which accounts were trimmed.
5. Every collected item stays in `items.tsv`; selection only affects what the report shows.

`build_report.py select` implements this and writes `analysis/selected.json`; verdicts exist only for selected items. Hook study in depth: [[hook_research]].
