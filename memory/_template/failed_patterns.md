---
type: memory
status: active
kind: failed_patterns
---
# Failed Patterns

> Memory holds **validated** findings only. Raw observations stay in `competitor_analysis/projects/[project]/runs/`.
> A block needs evidence (post count), a result and a confidence level. Weak or single-run findings stay in `experiments.md`.
> Never keep one giant file: add blocks here, split by platform if a file passes ~300 lines.

## Block format
```markdown
### FAIL-001 <short name>
- platform:
- pattern: <what we or competitors tried that underperformed>
- evidence: <N posts; ratio to own typical; runs>
- why it likely failed: <hypothesis, marked as hypothesis>
- confidence: low           # low (<5 posts or 1 run) | medium (5-15 posts or 2 runs) | high (15+ posts, our own validation)
- source: [[run-...]]
- do next: avoid | retest with change <x>
```

## Patterns
(none yet)
