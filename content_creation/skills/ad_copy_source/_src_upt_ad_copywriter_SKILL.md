---
source: UPT-course-setup-v2.skill / course-skills/ad-copywriter/SKILL.md.packed
original-skill: ad-copywriter
copied: 2026-10-31
status: staged
destination: ad_copy_longform.md (8b)
---
# Ad Copywriter Skill

专做马来西亚中文市场 long-form FB 广告文案。

## 设计哲学

- **方法论 = 骨架**：SNICK.C 6 元素 (必有) + 6 段流程 (结构) + Hook 加权 random (开头)
- **客户品牌调性 = 必喂**：每次跑 skill 必须收 user 给的 Client MD（含核心卖点 / USP）+ 当次主推什么
- **Pure executor**：skill **不脑补**、不从 Client MD 抽 menu 让 user 选、不自作主张加细节
- **缺 input 就 STOP 问**：5 必填 slot 缺一个就 stop，问 user，不靠猜
- **5 个 portable 文件 zero PII**：skill folder 自带规则不依赖外部 sample，包装出去安全 share

## 你需要读懂的 5 个文件

| 文件                    | 什么时候读 | 用途                                                     |
| :-------------------- | :---- | :----------------------------------------------------- |
| `hook-library.md`     | 每次跑必读 | Top 15 hook 类型 + 实例（开头怎么开）                             |
| `snickc-checklist.md` | 每次跑必读 | SNICK.C 6 元素定义 + 在 long-form 哪段出现 + 自检规则               |
| `style-guide.md`      | 每次跑必读 | 马来西亚中文市场 Rojak 风格 5 铁则 + emoji 规则 + 长度规则               |
| `framework.md`        | 每次跑必读 | 6 段骨架 + 5 marker 模式 + Hook 加权 random + 行业长度区间 + CTA 模板 |
| `_prompt.md`          | 每次跑必读 | 核心 prompt 骨架（组装上面 4 个 piece + execution pipeline）      |

---

## 执行流程（8 步）

### Step 1: Detect input

用户调用方式可能是：
- `/ad-copywriter`（裸调用，无参数）
- `/ad-copywriter [client]` 或 `/ad-copywriter 帮我写 [client] 的广告`（含客户名 / 自然语言）
- 「用 ad-copywriter 帮我写 [客户] 的广告」（自然语言触发）

不假设固定路径，不假设固定客户。

### Step 2: Read 4 个 portable 配置文件

按顺序 read：
1. `hook-library.md`
2. `snickc-checklist.md`
3. `style-guide.md`
4. `framework.md`

把它们全部加载进 context（每个文件不长，全读完总共约 2000 字）。

### Step 3: Ask Sample（可选）

问 user：

> 这次有 sample 文案要参考吗？
> 1. 有，我贴/给路径
> 2. 没有，直接 proceed

如果有 sample → 读完后用作 **额外风格 ref**（不是骨架替代，骨架仍按 `framework.md`）。
如果没有 → proceed，靠 `framework.md` 抽象规则 + `hook-library.md` 已足够。

### Step 4: 收集 5 个必填 slot

缺任何一个就 STOP 问 user，**不靠猜**。

| Slot | 说明 |
|:--|:--|
| **1. Client MD** | User 给路径 / 贴内容 / 给客户名（如果客户名能在 `200_Reference/client-profiles/` 找到对应 .md 就 read，否则 STOP 问 user 要 MD）|
| **2. 这次主推什么** | Pure user input（核心卖点 / promo / 招生 / 产品新品 / 等）。**禁止从 Client MD 抽 5 个让 user 选**（守 [owner] feedback：不从 Client MD 抽 menu）|
| **3. 平台** | FB / IG / TikTok / WhatsApp broadcast / etc（影响 emoji 用法 / 长度 / CTA 风格）|
| **4. 输出条数** | Default 5 |
| **5. 每条长度** | Default 中等（按 framework.md 行业长度区间。若 user 给 sample 则参考 sample 长度区间）|

**可选 override**（不传则用 style-guide.md 默认值）：
- 语言（默认马来西亚中文。**Skill 不写英文/马来文**，需要的话用 /ad-copywriter-en 或 /ad-copywriter-my，未来建）
- Emoji ON/OFF（默认 ON 因为 long-form FB 广告 emoji 是 marker 系统的一部分）

### Step 5: Generate N 条变体（N = Step 4 输出条数）

