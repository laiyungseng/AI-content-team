---
type: reference
status: active
source: competitor-content-radar/SKILL.md (adapted: data from items.tsv via to_radar_tsv.py, no separate Apify pull)
copied: 2026-10-31
related: [[output_schema]], [[stats_rules]]
---
# Optional page 3: performance radar (Instagram + TikTok)

A separate static artifact linked from the report summary. One tab per account, plus Head to Head and Topics & Gaps
when there are 2+ accounts, and a Playbook tab. Meta and XHS items are not shown (the dashboard supports IG/TikTok only).

The page is finished code in `assets/radar_template.html`; a run only supplies data. Collection already happened in
the run (step "collect"), so there is **no extra Apify pull** here.

## Rules
- Do NOT open, read or edit `radar_template.html`. `radar_build.py` injects into it.
- Do NOT write JSON or tagging scripts by hand. The adapter writes `config.json` + `posts.tsv` from `items.tsv`.
- Do NOT use `db`. Publish with `capabilities: {}` (explicitly empty), also on refresh: an older copy with `db` would otherwise show cached data.
- Topics come from the `sources.md` Topics table (4-6 shared keys, stable across runs). Items without a topic become `uncategorized`.
- Null rules from `output_schema.md` apply: empty means missing, never 0. Private / failed / empty accounts stay in with a status.

## Steps
1. Adapt: `uv run python scripts/to_radar_tsv.py <run> <run>/radar`
2. Build: `uv run python scripts/radar_build.py <run>/radar/config.json <run>/radar/posts.tsv <run>/radar/radar.html`
   If it prints `BUILD FAILED`, fix the named line (usually in `items.tsv`) and rerun. It ends with post counts per account and topic.
3. Publish `radar.html` with the Artifact tool, `capabilities: {}`. On a refresh, pass the previous radar's `url` so the link stays the same.
   To recover an older radar's accounts and topics: `uv run python scripts/radar_build.py --reuse <read index.html> --out-config <run>/radar/config.json`.
4. Link the radar URL from the report summary and record it in `run.md`.

## Hand-over (plain words, no statistical terms)
- Which accounts are in, and any that could not be pulled and why.
- Which topics have too few posts to judge (under 4 video posts for an account) and what would fix it (a wider window in `sources.md`).

Changing the page's design or logic: read `shared/frameworks/stats_rules.md` first (it holds the radar's analysis and validation rules).
