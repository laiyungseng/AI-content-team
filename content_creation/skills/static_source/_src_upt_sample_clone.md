---
source: UPT-course-setup-v2.skill / course-skills/lovart-sample-clone/SKILL.md.packed
original-skill: lovart-sample-clone
copied: 2026-10-31
status: staged
destination: static_post_generation.md; idea only, done with nanobanana (8b)
---
# Lovart SAMPLE 复刻法

## 一句话

SAMPLE 不是「参考」，SAMPLE 就是「模板」。你的活是写**文案替换对照表**，不是写新的设计 brief。

## 为什么这样最稳（先理解再执行）

图像生成模型「画」字不是「打」字 —— 中文字对它来说是图形，笔画多、结构复杂，注意力一分散就出错字、字体不统一、排版乱。

- **自己写设计 brief** = 要模型同时做「设计排版」+「渲染中文」两件难事 → 注意力分散 → 翻车
- **复刻 SAMPLE** = 模型只需「复制现成排版 + 替换文字」→ 注意力集中在文字上 → 中文准确率大幅提升

ref 图本身就包含了完整 layout 信息。用文字去描述图里已经看得见的东西（「右侧 3 个圆形 badge」「底部 ✓ bar」「金色 serif 标题」），等于在暗示模型「你可以重新设计」，反而破坏复刻。

这不是理论 —— 2026-06-03 实战：第一轮写了 600 字 brief（还明确说了「不要复刻它的 layout，请自由设计新版面」），出图字体 4 种乱用、中文错字 2 个；改成复刻 + 替换表后重跑，同一个模型、同一张图，中文 100% 准确、layout 完整保留。

## 执行流程

### Step 1 — 收 SAMPLE + 新文案

需要两样：
- **SAMPLE 图**（本地路径）—— 用户想复刻的那张成品广告图
- **新文案** —— 表格 / 逐条 / 一段话都接，用户怎么给就怎么收，不要求格式

用户常常只给「新文案」（例如一张 Slot 表：主标题 → KLCC、Badge 1 → 双子塔 VIEW…），**不会给旧文案**。旧文案要你自己从图里读出来。这就是 Step 2。

### Step 2 — 读图抄原文，列对照表给用户确认 ⭐

**这一步是整个 skill 成败的关键，不能跳。**

Read SAMPLE 图，把每个文字位置的**原文逐字抄下来**（verbatim，包括标点、空格、英文大小写），跟用户给的新文案配对成「旧 → 新」对照表。

然后把对照表贴给用户看，等确认。

为什么要停下来确认：模型是照「旧文案」去定位要改哪里的。你如果抄错一个字（例如把「免6个月Maintenance Fee」抄成「免 6 个月 Maintenance Fee」多了空格），模型可能定位不到那行，就会自己发挥。让用户扫一眼旧文案对不对，比出完图发现错了再重跑便宜得多。

对照表长这样：

```
主标题     BATU KAWAN            → KLCC
副标题     最适合投资的PROJECT    → KL 市中心最值得入手的 PROJECT
Badge 1    3房 LAYOUT            → 双子塔 VIEW
Badge 2    SEMI FURNISHED        → FULLY FURNISHED
Badge 3    RETURN 高达 6%        → RETURN 高达 7%
主 hook    打工族也可以负担的投资！ → 打工族也住得起的市中心黄金地段!
副 hook    低门槛 | 高Return      → 月供 RMxxxx | 高Return
Checkbox 1 免6个月Maintenance Fee → 免12个月Maintenance Fee
Checkbox 2 免SPA                  → （保留）
Checkbox 3 免律师费               → （保留）
右上角     [客户 logo 文字]       → （保留）
```

没变的 slot 也要列出来写「（保留）」—— 让模型知道那些是「确认过要留着」，不是「没提到所以随便」。

### Step 3 — 量 SAMPLE 尺寸 + 上传拿 CDN URL

先量原图尺寸，输出要跟它一样：

```bash
python3 -c "from PIL import Image; im=Image.open('<SAMPLE 绝对路径>'); print(im.size)"
# 没有 PIL 就用：file <SAMPLE 绝对路径>
```

