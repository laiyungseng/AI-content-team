---
type: methodology
name: content_strategy
status: active
phase: 2
read_by: [content_strategist]
---
# content_strategy

**Purpose:** turn intelligence into a strategy: objectives, pillars, and allocation of formats, funnel stages, hooks and experiments. Angles are generated and scored with [[angle_evaluation]].

## Process
1. Confirm an approved intelligence run (`competitor_analysis/projects/[project]/runs/index.md`) and a filled `brand/[project]/`. Stop and report if either is missing.
2. Fill the input brief (template section "Input brief"). Take what the brand files and the run already answer; ask the user only for the rest.
3. Pick objectives and at most three pillars from the brand files and the insights. Record the topic and the pillar for each planned post (see CLAUDE.md conflicts: competitors use topics, we use topics and pillars).
4. Run the angle process in [[angle_evaluation]]: 12 angles, kill filter, scorecard, best three.
5. Allocate the plan with two tags on every planned post: intent (Educate / Engage / Promote, default 50/20/30) and evidence (proven / adjacent / experimental, 70/20/10). They are separate axes; both are kept.
6. Cite evidence: every proven angle names the pattern or insight id and its post count. Experimental angles say what is being tested.
7. Check claims against `shared/platform_rules/meta.md` and `brand/[project]/prohibited_claims.md`.
8. Write `content_creation/projects/[project]/planning/current_strategy.md` from the template and present it through `artifact-presentation-setup` for approval.

## Output schema
`content_creation/templates/content_strategy.md`.

## Good / bad
- Good: "Hesitation: owners fear paid ads burn money with no result. Angle: show the cost of one ignored enquiry. Evidence: INS-0023, 14 posts."
- Bad: "Boost awareness with engaging content across platforms." (generic, no evidence, no hesitation)
