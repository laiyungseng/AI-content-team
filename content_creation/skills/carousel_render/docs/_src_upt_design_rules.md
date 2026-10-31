---
source: UPT-course-setup-v2.skill / course-skills/carousel-html/docs/design-rules.md
copied: 2026-10-31
status: staged
destination: carousel_generation.md (8b)
---
# Design Rules — Senior IG Designer Pattern Library

提炼自 7 个顶级中文/英文市场 IG carousel designer 的完整 carousel 分析（@jasonxtsai / Klick Start Media / @tenfoldmarc / @ericchi_6666 / @charliehills / 第六位华人创作者 / @divyanshisharma）。

这份文档是 **carousel-html skill 的设计宪法** —— 改 template / 加 layout / build design-critic agent 都必须遵守这里的规则。

---

## ⭐ 12 条 Universal Design Rules（每个 pro designer 都做的事）

### Rule 1: Color discipline — 暖色锁定，无冷色，无 pure black/white

- ✅ 背景：**warm cream** （`#EFE9DE` / `#F2EFE7` / `#F5EBD8` / `#EAEAD3`），永远不是 pure `#FFFFFF`
- ✅ 主文字：**warm dark** （`#1A1A1A` / `#1F1A14` / `#6B5544` / `#141414`），永远不是 pure `#000000`
- ✅ Brand accent：**terracotta / burnt-sienna 系**（`#D9663F` / `#C8542E` / `#D8541F` / `#D97A3D`）或 magenta→orange gradient
- ❌ 永不用：纯白 / 纯黑 / 冷蓝 / 冷灰 / 冷绿
- **整套调色板都在暖轴**（warm temperature lock）

### Rule 2: Corner brackets — L 形角标，1-2px 细线，asymmetric or 4 corners

- 6/7 个 designer 都用了 corner brackets（L-shaped marks 框页面）
- Stroke 0.75-2px，颜色 = brand accent or muted ink
- **常见模式**：只在 top-left + bottom-right（asymmetric pair）或 all 4 corners
- Size：80-100px L-shape
- CSS recipe：
  ```css
  .corner-tl { position:absolute; top:40px; left:40px; width:80px; height:80px;
    border-top:1.5px solid var(--brand-accent); border-left:1.5px solid var(--brand-accent); }
  .corner-br { position:absolute; bottom:40px; right:40px; width:80px; height:80px;
    border-bottom:1.5px solid var(--brand-accent); border-right:1.5px solid var(--brand-accent); }
  ```

### Rule 3: Watermark display text — 巨型 ghost serif 单词当背景层

- 4/7 designer 用：在 BG 放一个巨大的 outlined / ghost 单词（"WRONG" / "NOISE" / "UPGRADE" / "GPT"）
- 字号：**page height 的 35-50%** （400-650px）
- 颜色：**比 BG 暗一档的 solid tone**（不用 opacity hack），如 `#E6D8BD`（BG=`#F5EBD8`）
- 字体：相同 brand serif family (Black weight)
- 位置：常在 right edge 或 bottom-right，部分裁切出画面
- 让主 headline 浮在上面，BG text 不抢戏

### Rule 4: Header strict structure — left=handle, right=page counter

- **每页 header 三件套**：handle (left) + (optional eyebrow label) + page counter (right)
- Handle：sans 400 / 500，dark ink，~22-32px，可加 `@` 前缀
- Page counter：tracked all-caps，`01 / 10` 格式，font-variant: tabular-nums
- 高度 ~80-110px，top padding ~40-60px
- 部分 designer 加 corner bracket 框 page counter

### Rule 5: Footer strict structure — slogan left, SWIPE → right, hairline above

- **每页 footer 三件套**：brand slogan (left) + (optional middle dot) + `SWIPE →` (right)
- 上方有 1px hairline divider (warm muted tone)
- Slogan：sans 400，dark ink，~22-26px，**全部 page 持续不变**（brand anchor）
- `SWIPE →`：sans 600，all-caps + 箭头 glyph，最后一页换成 `END` 或 CTA pill
- 高度 ~80-100px

### Rule 6: Typography 二元对位 — Serif Heavy 当主视觉，Sans 当 body

- **headline 必须 serif Black/Heavy（weight 700-900）**，不是 sans
- **body 用 sans Regular/Medium**
- 字号关系：H1 ≈ 96-150px，sub-headline ≈ 60-90px，body ≈ 28-42px，eyebrow ≈ 18-32px
- Sans-Serif 二元对位是 carousel 设计的 **核心规则**
- 中文：Source Han Serif TC (思源宋體) Heavy / Noto Serif TC W7-W9
- Latin display：Playfair Display / DM Serif Display / 高对比 didone

### Rule 7: Eyebrow label — 全 caps tracked，brand accent，~30px