```bash
python3 .claude/skills/lovart-api/agent_skill.py upload --file <SAMPLE 绝对路径>
# → {"url": "https://assets-persist.lovart.ai/img/.../xxx.jpg"}
```

凭证读环境变量 `LOVART_ACCESS_KEY` / `LOVART_SECRET_KEY`（由 `/course-setup-v2` 写进 `~/.claude/settings.json` 的 `env` 区块，每个 session 自动注入，不用 source 任何文件）。

报 401 / `Invalid access key` = 钥匙过期或没设，**别死磕签名逻辑**。直接告诉用户跑 `/course-setup-v2` 重新接一次 Lovart。

### Step 4 — 组 prompt，贴给用户看

严格三段结构，**贴出来给用户过目，确认才发**：

```
输出尺寸：<W>x<H>，跟附件参考图完全一样的画布比例。

100% 复刻附件这张广告图的设计、layout、配色、字体、badge 风格、整体调性，
只做下面这些文案替换：

[Step 2 的对照表，一行一个 slot]

唯一的视觉差异：[一句话，例：把建筑物从 A 换成 B + 背景加上 C]。其他全部不动。
```

**尺寸为什么跟 SAMPLE 走**：复刻的本质是让模型少做决策。指定一个跟 ref 图不同的尺寸，等于要它把现成排版重新塞进另一个画布 —— 那就是重新排版，正是我们要避免的事。跟 ref 同尺寸时模型可以逐像素对位，负担最小。

所以 `<W>x<H>` 填 Step 3 量到的原图尺寸，不要用固定值。

理想长度 **100–300 字**。超过 500 字基本就是过度 brief 了 —— 回头看看是不是又开始描述 layout 了。

如果用户没指定要换场景，第三段就写「无视觉差异，只换文字」。

**换场景时要说清楚换到哪个程度** —— 这里有个容易踩的坑：「其他全部不动」指的是 **layout / 文字 / 配色 / 字体 / 涂鸦笔触**，不是照片内容。如果第三段写成「把背景换成 X，保留原图的人物构图、镜头角度、前景层次」，模型会理解成「前景照片留着，只在背景塞个 X 进去」，出来就是半换不换的画面 —— 例如汽车贴膜广告的前景还是一群人在用笔记本电脑，逻辑上自相矛盾。

换场景就写整个画面换：「把画面场景从 A 换成 B，画面主体是 [B 场景里在做什么的人/物]」，别提「保留原图构图」。构图本来就会跟着 layout 一起保留，不用额外交代。

**再加一句商标防护**：模型会自己编行业里的真实品牌名当道具（贴膜车间生出 XPEL 招牌、咖啡店生出 Starbucks 杯）。这些是真实商标，投放会有风险。第三段末尾固定加：

```
画面中不要出现任何真实存在的品牌名称、logo、招牌文字；招牌和衣服上的品牌位置留白或用无意义的抽象图形。
```

### Step 5 — 出图

```bash
python3 .claude/skills/lovart-api/agent_skill.py chat \
  --attachments "<Step 3 的 CDN URL>" \
  --prefer-models '{"IMAGE":["generate_image_gpt_image_2_medium"]}' \
  --prompt "<Step 4 的 prompt>" \
  --json --download --output-dir <输出目录>
```

**参数为什么这样锁**：
- `gpt_image_2_medium` — high 贵约 4 倍，medium 已经够中文广告用。只有客户付费要打印 / 要超精细才升 high，升之前先问用户
- **尺寸跟 SAMPLE 原图走**（写在 prompt 里，不是命令参数）— 理由见 Step 4。用户要发特定平台需要别的尺寸时，先出复刻版再单独 resize，别在生成阶段改画布
- 别让 Lovart agent 自己路由模型，路由结果不可控

没等到结果就 `result --thread-id <ID> --json --download` 轮询。

**记下返回的 `thread_id`** —— Step 6 要用。

### Step 6 — 交付 + 记住 thread_id

