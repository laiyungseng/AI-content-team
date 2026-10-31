---
source: UPT-course-setup-v2.skill / course-skills/fb-competitor-census-mcp-15m/SKILL.md.packed
original-skill: fb-competitor-census-mcp-15m
copied: 2026-10-31
status: staged
destination: competitor_discovery.md + source-manager discover mode (plan step 11d)
---
# FB Competitor Census — Meta MCP 15m

Produce one evidence-bounded competitor list. Optimize for discovery coverage, correct Page identity, verified active-ad counts, and a short runtime. Do not generate strategy analysis, HTML, Google results, or creative teardown.

## Scope

Include only advertisers discoverable through Meta Ad Library in the target country and industry.

Extract:

- industry
- country, default `MY`
- region, default Malaysia nationwide
- seed competitors, optional
- output path, default:
  `competitor_analysis/projects/[project]/discovery/YYYY-MM-DD_{industry-slug}-meta-competitors.md`

State that this is an Active Advertiser census, not a directory of every business in the industry.

## Tool boundary

Discover the read-only Meta Ads MCP capability named `ads_library_search`; its full name may vary. Inspect the exposed schema and adapt parameter names without inventing fields.

Use only:

- keyword searches with `search_terms`
- Page-specific searches with `page_ids`
- read/write tools for one Markdown output

Do not use Google, Firecrawl, Chrome, Computer Use, Playwright, campaign/account mutation tools, or another data source. If `ads_library_search` is unavailable or authentication fails, return `Unavailable`, name the failure, and stop. Do not silently substitute another source.

Common search shape:

```text
ads_library_search(
  search_terms="[query]",
  countries=["MY"],
  ad_active_status="ACTIVE",
  limit=25
)
```

Common count-verification shape:

```text
ads_library_search(
  page_ids=["[page_id]"],
  countries=["MY"],
  ad_active_status="ACTIVE",
  limit=1
)
```

## Runtime budget

Target 15-20 minutes. Treat 25 minutes as the normal upper bound for a dense market.

Allocate:

1. Query generation and setup: 1 minute.
2. Discovery searches: 6-8 minutes.
3. Deduplication and relevance filtering: 2 minutes.
4. Page-specific count verification: 4-10 minutes.
5. Saturation check and Markdown output: 2-3 minutes.

Prefer completeness and truthful count status over a false hard deadline. Never invent a count to finish faster.

## Step 1 — Build the query grid

Generate 15-20 queries maximum. Cover:

1. Core category terms.
2. Course, academy, class, training, workshop, and certification variants.
3. Simplified Chinese, traditional Chinese, English, and Malay variants relevant to the market.
4. Buyer-language and local Rojak variants.
5. Malaysia and 2-4 useful geographic slices such as KL, PJ, Penang, JB, Sabah, or Sarawak.
6. User-supplied seed competitors.

Start with narrow, high-relevance terms. Use broad terms last. Avoid generating dozens of tool-specific or weak synonym queries.

## Step 2 — Discover candidate Pages

Run the query grid against active ads in the target country.

For every returned ad, capture:

- `page_name`
- `page_id`
- Page URL if returned
- discovery query
- sample ad or library ID if returned
- visible category/relevance evidence

Deduplicate by `page_id`, not Page name.

Classify:

- `Direct`: sells the requested course, training, or closely equivalent offer.
- `Adjacent`: competes for the same learner but the offer is broader or neighboring.
- `Exclude`: unrelated advertiser, foreign-only offer, product seller without training, generic salon, or noise.
- `Uncertain`: evidence is insufficient.

Keep Direct and Adjacent in the final report. Put Uncertain in a separate section. Do not rank Exclude.

Do not treat the number of keyword-result appearances as the Page's active-ad count.

## Step 3 — Verify each Page and count

Query every retained Direct and Adjacent Page separately by `page_ids`.

Before the full count pass:

1. Choose one resolved Page.
2. Compare the count returned with `limit=1` against the count returned with `limit=50`.
3. If the Page-level total is identical, use `limit=1` for count-only probes.
4. If not identical or no total field is returned, use the smallest limit that produces a trustworthy Page-level count.
5. Record this probe in the methodology note.

