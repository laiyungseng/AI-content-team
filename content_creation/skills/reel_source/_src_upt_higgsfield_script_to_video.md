---
source: UPT-course-setup-v2.skill / course-skills/higgsfield-script-to-video/SKILL.md.packed
original-skill: higgsfield-script-to-video
copied: 2026-10-31
status: staged
destination: reel_generation.md video section, only if Higgsfield is used (8b)
---
# Higgsfield Script → Video

「一份稿 → 完整 AI 真人 UGC 视频」的端到端 skill。默认马来西亚华人中文市场，走 Higgsfield MCP + Seedance 2.0 native omni multi-ref。

## When NOT to invoke

- 用户只是想「画一张广告图」→ 走 `ugc-ad-ref` / `creative-director` / `ad-imagegen-template-use`
- 用户想「拆爆款短视频」→ 走 `viral-video-teardown`
- 用户想「训练某个人的脸做后续 AI 生成」→ 走 `higgsfield-soul-id`
- 用户想「用 Lovart 出视频」→ 走 `lovart-api`
- 用户没有稿，只是「帮我想广告 idea」→ 走对话或 marketer-agent

## Explicit trigger（用户明说）

- `/higgsfield-script-to-video`
- 「用这个 skill 出 higgsfield 视频」
- 「照这份 spec/稿 出 AI 视频（3 shot / 多 shot）」
- 「按 Google Sheet 里的分镜出 Higgsfield 视频」

绝不 auto-trigger 模糊的「出视频 / 拍一支」请求。


## 核心哲学

1. **严格按稿执行**，不擅自加戏 / 减戏。用户 confirm 变更才改。
2. **分 phase confirm**，每一步跟用户对齐再走下一步。
3. **踩坑清单是这个 skill 最值钱的部分** — 见文末，一定看完。
4. **先出 1 支样片让用户 review**，OK 才批量。
5. **每一支视频都是钱**，preflight cost 用 `get_cost: true` 先看数字。


## 全流程 Phase 图

```
Phase 0  接稿 / 提取稿
Phase 1  素材盘点 + 逐条 confirm（人脸 / 场景 / 服装 / 音色）
Phase 2  切换 team workspace ⚠️ 最大踩坑
Phase 3  稿 + 时长 audit（用真人语速算能不能装下）
Phase 4  Media 上传 → media_confirm
Phase 5  Preflight cost → 出「Shot 1」样片
Phase 6  用户 review Shot 1，Approve 才批量
Phase 7  批量生成剩余 shots（parallel）
Phase 8  用 explainer_video 拼接成完整视频（"hyperframe"）
Phase 9  交付 + 记录可复用素材
```

---

## Phase 0 — 接稿 / 提取稿

### 输入形式

- Google Sheet URL（可能是原生 Google Sheet，也可能是 uploaded .xlsx）
- 直接贴 spec 文字
- 附文件（.xlsx / .md / .txt）

### 抓稿

- Google Sheet 原生：`mcp__google-workspace__get_google_sheet_content`
- xlsx：先 `mcp__google-workspace__download_file` → 用 python openpyxl 读全部 cell（示例见 `references/read-xlsx.py`）
- 别用 `export_file`（xlsx 不是 Google 原生格式，会报错）

### 定位「完整 Prompt」

用户的 spec 通常有多列。**只看用户明确指定的那一列**（例如「完整 Prompt（多参考 + 口型同步 全中文版）」），不要合并所有列。

### 输出

一份纯文本 `script.md`，包含：
- `[参考素材]` block（@Image1 / @Image2 / @Image3 / @Audio1 等占位符定义）
- `[全局风格]` block
- `[Shot 1]` / `[Shot 2]` / `[Shot N]` block（每支含 时长 + 主体 + 动作 + 场景 + 镜头 + 口型同步/台词）

---

## Phase 1 — 素材盘点

### 逐条 confirm 清单（用 AskUserQuestion 一次问完）

对稿里每一个 `@ImageN` / `@AudioN` 都要 confirm 一次：

**@Image1（人物脸）**
- (a) 用户已提供本地文件路径
- (b) 从旧客户档案里挑现有的
- (c) 用 `01portrait-ai-creator` 现出一张（先跳出这个 skill 去生成）

