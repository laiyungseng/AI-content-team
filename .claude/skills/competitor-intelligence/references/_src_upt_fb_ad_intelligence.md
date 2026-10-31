---
source: UPT-course-setup-v2.skill / course-skills/fb-ad-intelligence-mcp/SKILL.md.packed
original-skill: fb-ad-intelligence-mcp
copied: 2026-10-31
status: staged
destination: competitor_discovery.md, Meta section of platform_scraping.md, comparison_method.md (plan step 11b, 11c)
---
# Skill: FB 广告竞争情报挖掘（MCP 版 v3）

> **v3 升级日志（2026-06-12）：**
> - ⭐ **Orchestration Mode（默认）**：用户给 1 次指令，主 Claude 自动 Agent tool 串联 6 个 sub-agent 跑完整流程，每个 sub-agent 独立 session（等同开新 chat），不超 context
> - 模型策略：sub-agent 不显式传 model 参数，**自动继承 main session 的 model + context window**（用户跑 Opus 4.7 1M → sub-agent 都是 Opus 1M；跑 Sonnet 4.6 → sub-agent 都是 Sonnet）
> - 每阶段加 sub-agent prompt template + JSON 返回总结格式（让主 Claude 决策下一步）
> - 失败 / 异常处理：sub-agent 报错 → 主 Claude 停，报告用户；Coverage Audit 未饱和 → 自动重跑阶段 2.5（最多 3 轮）
> - 保留 v2 兼容：用户说「跑阶段 X」「手动模式」→ 主 Claude 不串 sub-agent，直接自己跑指定阶段
>
> **v2 升级日志（2026-06-12 早）：**
> - 修正关键字策略：narrow query 优先（API 是 recency-sorted，宽词只能拿最新 50 条，tail 必漏）
> - 新增阶段 2.5 Hook 反查 + 滚雪球（解决 [example competitor] 类被漏抓的结构性盲区）
> - 阶段 4 分 Breadth Pass + Depth Pass 两层（130+ 浅档案 + Top 10-15 深度策略分析共存）
> - 加入 5 Lens 策略点拆框架 + Devil's Advocate 章节 + Winning Hook 投放规模榜
> - 通用化机会点（8 framing 模板 + 2x2 市场空白矩阵，禁止预设任何客户名 / IP 名）
> - 加入 Coverage Audit 步骤，HTML 输出估算覆盖率 % 而不是吹「100% 覆盖」
> - 阶段 5 HTML 升级暗色主题（参照参考报告 CSS）
>
> **v1 → v3 兼容性：** v3 是 orchestration 大改。所有阶段的产物文件名 / 格式与 v2 兼容。手动模式仍可用 stage 参数跳阶段。

---

## 触发条件

**必须用户明确点名 MCP / API / Ad Library 工具才触发**。例如：
- "用 ad library MCP 跑 [行业] 的 FB 广告情报"
- "用 ad library API 帮我挖 [行业] 竞争对手"
- "用 Meta Ads MCP 跑 FB 广告情报"
- "fb-ad-intelligence-mcp [行业]"
- "/fb-ad-intelligence-mcp"
- "用 API 跑 ad library [行业]"

⚠️ 关键规则：
- 用户**只说**"帮我跑 FB 广告情报 / 帮我挖 FB 对手"等泛用句 → **走旧版** [`/fb-ad-intelligence`](./fb-ad-intelligence.md)（Chrome 手动版覆盖率最完整）
- 用户句子里**明确出现** `MCP` / `API` / `ad library` 任一关键词 → **走本 MCP v2 版**
- 模棱两可时反问一句："用 MCP 跑（快但 ~85% 覆盖率）还是 Chrome 跑（慢但 100%）？"

---

## 工具依赖
- **Meta Ads 的 `ads_library_search` 能力** — Ad Library 广告 metadata
  - ⚠️ **工具全名会因人而异**。每台电脑连 Meta Ads 连接器后拿到的前缀不一样
    （可能长得像 `mcp__meta-ads__ads_library_search`，也可能是一串编号
    `mcp__<一串英数字>__ads_library_search`）。
  - **做法**：在当前可用工具里找名字带 `ads_library_search` 的那个来用，
    读它自己的参数说明再调，**不要凭记忆硬写参数名**。
  - 找不到 = Meta Ads 连接器没接上 → 叫用户跑 `/course-setup-v2` 接一次，不要换别的资料源硬凑。
  - 用 `search_terms` 跑关键字 / hook 反查
  - 用 `page_ids` 反查指定 page 全部 active 广告（绕过 50 limit）
- `mcp__firecrawl__firecrawl_search` — Google 搜索补漏
- `Write` / `Edit` / `Read` / `Bash` — 文件读写

**绝不用** Computer Use、Chrome MCP、Playwright（除非 MCP 全部失败再回退旧版）。

---

## 输入参数（从用户消息中提取）
- **industry**: 行业名称（例：汽车隔热膜、AI 培训、商业贷款）
- **region**: 目标地区（默认：马来西亚 KL，ISO-2 用 MY）
- **seed_competitors**: 已知竞争对手名称（可选，1-3 个）
- **stage**: 要执行的阶段（1/2/2.5/3/4/5，不填则从阶段 1 开始）
- **industry_context** ⭐ v2 新增（可选）: 用户可注入背景 context（例："我们是营销代理公司" / "目标客户是 SME 老板" / "我们想做 B2B HRDF 培训"）。**只用于辅助识别哪些机会点对用户更相关**，绝不预设具体客户名 / 个人 IP 名。**若用户没填则完全通用模式**。

---

## ⚠️ 核心认知：MCP API 的硬限制（必须接受）

Meta Ad Library API `ads_archive` endpoint 的结构性限制：

| 限制 | 影响 |
|------|------|
| **每次 search_terms 最多返 50 条** | 文档硬上限，不可绕过 |
| **不支持 offset / cursor 分页** | 不能翻页拿后面的结果 |
| **不支持 date range filter** | 不能按时间分窗采样 |
| **结果按 `ad_creation_time` 倒序**（recency） | 老广告即使关键字命中也进不了 top 50 |

