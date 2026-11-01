---
type: methodology
name: angle_evaluation
status: active
phase: 2
adapted_from: UPT ad-angle (brutal evaluation, weak idea kill filter, generic output detector)
read_by: [content_strategist, content_reviewer]
---
# Angle evaluation

**Purpose:** decide which content or ad angles are worth producing. Generate many, kill the weak ones, score the survivors strictly, keep three that are genuinely different and can be produced this week. Used by `content_strategist` before a strategy is shown, and by `content_reviewer` when a draft's angle is in doubt.

This scores the **angle** (/50). `content_reviewer` scores the finished **draft** (/100); the two are separate. Where this file's caps apply to a draft, they cap the reviewer's matching category (see "In review").

Inputs: the approved intelligence run, `brand/[project]/` (audience, positioning, offers, `prohibited_claims.md`), the input brief ([[content_strategy]] template), and `shared/platform_rules/meta.md` for risky categories. If an input is missing, state the assumption and label it; ask only when the brief cannot be understood.

## Process
1. **State assumptions.**
2. **Diagnose the business:** what is sold, who buys, what they believe, what worries them, why they delay or refuse, who we want to attract and who we want to filter out.
3. **Market pressure:** price war, cheap competitors, low-quality leads, fatigue, trust, commoditisation, platform change. Say how each changes the message. Competitor evidence comes from the intelligence run (cite item ids), never from memory.
4. **Pain map:** surface, hidden, financial, time, trust, status, operational, market pressure.
5. **Buyer hesitation map:** what the buyer says, what they actually mean, why it blocks the purchase, how the content handles it.
6. **Keyword clusters** by pain, hesitation, result, comparison, urgency, proof, local context, wrong-fit and high-intent buyers. Use real customer language when it exists (enquiries, comments, objections, call notes).
7. **Generate 12 meaningfully different angles.** Use varied types: contrarian, pain-agitation, before/after, mistake, hidden cost, market shift, comparison, proof or case, founder or expert, checklist, myth-busting, urgency. Each has: name, core insight, customer pain, hesitation addressed, main hook, message direction, why it can work, why it might fail, suggested visual, best format, risk level.
8. **Weak idea kill filter** on every angle: Keep, Rewrite or Kill (below).
9. **Rewrite** salvageable ideas: sharper specificity, buyer insight, contrast, sales logic, visual clarity, local language.
10. **Hooks:** three for each of the top five angles (direct pain, contrarian, curiosity). Build them with `shared/frameworks/hooks.md`; name the hook type.
11. **Score** every surviving angle with the scorecard.
12. **Select the best 3.** They must differ strategically, not be three wordings of one idea.
13. **Creative direction** for each: format, visual scene, who appears, what is shown, on-screen text, tone, what to avoid, ratio, platform.
14. **Compliance notes** (below), then **next test recommendation**.

Output structure: [[content_strategy]] template, "Angle evaluation" section.

## Weak idea kill filter
Kill or rewrite an angle that is: too generic; too soft; too corporate; missing the buyer hesitation; missing market insight; no strong pain; no contrast; no reason to stop scrolling; no visual direction; not connected to the offer; attracting the wrong audience; something any competitor could say; a vague hook; a compliance risk. Every angle gets exactly one verdict. Never keep a weak idea to fill the list.

## Scorecard (50 points)
Score each category 1 to 5. Be strict; a nice-sounding idea is not a high score.

| Category | Question |
|---|---|
| Pain depth | A real pain, or a surface problem? |
| Market specificity | Specific to this industry and market? |
| Buyer hesitation | Does it address why the buyer does not buy? |
| Contrast | Is there a strong reframing moment? |
| Offer fit | Does it connect naturally to what is sold? |
| Sales potential | Does it attract leads with buying intent? |
| Wrong-fit filtering | Does it keep out cheap or wrong-fit buyers? |
| Creative potential | Can it become a strong video, image or carousel? |
| Language sharpness | Human, local, not AI-sounding? |
| Compliance safety | Is every claim safe and not misleading? |

| Total | Rating |
|---|---|
| 45-50 | Strong test candidate |
| 40-44 | Good, can test |
| 34-39 | Usable, needs sharpening |
| 28-33 | Average, not a priority |
| under 28 | Kill |

**Caps (automatic penalties):** generic idea max 32 · no buyer hesitation max 35 · no creative direction max 36 · corporate language max 32 · risky claim max 30 · attracts wrong customers max 36 · cannot be tested this week max 34.

## Generic output detector
Rewrite when a line could be in any agency deck. Banned filler (examples): "boost brand awareness", "reach the target audience precisely", "full-funnel marketing strategy", "empower business growth", "one-stop solution", "digital transformation journey", "build brand influence", "take your business to the next level". Prefer sharp, specific sentences such as "You don't lack leads, you attract buyers who only compare prices." The banned list is per language: when the brand writes in another language, translate the idea and add that market's equivalent filler to `brand/[project]/brand_voice.md`.

Final self-check before delivery; fail any, rewrite:
1. Could this apply to any industry?
2. Does it mention buyer hesitation and market pressure?
3. Is there contrast?
4. Do the hooks sound like slogans?
5. Are the angles just rewordings of one idea?
6. Is there sales logic and a visual execution idea?
7. Is there a reason each angle can work, and a risk warning?
8. Does it read like an agency proposal, or like translated text?
9. Is it too safe to stop a scroll?

## Review checks (for `content_reviewer`)
- Pain and market specific; hesitation named; wrong-fit and best-fit customer identified.
- Angles different from each other, each with contrast, offer connection and visual direction.
- At least three ideas can be produced this week.
- Language fits the brand's market and avoids filler and translated phrasing.
- Scoring strict; weak ideas killed or rewritten; top three clearly stronger than the rest.
- Risky claims flagged (regulated finance: no guaranteed approval; courses: no unrealistic outcomes). Claim rules: `shared/platform_rules/meta.md`, `brand/[project]/prohibited_claims.md`.

**In review:** a generic angle caps originality; a risky claim caps brand/compliance; a missing hesitation caps audience fit. Never above the cap, whatever the draft's other scores.

**Pass condition:** the output is acceptable only if at least three concepts can realistically become content this week.

## Tests
Three de-branded cases and their acceptance checks: `content_creation/tests/angle_eval_cases/`.