**@Image2（场景，如「银行分行门口 / 咖啡店内 / 店铺外景」等）**
- 用户的稿通常写「要求」（如「银行招牌清晰、门口空旷、自然日光」）
- 找图 3 步：
  1. 用 `mcp__firecrawl__firecrawl_search` 找一批 real photo（**排除 stock**：`-site:shutterstock.com -site:alamy.com -site:gettyimages.com -site:dreamstime.com`）
  2. 用 `mcp__firecrawl__firecrawl_scrape` + Google Maps Street View URL 抓真实街景（screenshots 格式，viewport 1400×900）
  3. 用 firecrawl_scrape 拉 mall interior / user-uploaded 真实照片
- 给用户开 3-5 张候选（用 macOS `open` 命令直接打开 preview），让他挑
- **允许用户改主意**：内景 / 外景都行，让用户拍板

**@Image3（服装）**
- 常见：跟 @Image1 是同一张证件照 → 复用 media_id
- 如果稿写「T 恤 + 卡其裤」但用户实际给的是「西装」 → 明确 confirm 走哪版（B 版走用户实拍照片风格）

**@Audio1（音色/口音参考音频）**
- 用户提供 → 用 Groq API + whisper-large-v3-turbo 转录一下**验证内容**（memory 里有 groq key）
- ⚠️ 转录后跟用户对齐音频用途：**音色参考** vs 硬 lipsync（几乎永远是音色参考）
- 用户没有 → 让他手机录 20-30s，用平时讲课的口气念稿里全部台词就行

### 输出

一份 `assets.md`：
```
@Image1 = /path/to/character.png       (AI 生成证件照)
@Image2 = /path/to/scene.jpg           (真实场景 real photo)
@Image3 = same as @Image1              (服装复用)
@Audio1 = /path/to/voice-sample.m4a    (音色参考，14s)
```

---

## Phase 2 — 切换 team workspace ⚠️ 最大踩坑

### 一定要先切！

Higgsfield MCP **默认不绑定任何 workspace**，会回落到 free individual workspace。这时候用 `image_references` / `audio_references` role 会 **403 "Pro or Ultimate required"**。

### 3 步操作

```
mcp__[higgsfield]__list_workspaces
→ 找 plan_type == "team" 的那个（通常是公司 shared workspace）
→ 拿它的 workspace_id

mcp__[higgsfield]__select_workspace(workspace_id=<team-id>)
→ 返回 is_selected: true 才算成功

mcp__[higgsfield]__balance
→ 确认 subscription_plan_type == "team" + credits 足够
```

### 常见团队账号名参考

- 「[brand] Ai Marketing」= [brand] 团队 team workspace
- 「Private」/ 未命名 shared = 私人 free workspace（**别用**）

### 错误信号（切错 workspace 会看到）

- `403 seedance_2_0 backend request failed: "Pro" or "Ultimate" plan required`
- `403 job_minimum_basic_plan_required`

看到这两个错误立刻回 Phase 2 重新切 workspace。

---

## Phase 3 — 稿 + 时长 audit

### 语速公式（用户 / [owner] 自然语速基准）

- 马来西亚华人正常语速 = **4-4.5 字 / 秒**
- 例子：60 字的 hook 台词，自然念完约 **13-14 秒**
- 如果稿写「Shot 1 = 8 秒」但台词 60 字 → **物理装不下**

### 时长 audit 清单

对每一 shot 数一次台词字数：

| 字数 | 建议时长 |
|---|---|
| < 20 | 5s |
| 20-35 | 8s |
| 35-55 | 10-12s |
| 55-70 | 12-14s |

### confirm 3 个选项（当时长与台词量冲突）

- **(A) 拉长视频** 保留原台词内容（推荐 — 卖点不砍）
- **(B) 砍台词** 保留原时长（容易砍掉核心 hook）
- **(C) 分片** 拆成 2 支 shot（节奏破碎）

Default 推 **A**，除非用户明确说砍台词。

### Prompt 结构规范

Prompt 严格按稿结构复制，只做用户 confirm 过的替换：

```
[全局风格 — 真人 UGC]
...（原文 verbatim）

[Shot N — X 秒]
使用「第二张参考图」作为场景。

[主体] 使用「第一张参考图」的人物脸和服装 — <照稿描述，加已 confirm 的服装>
[动作] <照稿动作 verbatim>
[场景] <照稿场景 verbatim，如果 @Image2 换过 location 名字要同步>
[镜头] <照稿镜头 verbatim>

[口型同步]
用参考音频里的马来西亚华人口音和音色，按自然语速讲以下台词：「<稿里的台词 verbatim>」
```

⚠️ **绝不擅自加戏**：不要把「手指」改成「食指」、不要把「[demo bank] 银行」改成「[demo bank] Bank」、不要加「蓝色」形容词 —— 除非用户明确 confirm。

---

## Phase 4 — Media 上传