**这意味着：**
- 用「AI 课程」（估算 870 条命中）只能拿最新 50 条 → 漏 820 条
- 用「AI 培训」（估算 429 条命中）只能拿最新 50 条 → 漏 379 条
- **同一关键字命中的越多 = tail 漏抓越多**

**关键字策略反直觉：**
- 错的方向（v1）：宽词优先拿大覆盖
- 对的方向（v2）：**narrow query where `estimated_total_count` < 50** 才能拿完整集 → 包括 tail 对手

---

## ⭐ Orchestration Mode（v3 默认 — 主 Claude 必读）

**核心规则：** 用户调用本 skill 时，主 Claude **不要自己跑流程**。立刻 Agent tool 串联 6 个 sub-agent，每个跑一个阶段，主 Claude 是 orchestrator 不是 executor。

### 为什么这么设计

每个 sub-agent 是独立 Claude session = 等同「开新 chat」，自己有 200K-1M context window。主 Claude 只看 sub-agent 返回的简短 JSON 总结（每个 ~200 字），所以：
- ✅ 用户 1 次指令 → 全流程自动跑完，不用手动开 6 次 chat
- ✅ Sub-agent 各自 fresh context，不会因为流程长爆 context
- ✅ 主 Claude 自己 context 不爆（只看 6 个 200 字总结 = 1200 字）

### 执行流程（主 Claude 必照做）

```
用户："用 ad library MCP 跑 [行业] FB 广告情报"
  ↓
主 Claude：
1. 解析 input：industry, region (default MY), seed_competitors, industry_context (optional)
2. industry_slug = 把 industry 转可做文件夹名（去空格特殊符）
3. Bash: mkdir -p competitor_analysis/projects/[project]/discovery/{industry_slug}/
4. Agent tool 调 sub-agent 1（阶段 1）：
   - subagent_type: "general-purpose"
   - 不传 model 参数（继承 main session 1M）
   - prompt: 阶段 1 sub-agent prompt template（见阶段 1 末尾）
5. 等返回 → 解析 JSON summary → 验证 status="complete" + keywords_count>50
   - 失败 → 报告用户停下
   - 成功 → 进 sub-agent 2
6. Agent tool 调 sub-agent 2（阶段 2，含 Coverage Audit）
7. 解析返回 → 看 coverage_estimate < 85% 或 audit_new_pct > 10% → 立刻调 sub-agent 2.5
   - coverage_estimate ≥ 85% AND audit_new_pct ≤ 10% → 可跳过 2.5 直接进 3
8. Agent tool 调 sub-agent 2.5（Hook 反查滚雪球）
9. 重复 sub-agent 3 / 4 / 5
10. 最后报告用户：「跑完了，HTML 在 competitor_analysis/projects/[project]/discovery/{slug}/竞争情报报告.html」
   - 附上各阶段 metric 一行总结（如「78 关键字 / 95 对手 / 5 个 Hook 反查新发现 / Coverage ~87%」）
```

### Model 策略

**任何阶段都不传 `model` 参数**。Agent tool 文档：「Default to omitting it — the agent inherits the main-loop model」。

- 用户 main loop 是 Opus 4.7 1M → sub-agent 都是 Opus 4.7 1M
- 用户 main loop 是 Sonnet 4.6 → sub-agent 都是 Sonnet 4.6
- Sonnet 4.6 或 Opus 4.7 都够跑阶段 2 最重的工作（71 keywords × 50 ads JSON），1M context 撑得下

### 失败 / 异常处理

| 情况 | 主 Claude 怎么做 |
|------|----------------|
| Sub-agent JSON summary 含 `status="error"` | 报告用户错误细节，等用户决定（重试 / 跳过 / 改方向） |
| Sub-agent 返回不是合法 JSON | 当成错误处理，报告用户 |
| Coverage Audit `audit_new_pct > 10%` | 重跑阶段 2.5（最多 3 轮）— sub-agent 2.5 prompt 加「这是第 N 轮重跑」context |
| 阶段 2 sub-agent 报「API timeout 多次」 | 报告用户，建议手动 retry 或回退 Chrome 版 |
| 任何阶段超过 30 分钟无返回 | 主 Claude 报告 timeout 风险，等用户决定 |

### 手动模式（v2 兼容，不走 orchestration）

用户明确说「跑阶段 2.5」「stage 4 only」「我要手动分段跑」「stage=4」→ 主 Claude **不调 sub-agent**，直接自己跑指定阶段（按下面阶段 X 的描述跑）。

---

## 产物文件结构（所有阶段共用）

```
competitor_analysis/projects/[project]/discovery/{行业名}/
  ├── keywords.md              ← 阶段 1 产出
  ├── competitors_raw.md       ← 阶段 2 产出（含 Coverage Audit）
  ├── competitors_hook.md      ← 阶段 2.5 产出
  ├── competitors_full.md      ← 阶段 3 产出
  ├── report.md                ← 阶段 4 产出（Breadth + Depth 双层）
  └── 竞争情报报告.html         ← 阶段 5 产出
```

**执行时间估算（每阶段 sub-agent 跑）：**
- 阶段 1：关键字生成（3-5 分钟）
- 阶段 2：narrow 优先关键字搜索 + Coverage Audit（10-15 分钟）
- 阶段 2.5：Hook 反查 + 滚雪球（8-12 分钟，可能重跑 2-3 轮）
- 阶段 3：Google 补漏（5 分钟）
- 阶段 4：Breadth Pass + Depth Pass（15-20 分钟）
- 阶段 5：HTML 报告（5 分钟）

**总时长：** Orchestration 模式 ≈ 45-70 分钟自动跑完

---

## Sub-agent Prompt 通用框架（v3 — 主 Claude 调 Agent tool 时用）

主 Claude 在 Orchestration 模式下，每阶段调 Agent tool 时把以下 prompt 填模板传给 sub-agent（**不传 model 参数**，让 sub-agent 继承 main session model + context）：