- Headline 上方加一个 **小的 eyebrow label**：`TOOL 01` / `STEP 03 · GETTING STARTED` / `REALITY CHECK`
- 字号 ~18-32px，**letter-spacing +180-280** (0.18-0.28em)，全 caps
- 颜色 = brand accent or muted ink
- 下方常有一条 30-180px 长的 accent hairline 或 underline stub

### Rule 8: Big serif numeral as anchor — 巨大数字当视觉主体

- 多个 designer 用 **巨大 serif 数字 01-09 当 visual anchor**（不是 icon）
- 字号 ~110-220px (跟 headline 同高或更大)
- Brand accent 色 或 muted dark
- Roman numeral I-V 也用（manifesto-feel）

### Rule 9: Accent discipline — brand color 一页只出现 3-4 次

- **brand accent 不是装饰，是 semantic highlighter**
- 一页只在 3-4 个固定 slot 出现：(1) heading accent word / (2) eyebrow underline / (3) divider / (4) quote mark or pill
- 永远不在 random 装饰上用
- 让 accent 稀有 → 出现时才有 punch

### Rule 10: Subtle divider hairline — 0.5-3px brand accent，80-180px 宽

- 主 H1 下方常有 30-50px gap → 一条 **short brand-accent hairline** (80-180px wide × 3-5px tall)
- 不是全宽 line，是 short stub，像 Swiss-style section delimiter
- 在 header 和 footer 之间也常有 1px full-width hairline

### Rule 11: Pill chips — fully rounded，monospace inside，tinted accent fill

- 标签 / chip / button 全部 **fully rounded pill** (radius = half-height)
- Padding 10-24px (vertical) × 24-40px (horizontal)
- Fill = **15-20% tint of brand accent** (e.g. `#F2D6C7` over `#D9663F`)
- 字体 monospace or sans 600，tracked +60-180，all caps
- 边框 OR 实色填充，**绝不带 drop shadow**

### Rule 12: No drop shadow — 用 warm cream vs white card 创造 lift

- **永远不用 drop shadow 制造深度**
- 用 warm cream BG（`#EFE9DE`）vs 纯白 card（`#FFFFFF`）—— **warm/white 对比就是 lift**
- 这是 designer 看一眼就知道是不是 pro 的关键
- box-shadow: 0 8 24 rgba(0,0,0,0.06) 最多 minimum subtle，绝不重

---

## 🎨 4 个 Designer Style Presets（提炼自 7 个 reference）

### Preset A: Editorial Cream (jasonxtsai / tenfoldmarc / divyanshisharma 风格)

**最 mature + 最 Chinese-market-appropriate**

- BG: `#F5EBD8` (warm cream)
- Primary text: `#1A1A1A` (warm near-black)
- Accent: `#D8541F` (burnt-orange vermilion)
- Watermark: `#E6D8BD` (BG -12%)
- 字体：Source Han Serif Heavy (中文) + Playfair Display (Latin)
- Signature elements: corner bracket TL+BR / ghost watermark / Brand 圆 quote mark / hairline divider 80px terracotta
- 适合：教练 IP / 知识内容 / 思考类 / 高端培训

### Preset B: Dark Glow Gradient (Klick Start Media 风格)

**警示力 + 高对比，适合 marketing / agency / 销售内容**

- BG: `#0A0808` (warm-black)
- Primary text: `#F5F2EE` (warm off-white)
- Body grey: `#9A9590`
- Accent gradient: `linear-gradient(45deg, #FF2D7A 0%, #FF5E4D 50%, #FF9A2E 100%)`
- Corner blooms: magenta TL + orange BR radial at 30%/25% opacity
- 字体：PingFang SC Heavy (中文) + Söhne / Inter Display Bold (Latin)
- Signature elements: gradient stroke cards / inner glow / lightning ⚡ VS divider / gradient 当 semantic highlighter
- 适合：广告 agency / 行业警讯 / 高对比销售内容

### Preset C: Kinfolk Magazine (ericchi 风格)

**Photo + serif + 杂志感，适合 luxury / 个人 IP**

- BG: `#EEE7D8` (cream) / `#1B2419` (forest dark)，dual-mode
- Primary text: `#1F2A22` / `#F4ECD8`
- Accent: `#B89A5E` (matte champagne gold)
- 字体：Source Han Serif Heavy 中文 + Bodoni / Playfair Display Latin
- Signature elements: 真实摄影 BG / vertical caps track right edge / asymmetric L-bracket TL+BR / doubled ghost-serif watermark
- 适合：高端服务 / 个人 IP / luxury / lifestyle

### Preset D: Substack Notebook (charliehills 风格)

**Grid-paper + pixel mascot + pastel pills，适合 tech / SaaS / 工程师 IP**

