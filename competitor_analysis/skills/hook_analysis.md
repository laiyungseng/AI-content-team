---
type: methodology
name: hook_analysis
status: active
---
# hook_analysis

**Purpose:** Hook taxonomy, scoring framework and how to extract the underlying hook formula. Writing rules and examples live in [[hooks]]; the research method in `competitor-intelligence/references/hook_research.md`.

## Four components
Record each separately: **spoken** (first line said), **text** (on-screen words), **visual** (first frame/motion), **audio** (sound, music, voice tone). Write "not visible from the data" for any that cannot be read.

## Scoring dimensions
Curiosity, specificity, relevance, emotional impact, novelty, urgency, contrarian angle, fear/loss, transformation promise. Score each low / medium / high only where it applies; skip the rest.

## Process
1. Read the four components for the item.
2. Name the **formula** with blanks, not the wording: e.g. "[specific number] + [thing it replaces] + [time saved]".
3. Say why it stops the scroll in one sentence tied to a visible element.
4. Say how to rebuild it for us with different content, without reusing their line.

## Output schema
`{id, spoken, text, visual, audio, scores: {dimension: level}, formula, whyItStopsScroll, howToRebuild}` (list in `analysis/hooks.json`).

## Good / bad examples
- Good formula: "[Common belief] is wrong: [specific counter-fact]" with a cold-open visual of the fact on screen.
- Bad: copying "Nobody tells you this about X" verbatim, or praising a hook with no named element.