When the tool surface supports parallel calls, run three independent Page-specific calls concurrently. Do not combine three Page IDs into one query unless the schema explicitly returns a separate total for each Page.

Concurrency rules:

- default: 3
- maximum: 5 only after a successful batch
- on timeout or rate limit: reduce to 2, then 1
- retry each failed Page once after the current batch

For each retained Page, require:

- numeric active-ad count for the target country
- count timestamp
- `Verified` status

If the API field is named `estimated_total_count`, preserve that wording in the report note. Do not rename an estimate as an exact performance metric.

If a Page-specific query fails twice:

- set count to `无法确认`
- set status to `Unverified`
- mark the entire report `Partial`
- do not substitute its keyword sample hits

## Step 4 — Generate links

Use the real Page URL when returned by the tool.

If the real Page URL is absent, use the ID-based link and label it:

```text
https://www.facebook.com/{page_id}
```

Generate the Ad Library Page link:

```text
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country}&view_all_page_id={page_id}&search_type=page
```

Never invent a vanity username.

## Step 5 — Run a Meta-only saturation check

Run three holdout queries that were not used in discovery:

1. one alternate-language term
2. one geographic slice
3. one offer or industry-specific hook term

For each, count relevant unique Pages and newly discovered relevant unique Pages.

Do not divide new Pages by 50 ads. Use:

```text
new relevant unique Pages / all relevant unique Pages in that query
```

Rate saturation:

- `Strong`: the last three queries add at most one new relevant Page in total.
- `Moderate`: they add two to four.
- `Weak`: they add five or more, or a new market/language cluster appears.

Add every newly discovered relevant Page to the verification queue before finalizing.

Do not convert saturation into a fake coverage percentage.

## Step 6 — Sort and write one Markdown report

Sort Direct competitors by verified active-ad count descending. Sort Adjacent separately using the same rule.

Tie-breakers:

1. number of distinct discovery query families
2. Page name alphabetically

Write only one `.md` file with this contract:

```markdown
# {industry} — Meta Ad Library 竞争对手清单

- 国家：{country}
- 数据时间：{YYYY-MM-DD HH:mm MYT}
- 数据范围：Meta Ad Library Active Advertisers
- 排序依据：目标国家 Active Ads 数量
- Direct：{N}
- Adjacent：{N}
- 验证状态：Complete / Partial / Unavailable
- Saturation：Strong / Moderate / Weak

## 一、Direct Competitors

| 排名 | Page Name | Active Ads | Facebook Page | Ad Library | Page ID | 找到来源 | 数量状态 |
|---:|---|---:|---|---|---|---|---|

## 二、Adjacent Competitors

| 排名 | Page Name | Active Ads | Facebook Page | Ad Library | Page ID | 找到来源 | 数量状态 |
|---:|---|---:|---|---|---|---|---|

## 三、待确认候选

| Page Name | Page ID | 发现 Query | 无法确认原因 |
|---|---|---|---|

## 四、搜索覆盖记录

| Query | 相关独立 Page | 新增 Page | 状态 |
|---|---:|---:|---|

## 五、验证与数据边界

- Count probe：limit=1 / fallback 结果
- Active Ads 是目标国家在报告时间的快照。
- Active Ads 多不代表花费、销量、CPL、ROAS 或盈利更高。
- 本报告不包含未投 Meta Ads 的市场公司。
- Meta Ad Library 搜索存在结果数量与排序限制，不能声称 100% 覆盖。
```

## Completion gate

Set `Complete` only when:

- every retained row has Page name
- every retained row has Page ID
- every retained row has Facebook Page link
- every retained row has Ad Library link
- every retained row has a verified numeric count, including verified zero
- sorting uses only Page-specific counts
- three holdout queries are complete

Otherwise set `Partial` and show exactly what is missing.

## Final response

Return:

- clickable absolute path to the Markdown report
- elapsed time
- Direct / Adjacent / Uncertain counts
- saturation rating
- whether the count probe passed
- any unverified Pages

Do not paste the full table into chat unless the user asks.
