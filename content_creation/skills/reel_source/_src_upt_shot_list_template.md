---
source: UPT-course-setup-v2.skill / course-skills/viral-sales-video-clone/assets/output-template.md
copied: 2026-10-31
status: staged
destination: reel template (8b)
---
# 六列 Seedance Shot List 空白模板

> **使用**：Step 5 输出时，把 `<变量>` 全部替换成用户案例的实际内容。**shot 数量跟原视频**（不写死 3 个 shot）。

---

## 空白模板

| Shot (镜头) | Seedance Prompt (英文 6 要素) | Voice Over Script (旁白中文) | Reference Image (素材准备) | Seedance Prompt (中文版) | 完整 Prompt（多参考 + 口型同步 全中文版） |
|---|---|---|---|---|---|
| **Shot 1: <功能标签>** | Use @Image2 for <场景> context. 1 shot, <N>s, 9:16. [Subject] <who> [Action] <action seq> [Setting] <where> [Camera] <shot size / POV> [Style] Authentic Instagram Reel vlog style, raw iPhone footage, natural skin texture, no VFX. | "<VO 原话中文>" | @Image2 — <场景说明>\n\n📝 CapCut overlay: "<屏幕字眼 / emoji>" | 使用 @Image2 作为 <场景> 场景。单镜头，<N> 秒，9:16 竖屏。[主体] <人物> [动作] <动作序列> [场景] <地点+光线> [镜头] <景别> [风格] 真实竖屏短视频风格，手机原生质感，自然肌肤纹理，真实光线，无特效。 | `见下方 Shot 1 完整 Prompt 展开块` |
| **Shot 2: <功能标签>** | ... | ... | ... | ... | ... |
| **Shot 3: <功能标签>** | ... | ... | ... | ... | ... |

---

## 第 6 列「完整 Prompt」展开块（每个 Shot 一份）

### Shot 1 完整 Prompt

```
[参考素材]
@Image1 = <角色脸描述>
@Image2 = <场景描述 + 采集要求>
@Image3 = <服装描述>
@Audio1 = <口音描述>

[全局风格 — 真人 UGC]
真人朋友视角第一人称短视频。手机原生拍摄，未经修饰，竖屏 9:16，手持自然抖动加呼吸感微晃，偶尔轻微对焦漂移。竖屏短视频抓拍美学，业余拍摄感，构图略微不完美。柔和自然环境光，无人工补光，真实肌肤纹理可见毛孔。绝对禁止：字幕、音乐、覆盖层、特效、调色、电影感、稳定器顺滑运镜、高清锐利度、专业运镜动作。

[Shot 1 — <N> 秒]
使用 @Image2 作为 <场景> 场景。

[主体] 角色 @Image1 穿着 @Image3 — <人物描述>。
[动作] <动作 1 → 动作 2 → 结束姿态>。
[场景] <地点 + 光线 + 背景>。
[镜头] <景别 + 视角>。不是稳定器，不是顺滑跟拍。

[口型同步 @Audio1]
「<讲稿口播版，含本地化调整>」
```

### Shot 2 完整 Prompt

```
（同上结构，替换成 Shot 2 内容）
```

（依此类推，跟原视频段位数）

---

## 表格底部：Reference Image 采集清单

生成完表格后，附上这一块：

```markdown
## 📸 Reference Image / Audio 采集清单

| Ref | 内容 | 采集方式 / 要求 |
|---|---|---|
| @Image1 | <角色脸> | AI 生成（可用 Midjourney / GPT-image-2 / Lovart 出 3 视图），要求：<马来西亚华人特征 / 年龄段 / 表情基调> |
| @Image2 | <主场景> | <Google Maps 街景截图 / 实拍空景 / 3D 渲染>，要求：<招牌清晰 / 门口空旷 / 自然日光> |
| @Image3 | <服装> | <描述 + 简约干净关键词>，采集：<实拍 / 参考电商 SKU 图> |
| @Audio1 | <口音参考> | 大马华人口音样本（30 秒以上，含目标讲稿关键词），采集：<自己录 / 找配音员> |
```

