# Data schemas

All templates accept `title`, `subtitle`, `project`. Missing optional fields are skipped. Copy a file from `assets/sample_data/` as a starting point.

## approval-board  (required: `items`)
```json
{"instructions": "optional intro",
 "items": [{"id": "C001", "title": "", "type": "Reel brief", "status": "Brief Ready",
            "meta": {"Platform": "Instagram", "Publish": "2026-11-02"},
            "summary": "short", "sections": [{"label": "Hook", "body": "text"}]}]}
```

## content-preview  (required: `items`)
Common: `id, format (reel|carousel|static), platform, title, status, date, campaign_stage, hook, caption, cta, rationale, review{score,notes}`.
- reel: `reel.scenes[{time, seconds, label, onscreen, visual, voiceover}]` (`seconds` sets the timeline width)
- carousel: `carousel.slides[{headline, body}]`
- static: `static{headline, support, concept}`

## intelligence-report  (required: `summary` = list of finding strings)
`period`, `chart{title, unit, baseline_label, series[{label, value, baseline}]}`,
`patterns{winning[], weak[]}` with `{id, pattern, evidence, confidence (High|Medium|Low), lift, detail}`,
`hooks[{id, formula, example, score 0-100, source}]`, `gaps[{title, detail, opportunity}]`,
`recommendations[{title, detail, priority (High|Medium|Low)}]`.

## publishing-calendar  (required: `items`)
`items[{id, date YYYY-MM-DD, platform, format, campaign, stage, status, title, previous, next}]`. Mirrors the table in `schedule_publish.md`.

## brand-guideline  (required: `brand`)
`brand{name, tagline, summary}`, `positioning{statement, differentiators[]}`, `audience[{name, description, pains[], desires[]}]`,
`voice{traits[], do[], dont[], sample_lines[]}`, `products[{name, description, price}]`, `offers[{name, description, cta}]`,
`palette[{name, hex, role}]`, `fonts[{role, name, sample}]`, `prohibited[]`. Sections with no data are not shown.

## Status words
Badge colour follows the status: approved/published = green, scheduled/measured = blue, review/revision/draft = amber, rejected = red, anything else = neutral.
