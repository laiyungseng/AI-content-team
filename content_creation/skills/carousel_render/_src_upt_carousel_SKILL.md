---
source: UPT-course-setup-v2.skill / course-skills/carousel-html/SKILL.md.packed
original-skill: carousel-html
copied: 2026-10-31
status: staged
destination: carousel_generation.md, static_post_generation.md (plan step 8b)
---
# Carousel HTML — 中文轮播图程序化出图 skill

## 一句话：用 HTML 模板 + Chrome headless 截图，1080×1350 PNG 直接发 IG/小红书。

---

## 两条出图路径 — HTML 程序化 vs GPT-image-2 OAuth

这个 skill 有两条路径，按场景选。**默认走 HTML**。

| 维度 | HTML 路径（默认） | GPT-image-2 OAuth 路径 |
|------|-----------------|----------------------|
| 字精准度 | 100% 字形精准 | 中文 OK（2026-06-26 verified 8 张 i2i 中文 carousel 全 readable），偶有 micro drift |
| Brand 一致性 | 8 张完全一致（程序化确定性输出） | 高度一致但有 micro 差异（每张 pill / sticker 位置可能略偏） |
| 装饰元素 | CSS / inline SVG 模拟 | 真插画 / retro sticker / Bauhaus 手作感 |
| Layout 自由度 | 受 template 约束 | AI 自由发挥 |
| 速度 | 30-60s 全套 render | 8 张并发 ~5-10 min |
| 成本 | 几乎 0（本地 Chrome headless） | OAuth 配额 |
| 复用 | brand-kit JSON 定义一次，无限套用 | 单次出图 |
| 尺寸 | 精确 1080×1350 | 实际 1024×1536（最接近的 OAuth supported size，IG 仍可用） |
| 适合场景 | 信息密度高 / 文字量大 / 多客户长期复用 brand / 客户档案稳定 | retro 手作风 / 装饰元素多 / 单 post / 一次性活动 / 风格新颖 |

### 何时切 GPT-image-2 路径

> ⚠️ **这条路径需要额外条件**：ChatGPT Plus 订阅 + 装好 Codex CLI 并跑过 `codex login`。
> **没有的话就走 HTML 路径**（默认那条），它零 API key、零订阅、只要有 Chrome 就能跑，
> 而且中文字 100% 精准，是这个 skill 的主线。
>
> 使用者问起为什么用不了 GPT-image-2 → 照实说需要另外订阅，别叫他去装一堆东西。

有上述条件、且用户说以下话时 → 走 `docs/gpt-image2-path.md`：
- 「用 GPT-image-2 出 carousel」
- 「i2i 参考这张图的感觉」
- 「要 retro 手作感 / Bauhaus / 真插画 sticker」
- 「装饰元素丰富一点」
- 「HTML 太死板，想要更自由的设计」

### Hybrid 路径（HTML + GPT 装饰元素）

适合「字要精准但要真 sticker / icon illustration」的场景：
1. 用 GPT-image-2 OAuth 出 3-5 个装饰 asset（grid 纸纹 / retro sticker / icon set），保存到 `work-dir/assets/`
2. HTML template 嵌入这些 asset（base64 embed 或 file://）
3. 走标准 render.py 流程

实测 case：2026-06-26_[creator]-style ([creator] Hills IG 风格复刻) 走过 A/B/C 三路对比，B (hybrid) 跟 A 视觉差异主要在 retro sticker 的「手作感」。

---

## 触发后第一件事

**先 read 这个 skill 的同目录文件，确认 templates / brand-kits / scripts 都在：**

```
000_Agent/skills/carousel-html/
├── SKILL.md                            (本文件)
├── assets/
│   ├── brand-kits/
│   │   ├── _template.json              (新建 brand kit 模板)
│   │   ├── [creator-handle].json            ([owner] 个人 IP)
│   │   ├── claude.json / [brand].json      (已建的 brand kit 示例)
│   │   └── presets/                    (5 个 default preset)
│   │       ├── modern-minimal.json
│   │       ├── bold-marketing.json
│   │       ├── editorial.json
│   │       ├── luxury.json
│   │       └── warm-coach.json
│   ├── templates/                      (11 个 HTML layout)
│   └── scripts/render.py
├── docs/
│   ├── industry-recipes.md             (行业 → sequence)
│   └── content-ideas.md                (28 类内容)
└── examples/
```

---

## Step 0：识别用户身份 + brand kit 来源（4 级优先级）

**问 [owner]：「这次轮播图是给谁做？有没有参考图 / brand 资料？」**

