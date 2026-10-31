---
type: reference
status: active
source: account status rules copied from competitor-content-radar
---
# Run requirements

## Before collecting
1. `sources.md` synced (source-manager); at least one Enabled platform with an Active row.
2. Apify MCP authorised (`/mcp`). Without it, stop and tell the user.
3. A brand guideline is **not** required (onboarding deferred). If `brand/<project>/` has one, read it for positioning in the comparison.
4. Topics defined in `sources.md` (4 to 6). If empty, derive them from the first captions, ask the user to confirm, and save them via source-manager before tagging.
5. At least one **Ours** account on an enabled platform, else page 2 says "no baseline yet" and the run is competitor-only.

## Account status (kept, never dropped)
| status | meaning |
|---|---|
| ok | posts returned |
| private | account is private |
| failed | actor error or not found |
| empty | no posts in the window |

Write non-ok statuses to `raw/<platform>/status.json` as `{"handle": "private", ...}`; `normalise.py` also marks any target with zero items as `empty`. These rows appear in `items.tsv` with an empty itemId and the reason in `caption`, and the report lists them in a "Could not read" box.

## Hand-over
Tell the user in plain words: accounts in, accounts that could not be read and why, topics with too few posts (under 4 per account) and what would fix it (wider window, more posts).
