---
type: reference
status: active
source: content-performance-dashboard/SKILL.md (adapted: Ours baseline from items.tsv via to_perf_tsv.py, no separate Apify pull)
copied: 2026-10-31
related: [[output_schema]], [[stats_rules]], [[writing_insights]]
---
# Optional: Ours performance dashboard (Instagram + TikTok)

Used by performance_analyst for the "Ours" baseline when we have an active Ours account on **both** Instagram and TikTok.
Otherwise skip it and use `normalise.py stats <run>`. Also the Phase 5 weekly/monthly snapshot.

The page is finished code in `assets/perf_template.html`; a run supplies data and written insights. It is a static
snapshot: no `db`, no refresh button. Fresh numbers mean a new run republished to the same URL.

## Rules
- Do NOT open, read or edit `perf_template.html`. `perf_build.py` writes the config block.
- Do NOT write your own analysis code. `perf_build.py analyze` prints what the insights need, computed as the page computes it.
- At most 5 topics plus `uncategorized`; keep topic keys identical across snapshots so topic performance stays comparable.
- Instagram photo and carousel posts have no views: never compare their reach with a video's; compare photos only with each other, by likes and comments.
- Never write 0 for a missing number (see `output_schema.md`).

## Steps
1. Adapt: `uv run python scripts/to_perf_tsv.py <run> <run>/perf`
2. Analyse: `uv run python scripts/perf_build.py analyze <run>/perf/config.json <run>/perf/posts.tsv`
   It lists every post with a view count ranked by outlier score with quadrant and topic, the quadrant counts and the topic ranking.
   The top and bottom of each list are the top-five vs bottom-five comparison: read their full captions and find what separates them.
3. Read `shared/frameworks/writing_insights.md`, then fill `insights` in `<run>/perf/config.json`:
   ```json
   "insights": {
     "headline": "One paragraph: the single most useful thing found, ending in what to do this week.",
     "quadrants": {
       "instagram": {"both": "", "reach_only": "", "eng_only": "", "neither": ""},
       "tiktok":    {"both": "", "reach_only": "", "eng_only": "", "neither": ""}
     },
     "topics": {"instagram": "Why the top topic wins here.", "tiktok": ""}
   }
   ```
   An empty string falls back to the page's generic copy, which is right when there is nothing grounded to say.
4. Build: `uv run python scripts/perf_build.py build <run>/perf/config.json <run>/perf/posts.tsv <run>/perf/performance.html`
   If it prints `FAILED`, fix the named row or field and rerun.
5. Publish with no capabilities. On a refresh pass the previous dashboard's `url`; never hand over a second link.
   To recover an older dashboard's handles and topics verbatim: `uv run python scripts/perf_build.py reuse <read index.html> <run>/perf/config.json`.

Hand over as a snapshot of the run's window. Changing the page itself: read `shared/frameworks/stats_rules.md` and `stats_maintenance.md` first,
render once after any template edit, fix what that shows, and stop.