按答案分 4 条路（按优先级）：

### 路 A：用户给了 sample 图（最准 — sample-driven） ⭐ 推荐
1. **Read 用户给的参考图**（用 Read tool）
2. **提取**：主色 hex / 辅色 / 字体感觉 / 整体调性（杂志 / minimal / bold / luxury 等）
3. **Propose brand kit JSON**（参考 `assets/brand-kits/_template.json` 结构）— 列出来让 [owner] 确认 / 调整
4. 确认后 → 写到 `assets/brand-kits/{slug}.json` 持久化
5. 继续 Step 1

**Sample 图能提取什么 / 不能提取什么：**
- ✅ 能提取：主色 hex（眼测）、辅色、调性（暖/冷/中性）、风格类别（minimal/bold/editorial/luxury）
- ⚠️ 难提取：精准 hex（建议 propose 时给 ±5 hue 范围让用户挑）、字体名（建议直接用 brand-kit 内建的跨平台字体链，Mac / Windows 都验证过）

### 路 B：已有 client（[client] / [client] / [client] / [client] / [client] 等）
1. 检查 `200_Reference/client-profiles/{客户名}.md` 是否存在 → 提取颜色 / Logo / 字体偏好
2. 检查 `assets/brand-kits/{slug}.json` 是否存在
3. 都有 → 直接 load
4. client profile 有但 brand-kits/ 没有 → 从 client profile derive → 写 brand kit JSON 持久化

### 路 C：[owner] 个人 IP（@[creator-handle]）
- 直接 load `assets/brand-kits/[creator-handle].json`

### 路 D：全新客户 + 没 sample → 推 preset 让用户选
**列 5 个 preset：**

| Preset | 适合 |
|--------|------|
| modern-minimal | SaaS / 科技 / 工具 / B2B 顾问 |
| bold-marketing | Agency / 教练 IP / Sales / 课程 |
| editorial | 作家 / 顾问 / 杂志风内容 |
| luxury | 高端服务 / 投资 / 房产 / 律师 |
| warm-coach | 教练 / 个人 IP / 心理 / 育儿 |

- 用户选 preset → cp `assets/brand-kits/presets/{name}.json` → `assets/brand-kits/{slug}.json`
- 改 name / slug / handle / tagline → 持久化

### 路 E（fallback）：用户直接 type hex
- 现场问 5 项：name / handle / 主色 hex / dark color hex / light color hex
- 自动 derive body + muted（参考 _template.json）
- 持久化

---

## Step 1：让 [owner] 选 carousel 类型 + sequence

**核心理念**：内容类型 ≠ 设计 layout。skill 只管 layout，内容自己写。

### 给 [owner] 看的 menu（先列 sequence，再说每页用什么 layout）

```
要做哪种 carousel？

1. 教学 How-to (7 张)        ─ 封面 → 步骤1-5 → CTA
2. Listicle 清单 (8 张)      ─ 封面 → 项目1-6 → CTA
3. 金句海报 (1-3 张)         ─ 单纯大字 / 引言
4. 错误避坑 (6 张)           ─ 封面 → 5 个错误 → CTA
5. 案例拆解 (7 张)           ─ 封面 → 起点 → 关键动作 → 结果 → CTA
6. 客户见证 (3-5 张)         ─ 封面 → 见证 1-3 → CTA
7. 数据 / 数字 (4-6 张)      ─ 封面 → 数据卡 → 结论 → CTA
8. Before/After (5 张)       ─ 封面 → before → after → 对比 → CTA
```

**如果 [owner] 说「按行业推荐」** → 读 `docs/industry-recipes.md` 按该客户行业推 top 3。

**如果 [owner] 说「自由组合」** → 列 11 个 layout 给他自选每页。

---

## Step 1.5：Layout 接口 + max_chars 表（排版预防层）

**收内容前先看这表，超出建议数 → warn 用户「这段可能太长会溢出」。**