把图给用户看，并明确报出 thread_id（续修要用）。

### Step 7 — 续修（同一个 thread）

用户要改时，**一律带 `--thread-id` 回到同一个 thread**：

```bash
python3 .claude/skills/lovart-api/agent_skill.py chat \
  --thread-id <上一次的 thread_id> \
  --prefer-models '{"IMAGE":["generate_image_gpt_image_2_medium"]}' \
  --prompt "保持上一张所有文案、layout、badge 位置、底部 checkbox bar、主标题 — 全部不变。
只换 [那一件事]：[具体怎么换]" \
  --json --download --output-dir <输出目录>
```

**为什么必须同 thread**：模型记得上一张是怎么来的，改动会 diff 在既有结果上。换新 thread = 从头重新理解 ref 图 = 整张构图可能都变样，前面调好的东西白费。

**一次只动 1–2 件事。** 一个 prompt 塞 5 项改动，模型注意力又散了，中文开始翻车 —— 跟 Step 4 那段是同一个道理。

续修示例（真实有效的写法）：
- 「场景从外景楼盘换成豪华大客厅室内，落地大窗能看到双子塔」
- 「整体调色往更金色走，增加金色 highlight、暖光、金箔感」
- 「右上角 logo 区清空留白，我后期叠真 logo」

出 variants 也走同 thread：「保持所有元素 100% 不变，生成 2 张 variant，差异只在 [某个视觉细节]」。

## 反模式（这些做了就会翻车）

| ❌ 不要 | 为什么 |
|---|---|
| 自己写「主视觉场景描述 + 文字内容清单 + 风格关键词」三段式 brief | 等于让模型重新设计，中文翻车率飙升 |
| 用文字描述 SAMPLE 里看得见的 layout（「右侧 3 圆 badge」「金色 serif 标题」） | ref 图本身就有，描述反而暗示模型可以改 |
| 在 prompt 里写「参考它的调性但自由设计新版面」 | 2026-06-03 第一轮翻车的直接原因 |
| 跳过 Step 2 直接把新文案塞进 prompt | 模型不知道要替换哪里，只能猜 → 重新设计 |
| 让 Lovart agent 自己路由模型 | 路由结果不可控，可能选到不擅长中文的模型 |
| default 用 `gpt_image_2_high` | 贵约 4 倍，medium 已经够 |
| 续修开新 thread | 模型重新理解 ref，前面调好的全丢 |
| 一个 prompt 塞 5 件改动 | 注意力分散，中文开始出错 |

## 已知瑕疵与善后

**Logo 通常是 AI 编的**（不是真 logo），即使复刻成功也一样。两种处理：
- Prompt 里直接说「右上角 logo 区留白」，用户后期自己叠真 logo
- 接受 AI 编的（远距离看不出来）

出图前主动问用户走哪种，别等交付了才发现 logo 不对。

**计费模式**：不急的话可以先 `set-mode --unlimited`（排队但 0 credit），急就保持 `fast`（烧 credits）。查当前模式 `query-mode`。

## 边界（什么时候不该用这个 skill）

| 情况 | 走哪个 |
|---|---|
| 拆爆款图抽公式，换到自己行业（**故意做得不一样**） | `viral-image-teardown` |
| 只拆 layout 入模板库，不出图 | `ad-imagegen-template-clone` |
| 改原图的一个元素，不重新生成整张 | `ad-image-edit` |
| 有 SAMPLE 但想走 ChatGPT OAuth 不烧 credits | `ad-imagegen-template-clone` + `ad-imagegen-template-use` |
| 从零创作，没有 SAMPLE | `creative-director` / `ad-creative-blitz` |

本 skill 的定位是 **同 layout、换文案、几乎一模一样**。只要用户想要的结果跟 SAMPLE「看起来是同一套设计的第二版」，就是这个 skill。

## 参考

完整方法论与行业 prompt 库：[200_Reference/2026-05-20_lovart-ai-playbook.md](../../../200_Reference/2026-05-20_lovart-ai-playbook.md)「玩法 9：SAMPLE 复刻法」