```
You are an independent sub-agent for fb-ad-intelligence-mcp v3 skill, Stage {N} ({阶段名}).

## Read first
1. .claude/skills/fb-ad-intelligence-mcp.md
   ↑ 这是你的完整 SOP — 找到「阶段 {N}」段并照做所有步骤
2. {上阶段产物文件路径} （如果是阶段 1 则跳过）

## Inputs
- industry: {industry}
- industry_slug: {slug — 已转好的可做文件夹名}
- region: {region, default MY}
- seed_competitors: {seed if any}
- industry_context: {ctx if any}
- workspace: competitor_analysis/projects/[project]/discovery/{slug}/
- retry_round: {1, 2, 3 — 仅阶段 2.5 重跑时填}

## Tools available
- Meta Ads 的 `ads_library_search`（全名因机器而异，在可用工具里找带这个字串的那个）
- mcp__firecrawl__firecrawl_search
- Read / Write / Edit / Bash

## Your task
按 skill 文件「阶段 {N}」整段照做，写产物到 workspace 指定文件。

## Final output (MUST DO)
**回复的最后一行必须是严格 JSON**（主 Claude 用它决策下一阶段）：

```json
{stage-specific JSON schema — 见下面每阶段 schema}
```

如遇 error: 返回 `{"stage": "{N}", "status": "error", "error_detail": "具体错误"}`

## Constraints
- 自主完成所有决策。不要向主 Claude 提问。
- API timeout 重试 1 次仍败 → log 该 query 跳过继续，不要整个阶段崩
- 跑完即返回最后 JSON 总结，不要等确认
- 保持 markdown 产物文件 + JSON summary 两个独立输出
```

### 每阶段 JSON Summary Schema（sub-agent 返回的最后一行）

| 阶段 | JSON Schema |
|------|------------|
| 1 | `{"stage":"1","status":"complete","keywords_count":N,"category_breakdown":{"A":N,"B":N,"C":N,"D":N},"file":"keywords.md","next":"stage_2"}` |
| 2 | `{"stage":"2","status":"complete","competitors_count":N,"coverage_estimate":"87%","audit_new_pct_max":"12%","needs_2_5":true,"file":"competitors_raw.md","next":"stage_2_5"}` |
| 2.5 | `{"stage":"2.5","status":"complete","hooks_searched":N,"new_pages":N,"snowball_rounds":N,"retry_round":1,"file":"competitors_hook.md","next":"stage_3"}` |
| 3 | `{"stage":"3","status":"complete","google_queries":N,"new_pages_google":N,"total_competitors":N,"file":"competitors_full.md","next":"stage_4"}` |
| 4 | `{"stage":"4","status":"complete","depth_top_n":12,"breadth_count":N,"five_lens_done":true,"devils_advocate_count":N,"winning_hooks":N,"framing_templates":8,"file":"report.md","next":"stage_5"}` |
| 5 | `{"stage":"5","status":"complete","html_path":"competitor_analysis/projects/[project]/discovery/{slug}/竞争情报报告.html","sections":9,"next":"done"}` |

### 主 Claude 决策逻辑

| 收到 sub-agent 返回 | 做什么 |
|--------------------|--------|
| stage 1 / 3 / 5 status=complete | 立刻调下一 sub-agent |
| stage 2 status=complete & `needs_2_5=true` | 调 sub-agent 2.5（retry_round=1） |
| stage 2 status=complete & `needs_2_5=false` | 直接跳到 sub-agent 3 |
| stage 2.5 status=complete & 仍有 audit_new_pct>10% & retry_round<3 | 再调 sub-agent 2.5（retry_round+1） |
| stage 2.5 retry_round=3 | 不再重跑，进 sub-agent 3 |
| stage 4 status=complete | 调 sub-agent 5 |
| stage 5 status=complete | 报告用户最终 HTML 位置 + 各阶段 metric 一行总结 |
| 任何 status=error | 停下，把 error_detail 报告用户 |

---

## 阶段 1：关键字生成

### 准备工作
```bash
mkdir -p competitor_analysis/projects/[project]/discovery/{行业名}
```

### 关键字策略（v2 — narrow 优先 + 长尾覆盖）

**A 类：核心宽词（用于撞主要玩家，知道 tail 必漏）**
- 例：「AI 课程」「AI 培训」「AI training」
- 目标 8-10 个
- **预期 estimated_total_count 大（>100），只能拿前 50 ranked recency**

**B 类：narrow 服务 / 痛点 / 结果词（优先拿 tail）**
- 例：「AI 副业」「AI 写文案」「AI 自动化课程」
- 目标 10-15 个
- **预期 estimated_total_count 中等（50-200），第一遍跑前 50，后续阶段 2.5 用滚雪球补 tail**

**C 类：本地 Rojak 词（narrow，能拿完整）**
- 例：「Belajar AI Malaysia」「AI training KL」「ChatGPT 中文教学」
- 目标 5-8 个
- **预期 estimated_total_count 小（<50），通常拿完整集**

**D 类：工具名 + 课程组合（narrow）⭐ 高 ROI**
- 例：「Midjourney 课程」「Cursor 教学」「n8n 课程」
- 目标 10-30 个（按行业相关性选）
- **预期 estimated_total_count 小，能拿完整集**

### 输出
将以下内容写入 `competitor_analysis/projects/[project]/discovery/{行业名}/keywords.md`

```markdown
# 关键字清单
行业：{行业}
区域：{region}
生成日期：{日期}

## A 类（宽词，预期 >100 命中，拿前 50 recency）
1. AI 课程
2. AI 培训
...

## B 类（narrow 痛点/结果词，预期 50-200 命中）
1. AI 副业
2. AI 写文案
...

## C 类（本地 Rojak narrow 词，预期 <50 通常完整）
1. Belajar AI Malaysia
2. AI training KL
...

## D 类（工具名 + 课程 narrow 组合）
1. Midjourney 课程
2. Cursor 教学
...

## 已知种子竞争对手
1. {如有}

## 建议搜索顺序（v2 — narrow 优先）
1. **先 C + D 类**（small total，能拿完整集，覆盖 tail）
2. **再 B 类**（mid total，拿前 50 + 标注漏抓风险）
3. **最后 A 类**（large total，拿最新 50，仅做主玩家识别）
4. 阶段 2.5 用 hook 反查补 A/B 类的 tail
```