| Layout | 主 slot | 建议 max_chars | 备注 |
|--------|---------|---------------|------|
| `01-cover` | HEADLINE | ≤14 字 | 大字 130px，超过会换 3 行难看 |
| `01-cover` | SUBTITLE | ≤40 字 | 1-2 行 sub |
| `02-big-statement` | HEADLINE | ≤16 字 | 大字 140px |
| `02-big-statement` | SUBTITLE | ≤35 字 | |
| `03-title-body` | TITLE | ≤16 字 | 80px |
| `03-title-body` | BODY | ≤80 字 | 段落，可 `<br>` 换行；可用 `<strong>` 高亮 |
| `04-numbered-step` | TITLE | ≤12 字 | 70px |
| `04-numbered-step` | STEP_N_TITLE | ≤14 字 | 32px |
| `04-numbered-step` | STEP_N_DESC | ≤25 字 | 一行 |
| `05-checklist` | TITLE | ≤14 字 | 88px |
| `05-checklist` | ITEM_N | ≤16 字 | 主文字 |
| `05-checklist` | ITEM_N_NOTE | ≤22 字 | 注解 |
| `06-stat-cards` | TITLE | ≤14 字 | 78px |
| `06-stat-cards` | STAT_N_NUM | ≤4 字符 | 110px，太长换行（"6 位数" OK，"6 figures" NO） |
| `06-stat-cards` | STAT_N_LABEL | ≤12 字 | |
| `07-quote` | QUOTE | ≤30 字 | serif 84px，可 `<br>` |
| `07-quote` | ATTRIBUTION | ≤20 字 | uppercase |
| `08-comparison` | TITLE | ≤12 字 | center 64px |
| `08-comparison` | LEFT/RIGHT_HEADER | ≤18 字 | 44px |
| `08-comparison` | LEFT/RIGHT_BODY | ≤45 字 | |
| `09-testimonial` | QUOTE | ≤60 字 | serif 44px |
| `09-testimonial` | CUSTOMER_NAME | ≤8 字 | |
| `09-testimonial` | RESULT_NUM | ≤6 字符 | 56px |
| `10-image-caption` | HEADLINE | ≤18 字 | 84px on overlay |
| `10-image-caption` | CAPTION | ≤45 字 | |
| `11-cta-closing` | HEADLINE | ≤14 字 | 110px center |
| `11-cta-closing` | CTA_TEXT | ≤10 字符 | button 文字 |

**超出 max_chars → 不是 fatal，但要 warn + 询问是否截断 / 换 layout / 拆 2 页。**

---

## Step 2：收内容

按选定 sequence + max_chars 限制，**逐页问 [owner] 该页的文案 slot**。

UGC 真实照片页（10-image-caption.html）→ 问：
- `IMAGE_PATH`: 用户提供的真实照片绝对路径（render.py 自动 base64 embed）
- `HEADLINE` / `CAPTION` / `TAG`

---

## Step 3：组装 + render

1. 创建 work dir：`downloads/carousels/{client}/{YYYY-MM-DD}_{topic-slug}/`
2. 写 `config.json` 描述 sequence + slots
3. 跑 render.py

### Render command
```bash
python3 .claude/skills/carousel-html/assets/scripts/render.py \
  --work-dir downloads/carousels/{client}/{date}_{topic}
```

---

## Step 4：验证（**两层 — 都不能跳**）

### Layer 1: 技术层 — Claude 自己 Read 每张 PNG 跑基础 checklist

```
□ 1. 中文字体正确（非豆腐块 □ / 非乱码）—— Mac 走 PingFang SC，Windows 走 Microsoft YaHei，brand-kit 已内建 fallback
□ 2. Brand 主色对（跟 brand-kit JSON hex 一致 — accent 色块、按钮、icon）
□ 3. 文字没溢出（headline 不被切、不堆叠）
□ 4. 文字没截断（卡片内文字完整可读）
□ 5. Header bar / Footer bar 在（handle + page num + slogan + SWIPE）
□ 6. UGC photo（如有）正确嵌入，没变形 / 不灰
□ 7. 尺寸 1080×1350
□ 8. 留白合理（不挤、不空洞）
```

### Layer 2: 设计层 — **必须 invoke `design-critic` agent**

技术层过了之后 **必须** 用 Task tool spawn `design-critic` 这个 custom agent 跑 senior designer audit：

```
Agent({
  subagent_type: "design-critic",
  description: "Audit carousel design",
  prompt: "Audit downloads/carousels/{client}/{date}_{topic}/\nbrand: {brand-kit-slug}\n\n对照 design-rules.md 的 12 Universal Rules 跑 8 维度审核。verdict 是 PASS 我就交付给 [owner]，NEEDS FIX 就给 specific fix 让我 apply 后 re-render。"
})
```

`design-critic` 会输出结构化 audit report，含每页 specific findings + actionable CSS fix（file:line + 改成什么 hex/px）。

### 如发现问题 → 按顺序尝试：
1. **设计 issue（design-critic flag）** → 按 agent 给的 fix specific 改 template / brand-kit → re-render → 再 invoke agent
2. **内容太长** → 截短 OR 拆 2 页 OR 换 layout
3. **layout 渲染 bug** → 改对应 template HTML CSS → re-render
4. **字体问题** → 检查 brand-kit fonts 字段（内建链已含 Mac 的 PingFang SC + Windows 的 Microsoft YaHei；出方块先确认没被自订字体覆盖掉）

