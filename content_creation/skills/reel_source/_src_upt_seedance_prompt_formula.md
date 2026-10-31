---
source: UPT-course-setup-v2.skill / course-skills/viral-sales-video-clone/references/seedance-prompt-formula.md
copied: 2026-10-31
status: staged
destination: reel_generation.md (8b)
---
# Seedance Prompt 6 要素结构 + @Image 参考语法

## 一、6 要素英文架构（第 2 列用）

每个 Shot 的英文 Seedance Prompt 必须包含这 6 段：

```
Use @Image2 for the [scene] context. 1 shot, [duration]s, 9:16.
[Subject] <who is in frame — physical description, clothing, props>
[Action] <what they do, gesture-by-gesture, in order>
[Setting] <where, lighting, background elements>
[Camera] <shot size, POV, movement, angle>
[Style] <aesthetic reference — vlog / UGC / iPhone POV>
```

**关键要点：**
- 第 1 句必须先声明用哪个 `@Image` reference（场景 / 人物）
- 时长写具体秒数（原视频每个 shot 时长）
- 画幅默认 `9:16`（TikTok / Reel / Shorts）
- `[Action]` 里动作要**按顺序**写（第 1 个手势 → 第 2 个手势 → 结束姿态），因为 Seedance 会按序解析
- `[Style]` 强调 **raw iPhone footage / no VFX / natural skin texture**（反 slop 关键词）

---

## 二、6 要素中文架构（第 5 列用）

第 5 列是第 2 列的中文对照版，字段照译：

```
使用 @Image2 作为 [场景] 场景。单镜头，[N] 秒，9:16 竖屏。
[主体] <角色描述 + 服装 + 道具>
[动作] <动作 1 → 动作 2 → 结束姿态>
[场景] <地点 + 光线 + 背景元素>
[镜头] <景别 + 视角 + 运动 + 角度>
[风格] <UGC / 手机原生 / 真实肌肤纹理>
```

---

## 三、@Image / @Audio 参考语法

Seedance 支持多参考（multi-ref）注入。命名约定：

| 参考编号 | 用途 | 例 |
|---|---|---|
| `@Image1` | **角色脸** — AI 生成的一致人物形象（避免每 shot 换脸） | 融资顾问脸 / 清洁工阿姨脸 / 老板娘脸 |
| `@Image2` | **场景** — Google Maps 街景截图 / 实拍空景 / 3D 渲染背景 | [demo bank] 银行门口 / 客户家门口 / 办公室 |
| `@Image3` | **服装** — 主体人物的固定 outfit | 深色 T 恤 + 卡其裤 / 粉色制服 / 老板娘装 |
| `@Audio1` | **口音参考** — 用于口型同步的目标口音音频 | 大马华人口音 / 广东话 / Manglish |
| `@Image4+` / `@Audio2+` | 可扩展（次要道具、辅助配角、BGM 音源等） | 手机屏幕特写 / 产品包装 / 环境音 |

---

## 四、第 6 列「完整 Prompt」四段结构

```markdown
[参考素材]
@Image1 = <角色脸描述 + 生成/采集方式>
@Image2 = <场景描述 + 采集要求：招牌是否清晰 / 光线要求 / 构图要求>
@Image3 = <服装描述 + 简约干净的关键词>
@Audio1 = <口音描述 + 待提供 / 已提供>

[全局风格 — 真人 UGC]
<完整嵌入 references/ugc-anti-slop-rules.md 的铁律原文>

[Shot N — X 秒]
使用 @Image2 作为 <场景> 场景。

[主体] 角色 @Image1 穿着 @Image3 — <人物身份 + 表情/状态>。
[动作] <动作 1 → 动作 2 → 结束姿态>。
[场景] <地点 + 光线 + 背景元素>。
[镜头] <景别 + 视角 + 运动>。**不是稳定器，不是顺滑跟拍。**

[口型同步 @Audio1]
「<完整讲稿。含本地化调整：RM 750,000 → 75 万；form → 表单；CTOS → 信用评分；agency → 代理>」
```

**四段的顺序固定，不可换：**
1. `[参考素材]` — 让 Seedance 先知道所有 ref
2. `[全局风格 — 真人 UGC]` — 全局风格锁死
3. `[Shot N — X 秒]` — 当前 shot 详情
4. `[口型同步 @Audio1]` — 音轨对齐

---

## 五、口型同步讲稿本地化调整规则

Voice Over 从原视频转写出来后，写进 `[口型同步 @Audio1]` 时要做本地化：

| 原文（写稿） | 口型同步版（口播） |
|---|---|
| RM 750,000 | 75 万 |
| RM 3,000 | 3 千 |
| [demo product] Loan | [demo product] 融资 / 这个融资 |
| form | 表单 / 单 |
| CTOS 不美 | 信用评分不美 |
| solution | 方案 |
| agency | 代理 |
| 3.75% | 3.75 percent（口播） |

**原则：数字口播用中文习惯读法；英文行业术语该保留就保留（用户已确认调性是 Manglish 就更 OK 保留），但**过长的英文数字/单位一定要转成中文口播友好版**（不然 lip-sync 会怪）。

---

## 六、每 Shot 时长参考（跟原视频）

- Hook / 痛点段：**5–8 秒**（够快够狠）
- 引入方案：**7–10 秒**
- 信任背书 / Proof：**5–10 秒**
- CTA：**3–5 秒**（越短越有力，语气上扬收尾）

**原则**：跟原视频的每 shot 时长。不改。

---

## 七、Sanity Check（生成第 2 / 5 / 6 列前自查）

- [ ] `Use @Image2` 出现在第 1 句
- [ ] 时长 + 画幅明确（`8s, 9:16`）
- [ ] `[Subject]` / `[Action]` / `[Setting]` / `[Camera]` / `[Style]` 5 段齐全
- [ ] `[Action]` 里动作按序写（不是一坨形容词）
- [ ] `[Style]` 含 `raw iPhone / vlog / no VFX / natural skin` 关键词
- [ ] 第 6 列的四段结构完整
- [ ] 讲稿数字/术语已本地化到口播版

任何一项 ❌ → 补齐再交付。
