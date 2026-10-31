---
source: social-media-automation 0.2.0 / content-strategist/references/output-templates.md (Phase 2)
copied: 2026-10-31
---
# Output Templates

> **This project (Social Media Automation):** the two documents below are consolidated into ONE file, `04-strategy/strategy.md`: Document 1 becomes the Strategy half, Document 2 the Content pillars half. Write there rather than creating separate content-strategy.md / content-pillars.md files. Do not number the halves or sections; other files refer to them by heading name.

The two final deliverables. These outlines are a menu, not a template: include a section only when the interview produced real content for it, and leave out the rest, headings included. Leave no placeholders. Always keep the pillars and the tagging rule. If the user has their own structure, map these sections onto their headings and preserve anything extra they ask for.

Write both documents in Markdown with frontmatter, so they slot into knowledge bases and AI-readable folders.

---

## Document 1: content-strategy.md

```markdown
---
status: complete
last-updated: YYYY-MM-DD
owner: [name]
review-cadence: quarterly
---

# Content Strategy: [Brand]

> The why behind everything posted. Review quarterly.

## Business context

[3 to 5 sentences: what the brand sells, who buys, the 12-month business goal.
This is the paragraph a new team member or AI reads first.]

## Social media objectives

[1 to 3 objectives, each: verb + metric + target + deadline.]
[For each: which business goal it descends from.]

## Audience summary

[One short block per persona: who, core pain, what they want from content.
Link to fuller persona docs if they exist.]

## Intent mix

| Intent | Target share | What counts |
|---|---|---|
| Educate | X% | [one line] |
| Engage | Y% | [one line] |
| Promote | Z% | [one line] |

[One sentence on why this ratio fits this business.]
[Launch-mode ratio, if defined, and what triggers it.]

## Funnel mapping

- Top of funnel (attract strangers): [content types + which pillars]
- Middle (build trust): [content types + which pillars]
- Bottom (convert): [content types + which pillars]
- Target ratio across the three levels: [X/Y/Z]

## Products vs services split

[Only if the brand sells both. Effort split and seasonal shifts.]

## Platform roles

[One line per platform: its single job. Cut or park platforms with no job.]

## Key metrics

- [Metric → objective it measures → how and when it's checked]
- Vanity metrics we explicitly ignore: [list + one line why]

## Production capacity

[Posts per week, formats, who produces. The constraint every plan must respect.]

## Quarterly focus

### Q[X] [year]
- Theme: [one line]
- Priority objective: [which one]
- Key campaigns: [links if any]

## Risks and assumptions

[Anything decided on a guess, with a revisit date.
Any strategist recommendation the user overrode, recorded without blame.]

## Change log

- YYYY-MM-DD: created via strategist interview.
```

---

## Document 2: content-pillars.md

```markdown
---
status: complete
last-updated: YYYY-MM-DD
owner: [name]
---

# Content Pillars: [Brand]

> Every post must belong to exactly one pillar. 3 to 5 pillars total.

## Pillar overview

| # | Pillar | Intent | Share | Funnel stage | Success metric |
|---|---|---|---|---|---|
| 1 | [name] | Educate/Engage/Promote | X% | TOFU/MOFU/BOFU | [metric] |

[Sanity line: shares sum to 100% and match the intent mix in content-strategy.md.]

## Pillar 1: [Name]

### Purpose
[One sentence: what this pillar achieves for the brand.]

### Description
[2 to 3 sentences.]

### Topics inside this pillar
[5 to 10 recurring topics, in the audience's language.]

### Formats that fit
[Best formats per platform, within stated capacity.]

### Personas served
[Names from the audience summary.]

### Example post ideas
[3 to 5 ideas concrete enough to produce tomorrow.]

### Success metric
[The one number that shows this pillar is working, matched to its intent.]

---

[Repeat for each pillar.]

## Sample two weeks

[A simple week-by-week list showing the pillars in rotation at real capacity.
This is the stress-test output from Phase 7; it proves the strategy is executable.]

## Tagging rule

Tag every content file/post with its pillar name exactly as written here.
```

---

## Delivery notes

- Present both documents in one message, strategy first.
- After presenting, ask for edits and revise until sign-off. Expect at least one round.
- If the user maintains the documents in a specific folder or tool, offer the content formatted for that destination.
- Close by suggesting a 90-day review: pillars are hypotheses, and the first quarter of performance data is what turns them into knowledge.