---

## 填好的 Demo（示范格式，不是给用户抄的）

**⚠️ 这是格式示范。用户案例出图时，不要抄这里的行业 / 卖点 / 场景。**

| Shot (镜头) | Seedance Prompt (英文 6 要素) | Voice Over Script (旁白中文) | Reference Image (素材准备) | Seedance Prompt (中文版) | 完整 Prompt |
|---|---|---|---|---|---|
| **Shot 1: 痛点钩子** | Use @Image2 for the salon exterior context. 1 shot, 6s, 9:16. [Subject] A young Malaysian Chinese female salon owner in a black tee, hair slightly messy. [Action] She looks straight at camera with a tired expression, raises one hand to her forehead in an exhausted gesture, then shakes her head in disbelief. [Setting] Standing at her salon entrance, evening natural light, salon signage visible behind. [Camera] Medium close-up, handheld iPhone POV, subtle push-in, eye-level. [Style] Authentic Instagram Reel vlog style, raw iPhone footage, natural skin texture, no VFX. | "开美容院最痛的是什么？不是没客人，是每个月员工薪水一发出去，自己口袋剩下 RM 300。" | @Image2 — 美容院大门外景，傍晚自然光\n\n📝 CapCut overlay: "开美容院 3 年 / 月入 8 万 / 自己剩 RM 300 😩" | 使用 @Image2 作为美容院外景场景。单镜头，6 秒，9:16 竖屏。[主体] 一位年轻的马来西亚华人女性美容院老板，穿黑色 T 恤，头发略乱。[动作] 直视镜头，表情疲惫，一手扶额做出「累坏了」的手势，然后摇头表示难以置信。[场景] 站在美容院大门前，傍晚自然光，招牌可见。[镜头] 中近景，手持手机视角，轻微推进，平视。[风格] 真实竖屏短视频，手机原生质感，自然肌肤纹理，无特效。 | 见下方展开 |

**Shot 1 完整 Prompt（demo）：**

```
[参考素材]
@Image1 = 美容院老板角色脸（AI 生成，30 岁马来西亚华人女性，略带疲惫感）
@Image2 = 美容院大门外景（Google Maps 街景截图，要求：招牌清晰、傍晚自然光、街道略微行人往来）
@Image3 = 服装（黑色素色 T 恤 + 深色牛仔裤，简约疲惫感）
@Audio1 = 大马华人女性口音参考（待提供）

[全局风格 — 真人 UGC]
真人朋友视角第一人称短视频。手机原生拍摄，未经修饰，竖屏 9:16，手持自然抖动加呼吸感微晃，偶尔轻微对焦漂移。竖屏短视频抓拍美学，业余拍摄感，构图略微不完美。柔和自然环境光，无人工补光，真实肌肤纹理可见毛孔。绝对禁止：字幕、音乐、覆盖层、特效、调色、电影感、稳定器顺滑运镜、高清锐利度、专业运镜动作。

[Shot 1 — 6 秒]
使用 @Image2 作为美容院外景场景。

[主体] 角色 @Image1 穿着 @Image3 — 年轻的马来西亚华人女性美容院老板，头发略乱，表情疲惫。
[动作] 直视镜头，表情疲惫，一手扶额做出「累坏了」的手势，然后摇头表示难以置信。
[场景] 站在美容院大门前，傍晚自然光，招牌清晰可见在身后。
[镜头] 中近景，手持平视，自然身体晃动。不是稳定器，不是顺滑跟拍。

[口型同步 @Audio1]
「开美容院最痛的是什么？不是没客人，是每个月员工薪水一发出去，自己口袋剩下 3 百块。」
```

---

**⚠️ 再提醒**：上面 demo 是**美容院行业**的示范。用户跑真实案例时（银行 / 汽车 / 教育 / 叉车 / 装修 / 餐饮 / 电商...），**换掉行业 / 卖点 / 场景 / 人物**，只保留结构骨架。