---

## 阶段 2：Ad Library 搜索 + Coverage Audit

### 第一步：种子对手深挖（如有）
对每个种子对手用 `page_ids=` 反查（不是 search_terms），拿全部 active 广告。

### 第二步：关键字逐个搜索（按 keywords.md 顺序：C/D → B → A）

对每个关键字：
```
1. 调用 ads_library_search(search_terms="{关键字}", countries=["MY"], ad_active_status="ACTIVE", limit=50)
2. 记录 estimated_total_count 数字
3. 解析返回结果，记录每个 page_name + page_id + 广告数量
4. 立刻 append 写入 competitors_raw.md
5. ⚠️ v2 关键：在 competitors_raw.md 该关键字行标注：
   - "total=N, 拿到 50/N" 如 N>50 → 漏抓 (N-50) 条
   - "total=N, 拿到 N/N (完整)" 如 N≤50
```

### 第三步：滚雪球 — 每完成 5 个关键字检查一次
看新发现 page 的广告 `ad_creative_link_title` / `ad_creative_body` 有没有 keywords.md 没的高频短语 → 加进「补充关键字队列」当下一批跑。

### 第四步：⚠️ Coverage Audit（v2 新增，必跑）

跑完 keywords.md 所有关键字后，**立刻**做 3 个独立 audit query：

```
audit_query 1: 随机挑 1 个新词（如「{行业} workshop」「{行业}训练营」）
audit_query 2: 用最大 S 级对手的某个 hook 当 query（如「免费 VIP 培训」）
audit_query 3: 行业 + 城市组合（如「{行业} KL」「{行业} Penang」）

每个 audit 跑：ads_library_search(search_terms=..., countries=["MY"], ad_active_status="ACTIVE", limit=50)
```

对每个 audit query 的返回结果：
- 计算「新发现 page 占比」= 不在 competitors_raw.md 现有名单的 page 数 ÷ 50
- 如果 ≥ 10% new → coverage 还漏，**回到第二步用 audit query 当新关键字继续滚雪球**
- 如果 < 10% new → coverage 已饱和

### 结束条件
- 所有 keywords.md 关键字跑完
- 3 个 audit query 都 < 10% new
- 对手总数预期 50-150（按行业大小定）

### 输出 `competitors_raw.md` 格式

```markdown
# Ad Library 搜索结果
搜索日期：{日期}
行业：{行业}

## 竞争对手总表（按 page_id dedupe）
| Page 名称 | Page ID | 货币 | 发现关键字（命中次数） | 广告数量 | 备注 |
|----------|---------|------|--------------------|---------|-----|

## 关键字搜索进度
| 类别 | 关键字 | total | 拿到/total | 状态 | 新发现 page 数 |
|------|------|------|----------|-----|-------------|
| C | Belajar AI Malaysia | 140 | 50/140 | ⚠️漏抓 90 条 | 5 |
| D | n8n 课程 | 47 | 47/47 | ✅完整 | 4 |
| A | AI 课程 | 870 | 50/870 | ⚠️漏抓 820 条 | 15 |
...

## Coverage Audit 结果（v2 必填）
| Audit Query | total | 返回 50 中新发现 page 数 | % new | 结论 |
|------------|------|------------------------|------|------|
| {行业} workshop | 65 | 3 | 6% | ✅饱和 |
| 免费 VIP 培训 | 230 | 12 | 24% | ⚠️漏，回跑 |
| {行业} KL | 32 | 1 | 2% | ✅饱和（且完整） |

**Coverage 估算：** 基于 audit query 平均 new % = N%，覆盖率估算 ~{100-N*1.5}% local MY 主要玩家

## 过程中发现的新关键字（自动补充）
1. {从广告文案里抽出的高频短语}
```

---

## 阶段 2.5：Hook 反查 + 滚雪球（v2 新增，强制执行）

### 任务背景
阶段 2 即便做了 Coverage Audit，仍有「广告标题只写 hook 不写课程标签」的对手会漏（如 [example competitor] 的「用 1 个小时了解 AI 如何帮助你」「免费报名」）。
本阶段用对手原文 hook 当 search_term 反查。
**为什么有效？** 完整 hook 短句通常 estimated_total_count < 50，能拿完整集，包括 tail。

### 第一步：从 competitors_raw.md Top 15 对手抽 hook
对 Top 15（按广告数）每个 page 用 `page_ids=` 反查：
```
ads_library_search(page_ids=["{page_id}"], countries=["MY"], ad_active_status="ACTIVE", limit=50)
```
提取该 page 的 `ad_creative_link_title` 原文，记录所有 unique hook 短句（5-15 字段）。

### 第二步：Hook 反查
对提取的每个 unique hook：
```
ads_library_search(search_terms="{hook 短句}", countries=["MY"], ad_active_status="ACTIVE", limit=50)
```
看 estimated_total_count：
- < 50 → 拿完整集，记录所有不在 raw 名单的新 page
- ≥ 50 → 只拿前 50 (recency)，记录新 page 但标注「可能还漏 tail」

### 第三步：新发现 page 反查
对所有新发现 page 用 `page_ids=` 拉它全部 active 广告，append 到 `competitors_hook.md`。

### 第四步：滚雪球
新 page 的 hook 提取出来 → 当下一批 search_terms 继续跑。
**结束条件：** 连续 2 轮 hook 反查都没新对手。