**每修一次都要 re-render + 重 Read PNG + re-invoke design-critic。直到 verdict = ✅ PASS。**

### 如发现问题 → 按顺序尝试：
1. **内容太长** → 截短 OR 拆 2 页 OR 换 layout（如 02-big-statement → 03-title-body）
2. **颜色不对** → 改 brand-kit JSON hex → re-render
3. **layout 渲染 bug** → 改对应 template HTML CSS → re-render
4. **字体问题** → 检查 brand-kit fonts 字段（内建链已含 Mac 的 PingFang SC + Windows 的 Microsoft YaHei；出方块先确认没被自订字体覆盖掉）

**每修一次都要 re-render + 重 Read PNG 验证。直到所有 8 项全过。**

---

## Step 5：交付 + 持久化

1. 把所有 PNG 用 SendUserFile 发给 [owner]
2. 文件路径告诉他：`downloads/carousels/{client}/{date}_{topic}/page{N}.png`
3. 如果是新客户 / 改了 brand kit → 确认 `assets/brand-kits/{slug}.json` 已更新
4. 如果用了 sample-driven → 提一句「下次同一个 brand 直接说 slug 名即可，不用重传 sample」

---

## Brand kit JSON 结构（持久化模板）

```json
{
  "name": "Coach [owner]",
  "slug": "[creator-handle]",
  "handle": "@[creator-handle]",
  "logo_path": null,
  "colors": {
    "primary": "#00C896",
    "dark": "#0F1419",
    "light": "#F5F0E8",
    "body": "#2A2A2A",
    "muted": "#6B7280"
  },
  "fonts": {
    "sans": "'PingFang SC', 'Hiragino Sans GB', -apple-system, 'Helvetica Neue', sans-serif",
    "serif": "'Playfair Display', 'Songti SC', 'STSong', serif"
  },
  "tagline": "AI marketer · solo IP · Malaysia 教练"
}
```

---

## 关键技术决策（advisor 确认 + 实战验证）

1. **字体**：brand-kit 内建的 fallback 链已同时涵盖 macOS（PingFang SC / Songti SC）和 Windows（Microsoft YaHei / SimSun），两边都实测过。**不要** import Google Fonts Noto Sans SC（headless 易超时 + 几 MB）
2. **Render**：Chrome `--headless --screenshot --window-size=1080,1350` 直出，**不用** Playwright（依赖太重）
3. **UGC photo**：必须 base64 embed（render.py 已实现），相对路径在 headless 会断
4. **Brand kit**：JSON 持久化，定一次下次直接 load —— 这是「能复用」的核心
5. **Empty item cleanup**：render.py 用 regex 删除空 item（CSS `:has(:empty)` 不可靠，因为 .text 里有 child node）
6. **Quote mark**：用 curly quote `"` (U+201C) 不用 ASCII `"`，serif 字体下才漂亮
7. **Stat-cards border**：永远加 `border: 2px solid rgba(0,0,0,0.08)`，避免 brand light=纯白时 card 跟背景融合（[brand] brand 踩过）
8. **Sample 提取**：Read 图 → 眼测主色 → propose JSON 让用户确认（不要直接写 disk）

---

## 不要做的事

- ❌ 不要用 AI 出图代替 HTML（这是 layout/排版主导，UGC 真人照片走 `/ugc-ad-ref`，AI 创意图走 `/creative-director`）
- ❌ 不要直接发 PNG 给 [owner] 然后说「done」—— 先 Read 跑 8 项 checklist 验证
- ❌ 不要凭空想 layout，必须用 assets/templates/ 里的
- ❌ 不要塞 30 个 layout，11 个已经 cover 99% —— 想加新 layout 之前先问 [owner] 是否真的缺
- ❌ 默认 no emoji（参考 memory `feedback_no_emoji_icon_in_cta.md`），除非 [owner] 明说要
- ❌ 不要忽略 max_chars 表 — 超出就要 warn，不要假装能 fit

---

## 相关 skill

- `/ugc-ad-ref` — 用 GPT-image-2 出真人 UGC 广告图（用在 carousel 的 image-caption 页素材）
- `/creative-director` — AI 创意图（同上）
- `/create-client-profile` — 建客户档案（brand kit 可以从这里 derive）
- `/save-kb` — 把 carousel 出图教程存进知识库
