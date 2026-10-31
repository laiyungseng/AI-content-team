---
source: UPT-course-setup-v2.skill / course-skills/ad-copywriter/framework.md
copied: 2026-10-31
status: staged
destination: ad_copy_longform.md, cta.md (8b)
---
# Framework · 6 段骨架 + Marker 模式 + Hook 加权 + CTA 模板

> Skill 内置文件 · Portable · Zero PII
> 用途：`/ad-copywriter` skill 每次跑必读
> 抽象自 40 个真实爆款广告 sample 框架分析（sample 原文不进 skill folder）
> v1 · 2026-06-24

---

## 1. 6 段骨架（所有 long-form FB 广告共用）

```
┌─────────────────────────────────────────┐
│ 段 1: HOOK                              │ ← 抓眼球（1-5 行）
│   开头 1-3 行，配 emoji 情绪标记         │
├─────────────────────────────────────────┤
│ 段 2: PAIN（Issue 深化）                 │ ← 戳痛点
│   ❌ bullet list 列 3-5 个痛点          │
│   或故事化反问                            │
├─────────────────────────────────────────┤
│ 段 3: 转折 + SOLUTION + KNOWLEDGE       │ ← 给希望 + 教方法
│   💡 转折句「其实真正的问题是 XXX」      │
│   ✅ 介绍解决方案 / 产品 / 课程            │
│   📌 STEP 1-5 详细方法                   │
├─────────────────────────────────────────┤
│ 段 4: CERTIFIED PROOF                   │ ← 建立信任
│   🏆 资历列表（年限 / 案例数 / 认证）     │
│   导师介绍 / 公司介绍                     │
├─────────────────────────────────────────┤
│ 段 5: SCARCITY + 限时优惠                │ ← 制造紧迫
│   🔥 限时 / 限名额 / 数量有限              │
│   📅 日期 / 优惠幅度 / 原价对比            │
├─────────────────────────────────────────┤
│ 段 6: CTA + 联系 + #hashtag             │ ← 行动指令
│   👉 WhatsApp / Link / 电话              │
│   📍 地址（实体服务必有）                  │
│   #hashtag 集群（8-15 个）               │
└─────────────────────────────────────────┘
```

每段用 `.`（单独一行的句号）分隔。整体长度按 `style-guide.md` 行业长度区间。

---

## 2. Hook 加权 Random（40 sample 真实统计）

`hook-library.md` 有 15 个 hook 类型。**但实际使用频率不是平均** —— 按 40 sample 真实统计加权：

| Hook 类型 | 权重 | 占 40 sample 比例 |
|:--|:--:|:--:|
| Hook 01 痛点反问式 | **×4** | 45% ⭐ 主力 |
| Hook 12 同理共鸣式 | ×4 | （并入痛点反问统计）|
| Hook 02 数字震撼式 | **×2** | 15% |
| 结果前置（Hook 15 利益直击式 + 部分 Hook 02）| **×2** | 17.5% |
| Hook 08 故事钩式 | ×1.5 | 12.5% |
| Hook 04 秘密揭露式 | ×1.5 | 10% |
| Hook 05 反差对比式 | ×1.5 | 10% |
| Hook 06 权威背书式 | ×1 | 7.5% |
| 其他 hook（03/07/09/10/11/13/14）| ×1 each | 总占 ~5% |

### 加权 random 实现

每条变体选 hook 时：
1. **N 条必须 N 个不同 hook**（已 enforced 红线）
2. 抽取池按上面权重 sample（不是均匀 random）
3. 但**视客户行业微调**：保健品 / B2B 课程 → 权威背书 weight 升 1.5；房产 / 投资 → 数字震撼 weight 升 1.5；美食 → 利益直击 + 数字对比 weight 升 1.5

### N 条变体的 hook 抽法示例

User 要 5 条变体（default）→ 推荐 hook 组合：
- 1× 痛点反问（main）
- 1× 数字震撼 或 结果前置
- 1× 故事钩 或 秘密揭露
- 1× 反差对比 或 权威背书
- 1× 其他随机

User 要 3 条 → 选前 3 个 main hook
User 要 10 条 → 全 15 个 hook 选 10 个（按权重 sample）

---

## 3. 5 大 Marker 模式

### 模式 A：痛点列表（❌）
```
❌ 痛点 1
❌ 痛点 2  
❌ 痛点 3
```
**用在段 2 PAIN**。3-5 条最佳，太多 reader 疲惫。

### 模式 B：解决方案列表（✅）
```
✅ 解决方案 1
✅ 解决方案 2
✅ 解决方案 3
```
**用在段 3 SOLUTION**。常跟模式 A 在同一段内做 before/after 对比。

### 模式 C：知识点分步（📌 + 编号）
```
📌 STEP 1：xxx
[2-3 行细节]
.
📌 STEP 2：xxx
[2-3 行细节]
.
📌 STEP 3：xxx
[2-3 行细节]
```
**用在段 3 KNOWLEDGE**。3-5 个 STEP 最佳。每个 STEP 后面带 2-3 行细节解释，不只是标题。