### 输出 `competitors_hook.md`
```markdown
# Hook 反查 + 滚雪球补漏结果
更新日期：{日期}

## 反查使用的 Hook 清单（从阶段 2 Top 15 对手提取）
| 来源 Page | Hook 原文 | total 命中 | 新发现 page 数 |
|----------|----------|----------|--------------|
| AI 超级营销 | 点击报名免费课程 | 35 | 0 |
| AI Elite Mastery | 首 100 位免费报名 | 28 | 2 |
| [example competitor] (新) | 用 1 个小时了解 AI 如何帮助你 | 8 | 3 |
...

## 新发现对手（合并到 competitors_full 阶段 3）
| Page 名称 | Page ID | 来自 Hook | 广告数 |
|----------|---------|---------|------|

## 滚雪球轮次记录
轮 1: N 个新 page
轮 2: M 个新 page
轮 3: 0 个新 → 结束
```

---

## 阶段 3：Google 补漏

### 前提
读取 `competitors_raw.md` + `competitors_hook.md`。

### 任务说明
阶段 2 + 2.5 主要靠 Ad Library API 自身。本阶段用 Google 搜补「FB 广告投放少但有 page」的对手（如 SEO 流派 trainer / B2B HRDF 老牌机构）。

### Google 搜索（用 `industry` 替换 `{行业}`）
对每个 query 调用：
```
mcp__firecrawl__firecrawl_search(query="{query}", limit=10)
```

**Query 模板（v2 — 7 个 query）：**
1. `{行业} Malaysia Facebook`
2. `{行业} KL site:facebook.com`
3. `top {行业} provider Malaysia 2026 list`
4. `{行业} Kuala Lumpur HRDF claimable`（B2B 走 SEO 的对手）
5. `best {行业} Malaysia review` 
6. `马来西亚 {行业} 推荐 facebook`
7. `Kursus {行业} Malaysia` (Malay 市场)

### 反查验证
对 Google 新发现的每个 page name：
```
ads_library_search(search_terms="{page name}", countries=["MY"], ad_active_status="ACTIVE", limit=10)
```
- 有广告 → 加进 `competitors_full.md`，标 "Google 补漏 + 有跑广告"
- 没广告但 page 存在 → 仍加进，标 "Google 补漏 + 无 FB 广告（SEO 流派）"

### 输出 `competitors_full.md`
```markdown
# 竞争对手完整名单
更新日期：{日期}
来源汇总：Ad Library 关键字搜 N1 个 + Hook 反查 N2 个 + Google 补漏 N3 个 = 总 N

## 优先级定义
- S 级 = 广告 ≥ 15 条 / 行业大玩家
- A 级 = 广告 5-14 条 / 中型对手
- B 级 = 广告 1-4 条 / 小型 / 单点
- C 级 = Google 补漏（FB 广告 0 但 page 存在）

## 完整对手表（按级别分组）
（每个含 Page 名 / Page ID / 货币 / 来源 / 广告数 / 主打方向）

## Coverage 估算（v2 必填）
基于阶段 2 Coverage Audit + 阶段 2.5 滚雪球收敛：
- 估算覆盖率：~XX% local MY 主要玩家
- 已知盲区：A 类宽词漏的 N1 条 tail / 阶段 2.5 audit 仍 >10% 的 query 漏的 N2 条
- 数据来源：Meta Ad Library 官方 API
- 数据局限：API max 50 / no pagination / recency sort，无法保证 100% 覆盖
```

---

## 阶段 4：Breadth Pass + Depth Pass 双层报告

### v2 核心变化：分两层报告（[owner] 决策）

| Pass | 对手数 | 分析深度 | 用途 |
|------|------|---------|------|
| **Breadth Pass** | 全部 N（通常 80-150）| 浅 — 仅 name / id / 广告数 / 主打方向 1 句话 | 完整视野，给团队当 reference 名单 |
| **Depth Pass** | Top 10-15 only | 5 lens 深挖 + Devil's Advocate + Winning Hook | 给 marketer 实战参考 |

### Depth Pass — Top 10-15 selection 明确标准（v2 关键）

必须按以下规则筛选（**禁止仅按 raw 广告数排**）：
- ✅ Local MY page（page 货币 MYR / page 名地址 MY 信号 / Malay 或 MY 中文内容）
- ✅ Active ad count ≥ 5
- ✅ 直接做培训 / 课程（不是工具品牌 / 国际平台 / 学位文凭项目）
- ❌ 排除：国际广告主（如 Tyler Tometich 国际市场）/ 学位项目（如本科文凭课）/ 工具官方广告

### 任务 A：Breadth Pass — 浅档案

对 `competitors_full.md` 所有对手：
- 已经在 full.md 里的 1 句话主打方向 = 浅档案
- 不需要额外深挖，直接整合到报告里

### 任务 B：Depth Pass — 5 Lens 深档案

对每个 Top 10-15 对手用 `page_ids=` 拉完整 active 广告：
```
ads_library_search(page_ids=["{id}"], countries=["MY"], ad_active_status="ACTIVE", limit=50)
```

**每个对手必写满 5 Lens（禁止只列「主打卖点 / 常用词」表面信息）：**

**Lens 1 — Funnel 复用度 vs 产品多元化**
计算：active 广告数 ÷ unique hook 数
- 比值 >10（如 30 条 / 3 个 hook）→ 「funnel 已稳定，在 A/B 测受众 / 素材」
- 比值 <3（如 15 条 / 7 个 hook）→ 「产品多元化矩阵」
明确判断属于哪种，并解释商业含义。

**Lens 2 — 投放规模 vs 商业模式**
高广告量 ≠ 卖得好。判断是哪类：
- (a) ad account 容量大烧钱测素材
- (b) Lead Form 收名单后端跑 high-ticket
- (c) 主业是企业咨询 / 工作坊，FB 只是 lead 入口
Explicit 选 a/b/c。

**Lens 3 — Lead Form vs 真课卖 vs 名单倒卖**
判断标准：CTA / 紧迫感（「免费 VIP」「首 100 位」反复用 = 漏斗收名单嫌疑）/ 是否有真实课名 / 价格 / 讲师 LinkedIn。
Explicit 标注「疑似名单收割」/「真课程销售」/「咨询导流」。