- BG: `#F3EAD3` (warm parchment) + 6-8% opacity grid lines
- Primary text: `#0E1B33` (deep warm navy)
- Accent: `#E2785A` (coral terracotta)
- Step chip palette: 旋转 6 色 (lavender / lemon / mauve / mint / peach / sage)
- 字体：Sharp Grotesk Bold / Söhne Breit (Latin) + JetBrains Mono (code)
- Signature elements: grid paper BG / pixel mascot / cream-haloed pill chip / "PASTE THIS" disclosure pattern / mock-UI as illustration
- 适合：tech / SaaS / 程序员 IP / Notion-style 内容

---

## 🔍 Design-Critic Audit Checklist（22 项）

design-critic agent 用这份 checklist 审核每张 PNG。每项必须过关才能 ship。

### Color (5 项)
1. [ ] BG 是 warm cream / off-white，不是 `#FFFFFF`
2. [ ] 主文字是 warm dark，不是 `#000000`
3. [ ] Brand accent 一页只出现 3-4 次（accent discipline）
4. [ ] 没有冷色（蓝 / 紫 / 冷绿 / 冷灰）
5. [ ] 配色全部在 warm temperature axis

### Typography (5 项)
6. [ ] H1 用 serif Heavy (weight 700+)，不是 sans
7. [ ] Body 用 sans Regular/Medium
8. [ ] 字号 hierarchy ≥ 4 层（hero / heading / body / small）
9. [ ] Eyebrow label 有 letter-spacing +180+
10. [ ] 中文 + Latin 之间有 half-width space

### Layout (4 项)
11. [ ] Header 有 handle (left) + page counter (right)
12. [ ] Footer 有 brand slogan (left) + SWIPE → (right) + hairline above
13. [ ] Header 跟 footer 是 brand-持续 anchor（每页相同）
14. [ ] 内容区有 ≥ 64px breathing space 在 header/footer 之间

### Decorative Detail (4 项)
15. [ ] 至少 1 个 corner bracket OR 1 个 ghost watermark text OR 1 个 hairline divider
16. [ ] H1 下方有 short brand-accent hairline (80-180px)
17. [ ] 没有 drop shadow（除非 subtle 0 8 24 rgba(0,0,0,0.06)）
18. [ ] Pill chips 是 fully rounded (radius = half-height)，不是 8px radius

### Quality (4 项)
19. [ ] 文字没溢出 / 截断
20. [ ] 中文字符没豆腐块 □
21. [ ] 尺寸 1080×1350
22. [ ] 每页有一个明显的 visual focal point（不是 flat 平均分布）

---

## 🚫 8 个 Newbie Design Mistakes（design-critic 必须 flag 出来）

1. ❌ **用 pure white BG** → 改 warm cream `#F5EBD8`
2. ❌ **用 pure black 文字** → 改 warm dark `#1A1A1A`
3. ❌ **每页都用 brand color 当装饰** → 改 accent discipline，一页 3-4 次
4. ❌ **headline 用 sans 不用 serif** → 改 serif Heavy
5. ❌ **没有 eyebrow label** → 加 tracked all-caps label
6. ❌ **没有 footer slogan 当持续 anchor** → 加 brand-持续 footer
7. ❌ **用 drop shadow 制造 depth** → 改 warm cream vs white card 对比
8. ❌ **Pill chip 用 8px radius** → 改 fully rounded (radius=half-height)

---

## Per-Layout 设计升级建议（针对现有 11 个 template）

| Layout | 当前问题 | 升级方向 |
|--------|---------|---------|
| 01-cover | headline 太大占满页，无留白 | 加 corner bracket + eyebrow label + ghost watermark BG，headline 降到 110px |
| 02-big-statement | 累积 brand color 太多 | accent 只用在 1 个 highlight word + footer dot |
| 03-title-body | divider 全宽太长 | 改 short 80-140px terracotta hairline |
| 04-numbered-step | step number 用 sans 太弱 | 改 serif Heavy 巨大数字 01-05 |
| 05-checklist | checklist 太密无 lift | 加 warm/white 对比 + 行间 32px gap |
| 06-stat-cards | accent 过度 | 4 卡 only 1 卡用 dark accent 配色 |
| 07-quote | quote mark 已 fix | 加 corner bracket frame quote box |
| 08-comparison | 红/绿 cool color | 改 warm coral vs warm sage |
| 09-testimonial | card 中间空白 | 加 small caps eyebrow + result number 用 serif |
| 10-image-caption | overlay 太重 | 改 bottom-fade gradient overlay |
| 11-cta-closing | gradient angle 死板 | 改 organic angle + corner blooms |

---

## 文件状态

写于 2026-06-26，基于 7 个 IG reference designer 的 63 张图分析。

**下次更新条件**：找到新 reference style + [owner] 确认 + 跑过实战测试。