### 上传 3 类 media

```
mcp__[higgsfield]__media_upload(files=[
  {filename: "character.png", content_type: "image/png"},
  {filename: "scene.jpg", content_type: "image/jpeg"},
  {filename: "voice.m4a", content_type: "audio/mp4"}
])
→ 拿到 3 组 {media_id, upload_url}

# 用 curl PUT bytes（每个 upload_url 有效 24h）
curl -X PUT -H "Content-Type: image/png" --data-binary @character.png "<upload_url>"
curl -X PUT -H "Content-Type: image/jpeg" --data-binary @scene.jpg "<upload_url>"
curl -X PUT -H "Content-Type: audio/mp4" --data-binary @voice.m4a "<upload_url>"

# 全部 HTTP 200 后 confirm
mcp__[higgsfield]__media_confirm(type="image", media_id=<character-id>)
mcp__[higgsfield]__media_confirm(type="image", media_id=<scene-id>)
mcp__[higgsfield]__media_confirm(type="audio", media_id=<audio-id>)
→ 3 个都返回 status: "uploaded"
```

### 记录 media_id

存在 `assets.md` 里，后续 shots / 批量 / 重跑都直接引用：
```
character-face      → 08345d43-a63f-4d40-ab1c-88235ca4a5e8
scene               → 967b4e02-f2d9-4b4d-b1e9-7f65938fc56c
voice-audio         → 99120e8d-e9c5-4e87-a582-ac145d389905
```

---

## Phase 5 — Preflight cost + 出 Shot 1 样片

### Preflight（不扣 credit，只看数字）

```
mcp__[higgsfield]__generate_video(params={
  model: "seedance_2_0",
  prompt: "<Shot 1 prompt>",
  duration: 12,
  resolution: "720p",
  aspect_ratio: "9:16",
  get_cost: true,  # ← 关键
  medias: [
    {role: "image_references", value: "<character-id>"},
    {role: "image_references", value: "<scene-id>"},
    {role: "audio_references", value: "<audio-id>"}
  ]
})
→ 返回 {cost: {credits: N}}
```

### 给用户看 cost

- Seedance 2.0 / 720p / 9:16 / 12s ≈ **36 credits**
- 5s ≈ 15 credits
- 8s ≈ 25 credits

用户 confirm 才 submit（去掉 `get_cost: true`）。

### Submit + poll

Submit 后返回 `job_id` + `status: "pending"`。

用 `job_display(id=<job_id>)` 查状态。Seedance 12s 通常 **3-5 分钟**完成。

**Poll 策略（sleep 被 harness block）**：
- 用 `Monitor` tool，command 类似 `sleep 150; echo "READY"`，timeout 200000ms
- 第一次 poll 建议 sleep 150s，然后每次 60-90s

### 完成后下载

```
curl -sL "<rawUrl>" -o downloads/<client>/shot1.mp4
open shot1.mp4   # macOS 用默认播放器打开给用户看
```

---

## Phase 6 — 用户 review Shot 1

### 明确 4 个 review 点

用 AskUserQuestion 让用户逐条 confirm：

- **人脸** — 像不像本人 / identity 有没有漂
- **场景** — 品牌招牌 / logo 有没有错
- **手势 & 动作** — 有没有做出稿里描述的手势
- **音色 & 口音** — 是不是马来西亚华人腔调

### review 结果分支

- ✅ **全通过** → Phase 7 批量生成
- ⚠️ **只有 1-2 点要修** → 调 prompt 里对应部分（人脸重跑要换 @Image1；音色不对要重录 @Audio1；场景不对要换 @Image2 重跑）
- ❌ **整支都不对** → 回 Phase 3 重新 audit 稿 or 换模型

---

## Phase 7 — 批量生成剩余 shots

### Parallel submit

一次调用多个 `generate_video`（不同 shots）。它们会 pending 并 parallel 生成。

```
# 一个 assistant 回合里同时 submit Shot 2 + Shot 3
mcp__[higgsfield]__generate_video(...Shot 2 params...)
mcp__[higgsfield]__generate_video(...Shot 3 params...)
```

### 记录所有 job_id

```
shot1_job = c82456fa-0b56-4a24-9aad-ca1e8284c064
shot2_job = b02cf25f-5980-4499-9365-920584b34c44
shot3_job = 53f6d0ce-60a6-47a7-afec-0372e4c2dcd9
```

### 一起 poll

用 Monitor 等 ~3 分钟后，一次 `job_display` 检查所有 job。全 `completed` 才走 Phase 8。

### 批量 review