**Lens 4 — 双品牌轮投 / Page 矩阵**
检查同一 hook 是否在两个 page 同步跑（如 AI Elite Mastery + Fregolytics）→ 标注「防 page 被 ban + 翻倍 ad account 容量」。

**Lens 5 — Framing 流派定位**
归入 framing 流派（副业变现 FOMO / 职业转型 / 企业 HRDF / 卖课赚钱 / AI 管系统 / 大学文凭 / 工具单点 / 行业垂直 / 信任牌等），判断该流派的地位（领头 / 跟随 / 错位）。

**每个深档案的 markdown 必须含 3 个 block：**
- ### 策略点拆（5 Lens）
- ### 防御弱点
- ### 学得起 / 学不起的原因（让用户判断要不要抄）

### 任务 C：Devil's Advocate 章节（强制最后写）

prompt 进 AI：
> 「现在切换角度，假装你是这个市场已经做了 5 年的老 marketer。Brutally 列出 3-5 条『数据可能在骗读者』的洞察。
> - 每条三段式：『新手会怎么误判 → 真相是什么 → 因此读者该怎么调整策略』
> - 举例参考：『X 有 213 条广告 ≠ 卖得好，可能只是 ad account 容量大烧钱测素材』『Y 投 190 条很可能在拉名单不是卖课』『Z 看似强但靠的是学院信用背书，个人讲师打不过这块』」

### 任务 D：Winning Hook 投放规模榜（v2 新增）

**提取规则：**
1. 遍历每个 Top 10-15 对手的 active 广告 ad_creative_link_title + ad_creative_body
2. 找「同一对手反复使用 ≥3 次的句段」或「跨 ≥2 个对手都用的句段」
3. 输出三元组：(hook 原文 | 来源 page | 估算投放规模)

**强制 markdown 输出格式：**
| Hook 原文 | 来源 Page | 投放规模 | 类型 | 学得起 / 学不起 |
|----------|----------|---------|------|---------------|
| "AI Digital Marketing Masterclass - HRDF Claimable" | 没废话 Mark Goh | 50+ 条 | 单一品牌矩阵 | 学不起 — 靠 Mark Goh 个人 IP 信任 |
| "首 100 位免费报名" | AI Elite Mastery + Fregolytics | 33 条（双 page 轮投） | 双品牌 FOMO 漏斗 | 学得起 — 任何讲师可套 |
| "From AI Pilot to Production in 2 Days" | 360Digitmg | 3 条 | 反课程 framing | 学得起 — 角度任何人可套 |

### 任务 E：通用化机会点章节（v2 — 删除单一身份预设）

⚠️ **绝对禁止**：提任何具体客户名 / 个人 IP 名 / 行业品牌名。

#### E.1 — 2x2 市场空白矩阵（必出图表）

输出 markdown 表格：
- X 轴：客单价（低 RM<500 / 高 RM>2000）
- Y 轴：受众类型（B2C 个人学员 / B2B 企业老板）

每个象限列出：
- 现有玩家 N 个
- 拥挤度评分（1-5）
- 空白程度评分（1-5）
- 该象限关键差异化角度

#### E.2 — 8 种通用差异化 framing 模板

固定输出 8 个模板，每个含：
1. Framing 名称
2. 适用对象（仍占位通用，如 [产品类] / [受众类]）
3. 当前市场谁占了 / 谁还没占
4. 模板文案 hook 句式（占位 [产品] / [受众] / [结果数字]，让用户自己填）
5. 适用场景

**8 个固定模板：**

```
① 反课程叙事（「N 周理论 vs N 天实战」类）
② 时间承诺 + 结果承诺（「N 小时学会做出 X」类）
③ 反 FOMO 信任牌（「不留电话直接 WA / N 天退款 / 真讲师 LinkedIn」类）
④ 反向受众 framing（如别人卖给老板，你卖给员工说服老板）
⑤ HRDF / 政府补贴角度（B2B 切入）
⑥ 细分行业垂直（行业 + 工具组合）
⑦ 真实案例账本（脱敏客户数据做信任武器）
⑧ 价格透明对照（公开课程价 vs 对手私聊议价不透明）
```

每个模板格式：
```markdown
### 模板 X — [framing 名]
**适用对象：** [占位通用受众]
**当前市场：** 谁占了 / 谁还没占
**hook 模板：** "[占位文案，含 [产品]/[受众]/[结果] 占位符]"
**适用场景：** [何时用此 framing]
```

#### E.3 — 通用化原则（写进 prompt 给 AI）
> "禁止：提任何具体客户名 / 个人 IP 名 / 行业品牌名。
> 禁止：默认读者是某个特定身份。
> 必须：所有机会点写成「适用人群 + 切入条件 + 文案 hook 模板」三段式。
> 如果用户填了 `industry_context` 参数，可在每个模板下加一句「适用度评分 1-5（对此 context）」，但不可提具体名字。"

### 输出 `report.md` 格式（v2 整体结构）

```markdown
# {行业} — FB 广告竞争情报报告 v2
分析日期：{日期}
覆盖竞争对手：{N} 个（Breadth Pass）
深挖对手：Top {10-15} 个（Depth Pass）
Coverage 估算：~XX% local MY
数据来源：Meta Ad Library 官方 API + Hook 反查 + Google 补漏

---

## 〇、市场快读（5-8 行总览）
（独立小段，说明市场分裂成 N 大板块，整体特征）

## 一、Breadth Pass — 全名单（{N} 个）
（按 S/A/B/C 级分组的完整表格 + 1 句话主打方向）

## 二、Depth Pass — Top {N} 排名（明确 selection 标准说明）
（表格：Page / 级别 / Active 广告数 / 主推产品 / 角度）

## 三、Depth Pass — Top 5 S 级深档（5 Lens）
（每对手：策略点拆 / 防御弱点 / 学得起 学不起）

## 四、Depth Pass — A 级快档（5 个）
（每对手 3-5 hook + 1 段策略解读）

## 五、Devil's Advocate（强制章节）
（3-5 条「数据可能在骗读者」反向洞察）

## 六、Winning Hook 投放规模榜
（hook 原文 + 来源 + 规模 + 学得起原因）

## 七、市场卖点地图（6 大 framing 流派）
（表格：流派 / 代表玩家 / 核心钩 / 客单价）

## 八、2x2 市场空白矩阵 + 8 种通用 framing 模板
（矩阵图 + 8 模板 — 通用占位符格式，禁止预设身份）

## 附录 — Coverage Audit + 数据局限说明
（明确告知 Coverage 估算 XX% + API 硬限制）
```

