---
type: memory
status: active
kind: system
---
# System memory
How the **skills and tools** perform across all projects (not brand lessons). Feeds the retrospective step at the end of every run.

- `skill_feedback/<skill>.md` - problems and user overrides per skill (format below).
- `changelog.md` - skill edits the user approved.

## Retrospective rule
1. After each run, append problems and overrides to `skill_feedback/<skill>.md`.
2. Every 3 runs (or on request): read the log, propose concrete edits to the reference files (e.g. `verdict_rules.md`).
3. Apply an edit only after the user approves it in chat; then add a line to `changelog.md`.
User overrides of Adapt / Copy / Ignore are the main signal for recalibrating `verdict_rules.md`.
