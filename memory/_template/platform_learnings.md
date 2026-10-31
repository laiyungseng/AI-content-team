---
type: memory
status: active
kind: platform_learnings
---
# Platform Learnings

> Memory holds **validated** findings only. Raw observations stay in `competitor_analysis/projects/[project]/runs/`.
> A block needs evidence (post count), a result and a confidence level. Weak or single-run findings stay in `experiments.md`.
> Never keep one giant file: add blocks here, split by platform if a file passes ~300 lines.

Brand-specific platform findings (what works for this brand on each platform). Generic platform specs live in `shared/platform_rules/`.

## Block format
```markdown
## <platform>
### PLT-001 <finding>
- evidence / result:
- confidence: low           # low (<5 posts) | medium (5 to 14 posts; one run caps at medium) | high (15+ posts and a 2nd run or our own validation)
- source: [[run-...]]   date: YYYY-MM-DD
```

## Platforms
(none yet)
