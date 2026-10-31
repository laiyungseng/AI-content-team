---
type: run
run_id: YYYY-MM-DD_HHMM
platforms: []              # enabled platforms collected
counts: {competitor_items: 0, our_items: 0, failed_accounts: 0}
window: 90d
status: draft              # draft | approved
report_url:
approved_at:
---
# Run YYYY-MM-DD_HHMM

## Layout
```
raw/<platform>/         collector output, untouched
media/                  downloaded images
items.tsv               normalised data (owner accountId platform itemType itemId date views likes comments shares saves durationSec topic pillar caption mediaUrl permalink status)
analysis/verdicts.md    Adapt / Copy / Ignore per competitor item
analysis/ours.md        our baseline
analysis/comparison.md  us vs them, strategy, positioning
report.html             built artifact
```

## Sources used
(snapshot of the Enabled platforms and Active URLs at run start)

## Problems
(tool failures, missing fields, private accounts)

## User overrides
(verdict changes and comments; copied to `memory/_system/skill_feedback/`)

## Promoted to memory
(PAT / FAIL / LRN ids, or "none")
