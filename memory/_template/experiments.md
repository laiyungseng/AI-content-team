---
type: memory
status: active
kind: experiments
---
# Experiments
Log of tests and unproven findings. A result moves to `winning_patterns.md` / `failed_patterns.md` only when it meets the evidence rule in [[experimentation]].

## Block format
```markdown
### EXP-001 <name>
- hypothesis: If we change X, then Y improves, because Z.
- bucket: proven | adjacent | experimental
- variable / baseline metric:
- posts: <ids, count>
- status: planned | running | measured | promoted | dropped
- result:
- confidence: low | medium | high
- promoted to: PAT-### | FAIL-### | none
```

## Log
(none yet)
