---
type: methodology
name: content_scoring
status: active
---
# content_scoring

**Purpose:** Score content pieces consistently so patterns can be compared across accounts and runs.

## Process
1. **Reach score**: ratio = the item's views / that account's own typical views in the window (median of its scored posts). Never compare raw views across accounts ([[stats_rules]]).
2. **Engagement score**: (likes + comments) / views x 1000, compared with the account's own typical. Shares and saves are shown but never folded in (Instagram does not return them).
3. **Tier** (reach ratio): 10x or more = anomaly (inspect, not a pattern); 2x to under 10x = hit; 1x to under 2x = typical-plus; under 1x = below usual.
4. **No views** (Meta ads, photo posts, some XHS): no reach score. Use likes + comments against the account's other no-view posts, or ad longevity and variants. State "no reach data".
5. **Confidence**: one rule, defined in `.claude/skills/competitor-intelligence/references/verdict_rules.md`: low under 5 scored posts ("need more posts"), medium 5 to 14, high 15+ and a second run or our own validation.

## Output schema
Per item: `ratio`, `tier`, `engagementPer1000`, `confidence`. The report shows the ratio as "2.5x their usual reach".

## Good / bad examples
- Good: "8.5x their usual reach (account has 8 scored posts); inspect before copying."
- Bad: "197k views, so it is a winner" (raw views, no baseline).