---

## 阶段 5：HTML 报告输出（v2 暗色主题升级）

### 前提
先读取 5 个数据文件：
```bash
cat competitor_analysis/projects/[project]/discovery/{行业名}/keywords.md
cat competitor_analysis/projects/[project]/discovery/{行业名}/competitors_raw.md
cat competitor_analysis/projects/[project]/discovery/{行业名}/competitors_hook.md
cat competitor_analysis/projects/[project]/discovery/{行业名}/competitors_full.md
cat competitor_analysis/projects/[project]/discovery/{行业名}/report.md
```

### 输出原则（v2 严格遵守）

1. **不暴露工作流程**：不出现「阶段 1/2/2.5/3/4」「分 N 个阶段」等字眼
2. **不预设身份**：不提任何具体客户名 / 个人 IP 名 / 行业品牌名（除非用户填了 `industry_context`）
3. **不重叠**：同一数据只出现一次
4. **诚实声明 Coverage**：明确写「估算 ~XX% 覆盖」，禁止吹「100% 全覆盖」

### HTML 章节结构（v2 — 暗色主题）

| 章节 | 标题 | 数据来源 | 设计要点 |
|------|------|---------|---------|
| 0 | 顶部统计 + 「市场快读」 | report.md 〇 | .note 蓝灰底框，5-8 行总览 |
| 1 | 一、Top 10-15 排名 | report.md 二 | 表格 + 级别 badge |
| 2 | 二、S 级深档（5 Lens） | report.md 三 | 每对手一张 .card：策略点拆 / 防御弱点 / 学得起原因，**含 quote-box 原文 hook** |
| 3 | 三、A 级快档 | report.md 四 | 每对手简档：3-5 hook + 一段策略解读 |
| 4 | 四、B 级折叠区 | competitors_full.md | `<details>` 折叠，每对手 2-3 句 |
| 5 | 五、市场 framing 流派 | report.md 七 | 表格：流派 / 代表玩家 / 核心钩 / 客单价 |
| 6 | 六、Winning Hook 投放规模榜 | report.md 六 | .kw-grid 卡片：hook 原文 + 来源 + 规模 + 学得起原因 |
| 7 | 七、2x2 市场空白矩阵 + 8 framing 模板 | report.md 八 | 矩阵表 + 8 张 .opp 绿色卡片（通用占位符） |
| 8 | 八、Devil's Advocate | report.md 五 | .note warn 框，3-5 条反向洞察 |
| 9 | 附录 — Coverage + 数据局限 | competitors_full.md Coverage 段 | 页脚明确写 Coverage % |

### HTML 设计规范（v2 — 暗色主题 CSS）

参照参考报告 CSS：

```css
:root {
  --bg: #0f1217;          /* 主背景 */
  --card: #171b22;        /* 卡片背景 */
  --ink: #e8ecf2;         /* 主文字 */
  --muted: #8a93a3;       /* 次要文字 */
  --accent: #ffb547;      /* 强调黄 */
  --s: #ef4444;           /* S 级红 */
  --a: #f97316;           /* A 级橙 */
  --b: #3b82f6;           /* B 级蓝 */
  --c: #64748b;           /* C 级灰 */
  --line: #262c36;        /* 分隔线 */
  --green: #22c55e;       /* 绿（机会点） */
}
```

**字体：** `'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif`（不引入 Google Fonts）

**核心 CSS 类：**
- `.stat` — 顶部统计数字（`.num` + `.lbl`）
- `.note` — 蓝灰提示框（市场快读用）
- `.card` — 对手深档卡片（`.name` + `.meta` + 内嵌 hooks/strategy/weakness）
- `.hooks` — 原文 hook 列表（带 `.hook-tag` 标签）
- `.win` — 绿色「最强 / 学得起」
- `.warn` — 黄色「防御弱点」
- `.kw-grid` — Winning Hook 榜 grid（auto-fit minmax(220px,1fr)）
- `.kw-cell` — Hook 卡片（`.ct` 右浮黄色数字 = 投放规模）
- `.opp` — 机会点绿色卡片（gradient 背景 + 绿色左边框）
- `.opp-title` + `.opp-body`
- `.b-s` / `.b-a` / `.b-b` / `.b-c` — 级别 badge（rgba 半透）
- `<details>` + `<summary>` — B 级折叠区

**评级 Badge 配色：**
```css
.b-s { background: rgba(239,68,68,.15); color: #fda4a4; border: 1px solid rgba(239,68,68,.3); }
.b-a { background: rgba(249,115,22,.15); color: #fdba74; border: 1px solid rgba(249,115,22,.3); }
.b-b { background: rgba(59,130,246,.15); color: #93c5fd; border: 1px solid rgba(59,130,246,.3); }
.b-c { background: rgba(100,116,139,.15); color: #cbd5e1; border: 1px solid rgba(100,116,139,.3); }
```

### 强制必含 / 强制禁止

**必含：**
- 「市场快读」note 在 hero 下方
- 每个 S 级档案有「防御弱点」.warn 块 + 「学得起 / 学不起」.win 块
- Winning Hook 榜每条带具体投放规模数字 + 「学得起原因」一句
- Devil's Advocate 单独一节（warning 风格）
- 页脚明确写 Coverage 估算 % + API 硬限制说明

