---
type: memory
status: active
kind: skill_feedback_format
---
# skill_feedback format
Copy to `skill_feedback/<skill>.md` (e.g. `competitor-intelligence.md`) on first use. One block per event; append only.

```markdown
### FB-001 YYYY-MM-DD  run: <project>/<run id>
- type: tool_failure | missing_field | platform_change | user_override | method_gap | other
- where: <platform, actor, reference file or step>
- what happened: <facts>
- user override: <e.g. verdict Ignore -> Adapt on item X, reason> (if any)
- proposed edit: <file + change> or "none"
- status: open | proposed | applied | rejected
- repeats: <count of similar events so far>
```
