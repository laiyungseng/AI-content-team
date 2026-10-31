---
type: reference
status: active
---
# Us vs them method

Input: `items.tsv`, `analysis/verdicts.json`, `analysis/ours.json`. Output: `analysis/comparison.json` (schema in `output_schema.md`).

## Rules
- Compare like with like: ratio to own typical, engagement per 1,000 viewers (likes + comments), cadence, consistency. Never raw views or followers across accounts ([[stats_rules]]).
- Quote the post counts behind every claim (`postCounts`). Small samples: "too early to call".
- No Ours data: rows say "no baseline yet" and strategy is limited to what competitors do.
- Meta ads: compare creative approach and longevity only. State how complete the ad list is: the coverage estimate from the last discovery audit if there was one, otherwise "ad list may be incomplete: the Ad Library returns the newest ads first". Never write "all ads" or "100%".

## Rows (one per dimension)
hook, format, visual, message, offer, CTA, cadence, engagement. Per row: what we do (ours), what they do (theirs), who is stronger (`ours|theirs|similar|unclear`), why, how we implement it. "Why" cites evidence; "how" is something the production team can do.

## Topic coverage
No separate field in `comparison.json`: put a whitespace or saturated finding in a strategy item or the headline, with its post counts.
Use the shared topics from `sources.md`. Whitespace = a topic working for competitors and unused by us. Saturated = every competitor with 4+ posts is below its usual. Anything else: "too early to call".

## Winning hooks (Meta ads)
Adapted from the winning-hook ranking in the UPT ad-intelligence method. Run `build_report.py winning <run>`; it ranks each advertiser's identical ad texts by copies x days running (`analysis/winning_ads.json`). Longevity is the only performance signal Meta gives ([[meta]]), so this is a hypothesis, not proof. Take the top rows (up to 10), and for each write the `winningHooks` entry: the hook in our own plain words, the advertiser, the scale ("12 ads, running 64 days"), its `hookType`, and `reuse`:
- `yes`: any advertiser could use the angle.
- `partly`: the angle works but needs our own proof or offer.
- `no`: it rests on something we do not have (a personal following, a licence, a very large budget).
Never copy their wording. Skip rows whose text is an unfilled template such as `{{product.brand}}` (catalogue ads). If the run has no Meta ads or no running days, omit the section.

## Devil's Advocate (write last)
Adapted from the same method. After the rows, strategy and winning hooks are written, switch sides: act as someone who has worked this market for five years and list 3 to 5 places where the data could mislead us. Each item has three parts: `misread` (how a newcomer would read it), `truth` (what the data supports), `adjust` (what we do differently). Ground each in this run's counts. Typical traps:
- Many ads is not the same as selling well: an advertiser may be testing many creatives or have a big budget.
- A long-running ad may be a lead-capture ad for a different product, not the product it shows.
- A high ratio on a small account is one post, not a pattern.
- A format that works for a competitor because of their following will not work for us without it.
- A topic that looks empty may be empty because it does not sell.
If an item has no evidence in this run, drop it; fewer than 3 is fine when the data is thin, say so.

## Strategy and positioning
- Strategy: 3 to 5 items, each with a "Do next". Respect the mix 70% proven / 20% adjacent / 10% experimental ([[experimentation]]) and tag each Educate / Engage / Promote.
- Positioning: one statement of where we can stand apart, the gaps competitors leave, what to avoid.
- Headline: one paragraph, ends with "Do next: ...".