**禁止：**
- 章节 7（机会点）禁止提任何具体客户 / 个人 IP / 行业品牌名
- 章节 2/3「策略点拆」必须覆盖 5 Lens（少 Lens 不合格）
- 章节 8 Devil's Advocate 不可省略（少这章不算合格）
- 禁止「100% 覆盖」「全部不遗漏」等吹嘘话术

### 输出文件
路径：`competitor_analysis/projects/[project]/discovery/{行业名}/竞争情报报告.html`

完成后告知用户 HTML 路径。

---

## ⚠️ 数据局限说明（必须告诉用户）

MCP `ads_library_search` 走 Meta Graph API `ads_archive` endpoint。

**硬限制：**
- max 50 / no offset / no date filter / recency sort
- 100% 完整覆盖**技术上不可能**，不要承诺

**v2 已尽量缓解：**
- 阶段 2 narrow 优先策略：C/D 类小词通常 total<50 拿完整
- 阶段 2.5 Hook 反查：用 5-15 字短句反查通常 total<50 拿完整
- 阶段 2 Coverage Audit：跑完后用 3 个独立 query 测漏抓 %
- 阶段 3 Google 补漏：抓 SEO 流派 / B2B HRDF 不投 FB 的对手

**实测估算覆盖率：**
- 主要玩家（S+A 级）：~95%
- 中型对手（B 级）：~85%
- 长尾（C 级）：~60-70%

**报告末尾标注：**
> 数据来源：Meta Ad Library 官方 API + Hook 反查 + Google 补漏 + Coverage Audit。MY 商业广告主要玩家覆盖率约 95%，长尾覆盖约 60-70%。完整覆盖在 MCP API 限制下技术上不可能，如需 100% 覆盖请回退 `/fb-ad-intelligence`（Chrome 手动版）。

---

## 常见问题处理

| 问题 | 解决方法 |
|------|---------|
| MCP `ads_library_search` 报错 / timeout | 重试 1 次，仍败 → 跳过该关键字记录 log，继续跑下一个 |
| `estimated_total_count > 50` 拿不全 | v2 用阶段 2.5 Hook 反查补 tail；不要直接放弃 |
| `ad_creative_link_title` 是空 | 用 `ad_id` 当 fallback label，也看 `ad_creative_body` |
| 同一 page 出现在多个关键字 | 按 `page_id` dedupe，记录每个 page 命中的关键字数量（覆盖广度） |
| Firecrawl Google 搜索返回 0 结果 | 简化 query 重试一次，仍 0 → 标注「该 query 无收获」 |
| Context 快满（sub-agent 自己 context 接近上限） | 立刻保存当前进度到产物文件，JSON summary 标 `status="context_overflow"` + `progress_saved_to:"path"`，主 Claude 收到后调下一 sub-agent 接着跑（不打扰用户） |
| 主 Claude 自己 context 快满 | 主 Claude 把当前各阶段 metric + 下一步告知用户，让用户开新对话继续 orchestration（用户说「继续跑」即可） |
| Coverage Audit 3 轮都 > 10% new | 用户的行业可能太宽（如「营销」），建议缩窄到子行业重跑 |
| 用户没填 `industry_context` | 默认完全通用模式，所有 framing 模板用占位符 [产品]/[受众]/[结果] |

---

## 快速触发模板

### 触发 1：默认 Orchestration 模式（v3）

**用户说：** "用 ad library MCP 跑 [汽车隔热膜] 的 FB 广告情报，我们公司是营销代理"

**主 Claude 立刻做（不要问，直接跑）：**
```
1. 解析 input：
   - industry = 汽车隔热膜
   - industry_slug = 汽车隔热膜
   - region = MY (默认)
   - seed_competitors = (无)
   - industry_context = "营销代理公司"

2. Bash: mkdir -p competitor_analysis/projects/[project]/discovery/汽车隔热膜/

3. 告诉用户 1 句话：「开跑 6 阶段 orchestration，预计 45-70 分钟，跑完通知。」

4. Agent tool 调 sub-agent 1（阶段 1 — 关键字生成）：
   - subagent_type: "general-purpose"
   - 不传 model
   - prompt: 套用「Sub-agent Prompt 通用框架」，stage_n=1，industry/slug/context 都填上

5. 等返回，解析最后一行 JSON

6. 按「主 Claude 决策逻辑」表 → 立刻调下一个 sub-agent
   - 重复直到阶段 5 完成
   - 任何阶段 status=error → 停下报告用户

7. 最后报告：「报告在 competitor_analysis/projects/[project]/discovery/汽车隔热膜/竞争情报报告.html。
   - 阶段 1: N 关键字
   - 阶段 2: M 对手 / Coverage ~85%
   - 阶段 2.5: K 个 Hook 反查新发现
   - 阶段 3: L 个 Google 补漏
   - 阶段 4: Top 12 深度档案
   - 阶段 5: HTML 输出」
```

### 触发 2：手动模式（v2 兼容，单阶段跑）

**用户说：** "/fb-ad-intelligence-mcp AI 培训 阶段 2.5" / "stage 4 only" / "我手动跑阶段 X"

**主 Claude 做：**
```
1. 解析 stage 参数（如 stage=2.5）
2. 检查前置阶段产物是否齐全：
   - 阶段 2.5 需要 competitors_raw.md
   - 阶段 4 需要 competitors_full.md
   - 缺 → 报告用户「前置文件 X 缺失，先跑前置阶段」
3. **不调 sub-agent**，主 Claude 自己按 skill 文件「阶段 X」段跑
4. 写产物 + 报告用户
```

### 触发 3：跑过一半要继续

**用户说：** "继续跑" / "fb-ad-intelligence-mcp AI 培训 继续"

**主 Claude 做：**
```
1. 检查 competitor_analysis/projects/[project]/discovery/{industry}/ 已有哪些产物文件
2. 找到最后一个完成的阶段
3. 进入 Orchestration 模式 从下一阶段开始
```