### 模式 D：资历背书（🏆）
```
🏆 资历 1（年限）
🏆 资历 2（认证 / 奖项）
🏆 资历 3（客户数 / 案例数）
🏆 资历 4（其他亮点）
```
**用在段 4 CERTIFIED PROOF**。导师介绍段或公司介绍段独立成块。

### 模式 E：彩色多列表（💚 💜 🩷）
```
💚 [项目 1] | [说明]
💜 [项目 2] | [说明]
🩷 [项目 3] | [说明]
```
**用在段 3 SOLUTION**（多服务/多产品并列时）。常用于美容、健康、套餐 / 配套类。

---

## 4. CTA 段模板（段 5-6）

固定结构：

```
[紧迫感声明]
"名额有限，先到先得"
"不要再等"
"数量有限，送完即止"
"错过要等下一炉"
↓
[具体优惠信息]
"限时优惠"
"首 X 位免费 / 折扣 XX%"
"原价 RM XXX，现在只需 RM XXX"
"赠送 RM XXX 的 [bonus]"
↓
[多个 CTA 渠道]
👉 WhatsApp link (wa.link/xxxx)  ← 主渠道，必有
👉 URL link
📞 电话号码
📍 地址（实体服务必有）
↓
[Hashtag 集群]
#品牌名 #产品/服务 #地点 #行业词 ...（8-15 个）
```

### Hashtag 配比（参考）

| 类型 | 占比 | 例子 |
|:--|:--|:--|
| 品牌 / 公司名 | 15% | #客户品牌 |
| 产品 / 服务关键词 | 35% | #中医推拿 #房产投资 #企业融资 |
| 地点 | 20% | #KL中医 #Puchong海鲜 #PJ补习 |
| 行业通用词 | 15% | #PropertyInvestment #小六冲刺 |
| SEO 长尾词 | 10% | #马来文从Fail变B #打工族也能投资 |
| 社群参与词 | 5% | #打卡送礼 #周年庆 |

**数量按行业**：
- 课程 / 教育：8-15 个（最多）
- 房产 / 产品：8-12 个
- 服务（财务 / 装修 / 美容）：8-10 个
- 美食：6-8 个（最少）

---

## 5. 行业长度区间（cross-ref `style-guide.md` 长度规则）

| 行业 | 行数 | 字数 |
|:--|:--|:--|
| 课程 / 研讨会 | 70-85 | 1200-1600 |
| 产品销售 | 75-105 | 1200-1800 |
| 房产投资 | 60-75 | 1000-1500 |
| 房屋装修 | 50-55 | 1000-1200 |
| 财务 / 融资 | 45-70 | 900-1300 |
| 旅游 | 40-60 | 800-1200 |
| 医疗 / 美容 | 30-45 | 600-1000 |
| 美食餐饮 | 25-40 | 400-800 |

按 Client MD 行业 default；user 可启动 override。

---

## 6. Rojak 词汇库（高频，按词性分）

### Noun（英文）— 自然混用 OK
Loan / P.Loan / SME Loan / Project / Rental / Rental Yield / Installment / Monthly Instalment / Course / Webinar / Bonus / Promotion / Consultant / Advisory / Layout / Unit / Income / Passive Income / CCRIS / CTOS / DSR / CTO / Warranty / Guarantee / RM / Boost / Inbox / Customer / Follower / Sales / Order / Deadline / FB / IG / Post / Tool / Team / ROI / CPM / Site Visit / Renovation / Flooring / Whitening / DSD (Digital Smile Design)

### Adj（英文）
Practical / Realistic / Professional / Flexible / Free / Limited / Transparent / Customized / Minimal / Low Cost / Outdated / Fresh

### Bahasa Pasar / Manglish（按行业用）
- 美食 / 餐饮高频：Nah, Geng, Sibeh, Ngam, Jio, Kaki, Confirm
- 美容 / 健康：Confirm, Sibeh, Ngam
- B2B / 财务：Confirm（不要用 Bahasa Pasar 太多）
- 装修 / 服务：Confirm, Ngam, Sibeh

### 中文口语 particle（必有，无行业差异）
罢了 / 酱 / 讲真的 / 根本 / 才是 / 完全 / 铁律 / 你都不知道 / 想都想不到 / 老板们 / 姐妹们 / 你看 / 不要再 / 趁现在 / 别等 / 先到先得

### 语气助词（节制用）
Lah / Lor / Hor / Leh / Eh / Mah（每条文案至多 2-3 个）

---

## 7. SNICK.C 在 6 段骨架里的对应

详见 `snickc-checklist.md` 末段「在 6 段骨架里的对应」section。

简版回顾：
- 段 1 Hook：无固定 SNICK.C 元素（Hook 是引子）
- 段 2 Pain：**Issue (I)** 主要在这
- 段 3 转折+Solution+Knowledge：**Solution (S)** + **Knowledge (K)** 都在这
- 段 4 Proof：**Certified Proof (C)** 主要在这
- 段 5 Scarcity：**.C-1 Scarcity** 在这
- 段 6 CTA：**.C-2 CTA** 在这
- **Numbers (N)** 散落各段（金额 / 人数 / 时间 / 百分比 / 倍数）

每条变体输出前跑 `snickc-checklist.md` self-check 6 元素齐全。