3 支视频用 `open` 一起打开 QuickTime，让用户逐支过一遍。

同一 review 4 点（脸 / 场景 / 手势 / 音色）。有问题就重跑那一支。

---

## Phase 8 — 拼接（Higgsfield 网页 UI 叫「Hyperframe」，MCP 叫 `explainer_video`）

### 命名踩坑

用户可能说「用 hyperframe 拼」— 这是 Higgsfield 网页 UI 的功能名。MCP 里对应工具是 **`mcp__[higgsfield]__explainer_video`**。功能一样：把 N 支 clip 按顺序 stitch 成一支 mp4。

### 用法

```
mcp__[higgsfield]__explainer_video(params={
  width: 720,
  height: 1280,
  items: [
    {video: "<shot1_job_id>"},
    {video: "<shot2_job_id>"},
    {video: "<shot3_job_id>"}
  ]
  # 不加 subtitles（脚本明确禁字幕）
  # 不加额外 audio（每支 clip 已经有自己的 lipsync 音频）
})
```

### 特性

- **Free assembly**（0 credit）
- 一般 30-60s 完成
- 保留每支 clip 自带的 audio（lipsync 不会被覆盖）
- 输出 `width × height` 用源 clip 的分辨率（720×1280 for 9:16）

### 下载完整视频

```
curl -sL "<rawUrl>" -o downloads/<client>/final-<total-duration>s.mp4
open final-*.mp4
```

---

## Phase 9 — 交付 + 记录可复用素材

### 交付文件

```
downloads/<client>/
├── character-face.png              # @Image1
├── scene-<location>.jpg            # @Image2  
├── shot1.mp4                       # 单支
├── shot2.mp4
├── shot3.mp4
├── final-<total-duration>s.mp4     # 完整拼接版
├── script.md                       # Phase 0 输出
├── assets.md                       # media_id 清单
└── prompts.md                      # 每支 shot 的 final prompt
```

### 可复用素材记录

告诉用户：这些 media_id 已经上传到 team workspace，下次做同客户新视频**直接引用不用重传**：

```
Higgsfield team workspace media IDs:
- character-face  → 08345d43-...
- scene-<location> → 967b4e02-...
- voice-audio     → 99120e8d-...
```

### Cost summary

告诉用户今天花了多少 credits + workspace 剩多少。


---

# 踩坑清单（🚨 全部读完再动手）

按重要性从高到低：

### 1. Workspace 切换 — 不切必炸

- **症状**：`403 "Pro or Ultimate required"` / `403 job_minimum_basic_plan_required`
- **观察**：MCP 默认没绑定 workspace，生成请求会被拒绝。奇怪的是 `balance` 可能显示 team plan / 有 credits，**但生成端点仍拒**（balance 端点跟 generate 端点校验路径可能不同）— 所以别拿 balance 通过来推断 workspace 已绑定
- **解法**：Phase 2 必做 `list_workspaces` + `select_workspace(<team-id>)`
- **验证**：`select_workspace` 返回 `is_selected: true` 才算真切成功

### 2. Reference role 用法（不是 start_image）

- **稿里写 `[口型同步 @AudioN]`** 时，`@AudioN` 一定用 `audio_references` role，不是 `audio`
- **稿里的图** 一律用 `image_references` role，不是 `start_image`
- **CLI 版**（`higgsfield generate create`）**只暴露 start_image**，砍了 `image_references`。**不要用 CLI**，一律走 MCP
- 参考图数量：MCP 层可以 2+ 张 `image_references`（native omni），CLI 只能 1 张

### 3. Audio 是"音色参考"，不是硬 lipsync

- 稿里的 `[口型同步 @Audio1]` + 台词引号，很容易被误解成「把音频塞进视频硬对齐嘴形」
- **真实用法**：`audio_references` role 让 Seedance **学音色/口音**，然后按 prompt 里的台词**自己生成新音频**+ 对嘴
- 视频时长可以跟音频时长**不匹配**，Seedance 会按视频时长自己调节奏
- Prompt 里明写「用参考音频里的口音和音色，按自然语速讲以下台词：...」

### 4. 时长与内容量匹配

- 稿里的时长是编剧初稿假设，不一定跟真人语速匹配
- **规则**：用 4-4.5 字/秒 算，用户 confirm 时长是否要拉长
- 60 字硬塞 8s 会生成 1.75x 语速的怪视频，且手势节奏全乱

### 5. Composite first-frame vs native omni

- CLI 时代要 composite（用 GPT Image 2 把人 + 场景合成一张）→ 走 start_image
- MCP + team workspace **不需要 composite**，直接 `image_references` 多张
- **只有一种情况要 composite**：workspace 或 plan 限制拿不到 native omni

