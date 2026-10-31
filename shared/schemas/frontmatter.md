---
type: schema
status: active
---
# Frontmatter schema

Every major file carries YAML frontmatter so the vault works as an Obsidian knowledge graph.

```yaml
---
id: C002                  # C### content, PAT-### pattern, INS-### insight, EXP-### experiment
type: content             # content | brief | pattern | insight | competitor_post | experiment | report
project: project_name
campaign: crm_launch
campaign_stage: problem
platform: instagram
format: carousel          # reel | carousel | static | flyer | ad
status: draft             # idea | planned | brief_ready | draft | review | revision | approved | scheduled | published | measured
publish_date: 2026-11-04
publish_authorized: false # publishing requires status=approved AND publish_authorized=true
previous_content: C001
next_content: C003
source_patterns: [PAT-004]
source_insights: [INS-027]
---
```

Link with `[[PAT-004]]`, `[[INS-027]]`, `[[C001]]`. Tags: #competitor #research #insight #pattern #winning #failed
#experiment #campaign #content #reel #carousel #static #approved #published
