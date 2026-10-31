---
type: methodology
name: pattern_detection
status: active
---
# pattern_detection

**Purpose:** Turn repeated observations into a pattern with an evidence count and confidence. A pattern is a candidate for memory only after approval ([[experimentation]]).

## Process
1. **Observe**: list verdicts and hook formulas for Copy/Adapt items (hits) and for Ignore items that fell below usual (misses).
2. **Group** by one shared feature at a time: hook formula, format, length, topic, offer, CTA type, visual style. One feature per pattern.
3. **Count**: how many hits and how many misses share the feature, across how many accounts. A pattern needs 3 or more hits from 2 or more accounts, or an ad running 30+ days in 3 or more variants.
4. **Check the other side**: how often does the feature appear in misses? If similar, it is not a pattern.
5. **Confidence**: one rule, defined in `.claude/skills/competitor-intelligence/references/verdict_rules.md`: low under 5 posts, medium 5 to 14, high 15+ and a second run or our own posts that confirm it. One run caps the result at medium.
6. **Compare with memory**: confirmed, weakened or contradicted.
7. Write candidates as blocks in the formats of `memory/_template/winning_patterns.md` / `failed_patterns.md` in `insights/<run>_proposed_lessons.md`. Anything below the evidence bar goes to `experiments.md` as a hypothesis.

## Output schema
Memory block fields: pattern, evidence (counts, runs), our validation, result, confidence, source, do next.

## Good / bad examples
- Good: "Cold-open number hook: 5 hits (4 accounts), 1 miss; confidence medium; our validation: none yet."
- Bad: "Everyone is doing carousels, so carousels work." (no hit/miss comparison).