### 6. Setapak vs Utropolis 场景类型

- 用户稿里写「银行外景，招牌清晰、门口空旷、自然日光」时：
  - **不要用 Google Street View** — 街景通常门口停一排车，Google 又打 blur
  - **优先用 real photo**（用户上传的真实拍摄 / 商场里的银行分店 official 照片）
  - **室内/商场里的分行也可以**（用户会 confirm）— 招牌反而更清晰、门口更空旷

### 7. 禁 stock photo

- 用户 memory 里明说过：**Unsplash / Pexels / Getty / Shutterstock / Alamy / Dreamstime 全部禁用**
- firecrawl_search 加 `-site:shutterstock.com -site:alamy.com -site:gettyimages.com -site:dreamstime.com` 过滤

### 8. Preview 浏览器 rendering Google Maps 会挂

- Preview browser (`preview_start`) 打开 Google Maps 会渲染不出街景（黑屏）
- **改用 `firecrawl_scrape` + Google Maps URL** + `formats: ["screenshot"]` 服务端渲染
- Street view URL 格式：`https://www.google.com/maps/@LAT,LNG,3a,75y,YAWh,90t/data=!3m6!1e1!3m4!1s0!2e0!7i16384!8i8192`
- 调 yaw (0/90/180/270) 换视角

### 9. Google Sheet 是 xlsx 还是 native

- URL 里带 `rtpof=true&sd=true` 通常是**上传的 xlsx**（不是 Google 原生 Sheet）
- `get_google_sheet_content` 会失败 → 改用 `download_file` + openpyxl 读

### 10. Sleep 命令被 harness block

- Bash 里 `sleep 60` 以上会被 block
- 用 `Monitor` tool + `sleep 150; echo READY` command，timeout 200000

### 11. Seedance 生成时间预期

- 12s 视频 @ 720p / 9:16 / std mode ≈ **3-5 分钟**
- 5s 视频 ≈ 2-3 分钟
- Parallel submit N 个 job，backend 会 queue，总时间 ≈ max(单个) + 少量 overhead

### 12. Skill 权限 gate

- 团队用户第一次跑这个 skill 前，必须先在 Higgsfield dashboard 上确认自己被加进公司 team workspace（作为 member 或 owner）
- 没被加进去 → `list_workspaces` 看不到 team workspace → 永远只能用 free plan
- 让 owner 去 Higgsfield → Workspace Settings → Invite member 加进来

### 13. 不擅自加戏

- Prompt 严格按稿 verbatim，不要自己「优化」措辞
- 「手指」不要改「食指」；「银行」不要英文化；不要加「蓝色」形容词
- 除非用户明确 confirm 变更


---

# Quick Reference — MCP Tool 对照表

| 需求 | Tool |
|---|---|
| 切 workspace | `list_workspaces` + `select_workspace` |
| 查 balance | `balance` |
| 查模型能力 | `models_explore(action="get", model_id="seedance_2_0")` |
| 上传 media（本地文件） | `media_upload` + curl PUT + `media_confirm` |
| 上传 media（web URL） | `media_import_url` |
| 生成视频 | `generate_video` |
| 查 job 状态 | `job_display(id=<job_id>)` |
| 拼接多支 clip（hyperframe） | `explainer_video` |
| 查已上传素材 | `show_medias(type="image" \| "audio" \| "video")` |
| 升级付款 widget | `show_plans_and_credits(intent="upgrade")` |

---

# 附录：完整跑一次的 checklist

Print 出来给团队第一次跑用：

- [ ] Phase 0 稿抓好，看的是「完整 Prompt」那一列
- [ ] Phase 1 素材 4 类全部 confirm（人 / 场景 / 服装 / 音色）
- [ ] Phase 2 `list_workspaces` → select team workspace → balance 显示 team plan
- [ ] Phase 3 时长 audit 完成，字数 vs 秒数对齐
- [ ] Phase 4 3 个 media 全部 `status: uploaded`
- [ ] Phase 5 preflight cost 用户 confirm，Shot 1 submit + poll + download
- [ ] Phase 6 用户逐点 review Shot 1（脸/场景/手势/音色），approve
- [ ] Phase 7 剩余 shots parallel submit + poll + download
- [ ] Phase 8 `explainer_video` 拼完整版
- [ ] Phase 9 交付 + 记 media_id + cost summary

by [brand] & [owner] — 2026-07-12 一次完整实战踩坑总结（银行融资 3-shot 案例）