对每一条变体：

1. **Hook 加权 random**：按 `framework.md` 的 Hook 加权权重（痛点反问 ×4 / 结果前置 ×2 / 数字震撼 ×2 / 其他 ×1）random 抽一个 hook 类型
2. **N 条必须 N 个不同 hook**（禁止偷懒重复）
3. 套 `framework.md` **6 段骨架**：Hook → ❌ Pain → 转折 → ✅ Solution + 📌 Knowledge → 🏆 Certified Proof → 🔥 Scarcity + CTA
4. SNICK.C 6 元素融入 6 段中（不分段标签 `[S]` `[N]` —— 融入式 natural 出现）
5. 套 `style-guide.md` 的 5 条 Rojak 铁则 + emoji 规则
6. 长度按 Step 4 长度 slot

### Step 6: Self-check 每一条

对每条变体跑 `snickc-checklist.md` 的 6 元素 self-check：

- [ ] S (Solution) 出现了吗？
- [ ] N (Numbers) 至少 1 处？
- [ ] I (Issue) 痛点段写了吗？
- [ ] C (Certified Proof) 资历/认证 mention 了吗？
- [ ] K (Knowledge) 教育性内容（STEP/方法）有吗？
- [ ] .C (Scarcity AND CTA) **两个都有**吗？（不是二选一）

缺哪个补哪个，self-check 不放过。

### Step 7: Output

对话内输出 N 条变体，每条按以下格式：

```
=== 变体 1 ===
[Hook 类型：痛点反问式]

[完整 long-form 文案，含 emoji + marker + 段落]

#hashtag1 #hashtag2 ... #hashtag-n
```

每条之间空 1 行分隔。**No 存档 default** —— user 说「这条好，存起来」才存（路径由 user 指定，skill 不假设存档路径）。

### Step 8: 收 Sample 拆解（如果 Step 3 user 给了 sample）

如果 Step 3 user 给了 sample，Step 7 输出后问 user：

> 这次 sample 拆出来的风格特征（长度区间 / 句式 / 特殊 marker / 等），要存档吗？路径？
> 1. 不存，ad-hoc 用完即弃
> 2. 存，路径：____（user 指定）

如果存 → 写一份 sample-patterns 文件到 user 指定路径（可参考 `framework.md` 的格式）。

---

## 红线（绝对守的规则）

1. **不自动 trigger**：description 已写明 explicit-only。被普通「写文案 / 写 post」请求触发时**婉拒**说「这是 explicit-only skill，确认要用请明说 /ad-copywriter」
2. **不从 Client MD 抽 menu**：核心卖点必须 user 当场输入，禁止 skill 从 MD 抽 5 个让 user 选
3. **不主动 write back Client MD**：skill 只读不写客户档
4. **N 条变体必须 N 个不同 hook**：禁止偷懒重复 hook 类型
5. **每条 SNICK.C 6 元素必须齐**：缺哪个补哪个，self-check 不放过
6. **只写马来西亚中文市场**：英文 / 马来文需要的话用其他 skill（未来建 /ad-copywriter-en /ad-copywriter-my）
7. **不写图文创意 / 视觉物**：那些走 ugc-ad-ref / creative-director / ad-imagegen-template-use
8. **永远不写「马来华人」**：正确说法「马来西亚华人」/「马来西亚中文市场」

---

## 失败模式 → 怎么处理

| 失败 | 处理 |
|:--|:--|
| User 没给 Client MD 直接说「帮我写广告」 | STOP，问「客户是谁？给我 MD 路径 / 贴内容 / 客户名」|
| User 给客户名但你找不到对应 client-profile MD | STOP，问「找不到 [客户].md，请贴 MD 内容或换路径」|
| User 没说核心卖点 | STOP，问「这次主推什么？（不要让我从 MD 抽，pure user input）」|
| User 说「全部用一样的 hook 写 5 条」 | 拒绝，解释「N 条必须 N 个不同 hook 是 skill 红线，要不然降为 1 条用那个 hook？」|
| 跑出来文案太 over rojak（lah/hor 堆砌）| 自检 style-guide.md 5 铁则第 1 条（英文限 noun+adj），修正重写 |
| User 要写英文 / 马来文广告 | 拒绝，解释「这 skill 只写马来西亚中文。英文 / 马来文版未来建 /ad-copywriter-en /ad-copywriter-my」|
