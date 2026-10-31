#!/usr/bin/env python3
"""Create the AI content team workspace: folders, agent stubs, methodology stubs, templates.

Idempotent: never overwrites a file that already exists, so it is safe to re-run after the
folder structure is extended. Run from anywhere:

    python scaffold_workspace.py --root "D:/program/AI content team"

The per-project folders live under a `_template` directory in each domain; use
.claude/skills/business-onboarding/scripts/init_project.py to copy them for a new project.
"""
from __future__ import annotations

import argparse
from pathlib import Path

# --------------------------------------------------------------------------- agents
# name: (title, phase, purpose, inputs, read, write, next_agent, restrictions)
AGENTS = {
    "orchestrator": (
        "Orchestrator", 1,
        "Control the complete workflow and decide which agent executes each task. Does not do deep specialist work itself.",
        "User request; state/[project]/*.md",
        "CLAUDE.md; state/[project]/**; brand/[project]/brand_guideline.md",
        "state/[project]/**",
        "Whichever agent the request routes to",
        "Must not generate content before required intelligence exists. Must not skip workflow stages.",
    ),
    "competitor_researcher": (
        "Competitor Researcher", 1,
        "Collect competitor and internal content: metadata, format, hook, CTA, engagement metrics, publishing info, source reference.",
        "Competitor list, platforms, research period, content quantity, brand/project context",
        "brand/[project]/**; competitor_analysis/templates/content_record.md",
        "competitor_analysis/projects/[project]/raw/**; competitor_analysis/projects/[project]/sources/**",
        "competitor_analyzer",
        "Must not modify brand/**, content_creation/**, memory/**.",
    ),
    "competitor_analyzer": (
        "Competitor Analyzer", 1,
        "Analyze individual content pieces: topic, objective, structure, value proposition, storytelling, emotional trigger, visual pattern, CTA, engagement mechanism, differentiation.",
        "Raw content records",
        "competitor_analysis/projects/[project]/raw/**; brand/[project]/**",
        "competitor_analysis/projects/[project]/analysis/content/**",
        "hook_analyzer",
        "Must not modify raw/**, brand/**, content_creation/**, memory/**.",
    ),
    "hook_analyzer": (
        "Hook Analyzer", 1,
        "Score hook quality and extract the reusable hook formula rather than copying the competitor hook.",
        "Raw content records",
        "competitor_analysis/projects/[project]/raw/**; brand/[project]/**; shared/frameworks/hooks.md",
        "competitor_analysis/projects/[project]/analysis/hooks/**",
        "performance_analyst",
        "Must not modify brand/**, content_creation/**, memory/**.",
    ),
    "performance_analyst": (
        "Performance Analyst", 1,
        "Decide whether content outperformed its own baseline (account median), separating genuinely strong content from reach driven by account size.",
        "Raw content records with metrics; performance/[project]/raw/**",
        "competitor_analysis/projects/[project]/raw/**; performance/[project]/**",
        "competitor_analysis/projects/[project]/analysis/performance/**; performance/[project]/weekly/**; performance/[project]/monthly/**",
        "insight_synthesizer",
        "Must not modify brand/**, content_creation/**, memory/**.",
    ),
    "insight_synthesizer": (
        "Insight Synthesizer", 1,
        "Combine analyses into reusable strategic intelligence: winning and weak patterns, content gaps, hook library, opportunities.",
        "All analysis/** outputs",
        "competitor_analysis/projects/[project]/analysis/**; memory/[project]/**",
        "competitor_analysis/projects/[project]/insights/**; competitor_analysis/projects/[project]/reports/**",
        "content_strategist",
        "Must not modify analysis/**, brand/**, content_creation/**. Memory updates only for validated findings.",
    ),
    "content_strategist": (
        "Content Strategist", 2,
        "Convert intelligence into a content strategy: objectives, pillars, format/funnel/hook/experiment allocation.",
        "Brand positioning, audience, objectives, insights, performance history, requested quantity",
        "brand/[project]/**; competitor_analysis/projects/[project]/insights/**; memory/[project]/**; performance/[project]/performance_summary.md",
        "content_creation/projects/[project]/planning/current_strategy.md",
        "campaign_planner",
        "Must not run without intelligence output. Must not modify brand/**.",
    ),
    "campaign_planner": (
        "Campaign Planner", 2,
        "Build connected content sequences (awareness > problem > cost > solution > proof > offer > CTA). Every item references previous, next, stage and objective.",
        "current_strategy.md",
        "content_creation/projects/[project]/planning/current_strategy.md; brand/[project]/**",
        "content_creation/projects/[project]/planning/campaign_map.md",
        "schedule_planner",
        "Must not break sequences once approved.",
    ),
    "schedule_planner": (
        "Schedule Planner", 2,
        "Decide when and in what sequence content publishes. Prevents repetition, consecutive sales messages, repeated hooks, identical-format runs and broken campaign sequences.",
        "Period, quantity, campaign map, format mix, platform rules",
        "content_creation/projects/[project]/planning/**; shared/platform_rules/**",
        "content_creation/projects/[project]/planning/schedule_publish.md",
        "content brief generation (content_strategist) then creators",
        "Must not change content status beyond Planned.",
    ),
    "reel_creator": (
        "Reel Creator", 3,
        "Produce hook, spoken script, scene structure, B-roll, on-screen text, caption, CTA and editing direction from a content brief.",
        "One content brief",
        "content_creation/projects/[project]/briefs/**; brand/[project]/**; shared/frameworks/**",
        "content_creation/projects/[project]/drafts/**",
        "content_reviewer",
        "Must not approve its own content.",
    ),
    "carousel_creator": (
        "Carousel Creator", 3,
        "Produce slide structure, headlines, supporting copy, CTA, visual recommendations and caption from a content brief.",
        "One content brief",
        "content_creation/projects/[project]/briefs/**; brand/[project]/**; shared/frameworks/**",
        "content_creation/projects/[project]/drafts/**",
        "content_reviewer",
        "Must not approve its own content.",
    ),
    "static_content_creator": (
        "Static Content Creator", 3,
        "Produce image headline, supporting text, design concept, caption and CTA for flyers, quotes, infographics, announcements, promotions and single-image posts.",
        "One content brief",
        "content_creation/projects/[project]/briefs/**; brand/[project]/**; shared/frameworks/**",
        "content_creation/projects/[project]/drafts/**",
        "content_reviewer",
        "Must not approve its own content.",
    ),
    "content_reviewer": (
        "Content Reviewer", 3,
        "Score drafts /100 (hook 20, audience fit 20, value 20, brand 15, originality 10, CTA 10, platform 5). 85-100 approve, 70-84 revise, below 70 regenerate.",
        "A draft and its brief",
        "content_creation/projects/[project]/drafts/**; briefs/**; brand/[project]/**; competitor_analysis/projects/[project]/insights/**",
        "content_creation/projects/[project]/review/**",
        "Approved: publishing_agent. Revise or regenerate: the originating creator.",
        "Must not edit drafts. Must not review content it created.",
    ),
    "publishing_agent": (
        "Publishing Agent", 6,
        "Schedule and publish approved content through a scheduling connector. Only content with status=approved AND publish_authorized=true may be published.",
        "Approved content items",
        "content_creation/projects/[project]/scheduled/**; planning/schedule_publish.md",
        "content_creation/projects/[project]/scheduled/**; content_creation/projects/[project]/published/**; state/[project]/publishing_status.md",
        "performance_analyst (after publish)",
        "Phase 6 only. Must never publish without explicit user authorization recorded in the content frontmatter.",
    ),
}

# ------------------------------------------------------------------ methodology skills
# file -> (purpose, extra_body)
CA_SKILLS = {
    "competitor_research": ("How to collect competitor and internal content reliably (which platforms, how many posts, which fields).", ""),
    "competitor_analysis": ("How to break a single piece of content into topic, structure, value, emotion, CTA and differentiation.", ""),
    "hook_analysis": (
        "Hook taxonomy, scoring framework and how to extract the underlying hook formula.",
        "## Scoring dimensions\nCuriosity, specificity, relevance, emotional impact, novelty, urgency, contrarian angle, fear/loss, transformation promise.\n",
    ),
    "content_scoring": ("How to score content pieces consistently so patterns can be compared.", ""),
    "performance_analysis": (
        "How to decide whether content beat its baseline rather than just having big reach.",
        "## Metrics\nViews, likes, comments, shares, saves, followers, engagement rate, view-to-follower ratio, comment-to-view ratio, performance relative to account median.\n",
    ),
    "pattern_detection": ("How to turn repeated observations into a pattern with an evidence count and confidence.", ""),
    "report_generation": ("How to assemble the intelligence report (winning/weak patterns, hook library, gaps, opportunities).", ""),
}
CC_SKILLS = {
    "generate_insight": "How to convert intelligence into an actionable insight for planning.",
    "content_strategy": "Content strategy framework: objectives, pillars, format/funnel/hook/experiment allocation (70/20/10 rule).",
    "campaign_planning": "Campaign sequencing framework for connected content.",
    "schedule_planning": "Scheduling rules: spacing, format variety, no consecutive sales posts, sequence integrity.",
    "content_brief_generation": "How to write one brief per content item from strategy, campaign and schedule.",
    "carousel_generation": "Carousel structure and copy framework.",
    "reel_generation": "Reel structure: 0-3s hook, 3-10s problem, 10-30s value, 30-45s proof, 45-60s CTA.",
    "static_post_generation": "Static post / flyer / quote / infographic framework.",
    "CTA_generation": "CTA framework matched to funnel stage and platform.",
    "content_review": "Review rubric and decision thresholds (85+ approve, 70-84 revise, <70 regenerate).",
}

CA_TEMPLATES = {
    "competitor_profile": "Competitor account profile: handle, platform, followers, niche, posting cadence, baseline (median) metrics.",
    "content_record": "One raw content record: id, source URL, platform, format, hook, CTA, metrics, publish date.",
    "hook_analysis": "One hook analysis: hook text, scores per dimension, extracted formula.",
    "insight": "One insight: id, observation(s), evidence count, confidence, implication.",
    "analysis_report": "Intelligence report skeleton.",
}
CC_TEMPLATES = {
    "content_strategy": "Strategy document skeleton.",
    "campaign_plan": "Campaign plan skeleton.",
    "content_brief": "One brief per content item.",
    "carousel": "Carousel draft skeleton.",
    "reel": "Reel draft skeleton.",
    "static_post": "Static post draft skeleton.",
    "publish_schedule": "Operational dashboard table.",
}

TEMPLATE_BODIES = {
    ("content_creation", "content_brief"): """---
id: C000
type: brief
project: {{project}}
format: reel            # reel | carousel | static | flyer | ad
objective: awareness
campaign:
campaign_stage:
platform:
status: brief_ready
previous_content:
next_content:
source_patterns: []     # e.g. [[PAT-0041]]
source_insights: []     # e.g. [[INS-0023]]
publish_authorized: false
---

## Audience

## Problem

## Hook pattern

## Core message

## CTA
""",
    ("content_creation", "publish_schedule"): """---
type: schedule
project: {{project}}
---

| ID | Date | Platform | Format | Campaign | Stage | Status | Previous | Next |
|---|---|---|---|---|---|---|---|---|

Status lifecycle: Idea > Planned > Brief Ready > Draft > Review > Revision > Approved > Scheduled > Published > Measured
""",
}

SHARED = {
    "frameworks/hooks.md": "Hook formulas and taxonomy (shared by hook_analyzer and creators).",
    "frameworks/cta.md": "CTA patterns by funnel stage.",
    "frameworks/storytelling.md": "Storytelling structures for short-form video and carousels.",
    "frameworks/experimentation.md": "70% proven / 20% adjacent / 10% experimental allocation and how to record results.",
    "platform_rules/instagram.md": "Instagram format specs, limits, best practices.",
    "platform_rules/tiktok.md": "TikTok format specs, limits, best practices.",
    "platform_rules/linkedin.md": "LinkedIn format specs, limits, best practices.",
    "schemas/frontmatter.md": None,  # filled below
}

FRONTMATTER_SCHEMA = """---
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
"""

MEMORY_FILES = {
    "learnings.md": "Validated lessons learned (only findings with evidence).",
    "winning_patterns.md": "Patterns validated as winning. One block per pattern (PAT-###).",
    "failed_patterns.md": "Patterns validated as failing.",
    "experiments.md": "Experiment log: hypothesis, allocation, result.",
    "audience_learnings.md": "Audience behaviour learnings.",
    "platform_learnings.md": "Platform-specific learnings.",
    "decisions.md": "Strategic decisions and the reason for each.",
}
STATE_FILES = ["current_cycle.md", "research_status.md", "generation_status.md", "publishing_status.md"]
BRAND_FILES = {
    "brand_guideline.md": "Master brand guideline (summary of everything below).",
    "brand_voice.md": "Voice, tone, vocabulary, do/don't phrases.",
    "audience.md": "Target audience segments, pains, desires, objections.",
    "positioning.md": "Positioning statement, differentiation, competitors.",
    "products_services.md": "Products and services.",
    "offers.md": "Current offers, pricing logic, CTAs.",
    "prohibited_claims.md": "Claims, words and topics that must never appear.",
}

AGENT_TMPL = """---
name: {name}
description: {purpose}
status: stub
phase: {phase}
---
# {title}

> Status: stub (roadmap phase {phase}). Fill in the sections below before relying on this agent.

## Purpose
{purpose}

## Inputs
{inputs}

## Required reading
{read}

## Allowed output folders
{write}

## Process
_TODO: step-by-step process._

## Expected output format
_TODO: reference the matching template in `*/templates/`._

## Quality requirements
_TODO._

## Restrictions
{restrictions}

## When to stop
_TODO: define the stop condition and what to report._

## Which agent runs next
{next_agent}
"""

SKILL_DOC_TMPL = """---
type: methodology
name: {name}
status: stub
---
# {name}

**Purpose:** {purpose}

{extra}## Process
_TODO_

## Output schema
_TODO_

## Good / bad examples
_TODO_
"""

TEMPLATE_TMPL = """---
type: template
name: {name}
status: stub
---
# Template: {name}

{purpose}

_TODO: define fields._
"""


def write(path: Path, text: str, created: list[Path]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    created.append(path)


def keep(path: Path, created: list[Path]) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gk = path / ".gitkeep"
    if not gk.exists() and not any(p for p in path.iterdir() if p.name != ".gitkeep"):
        gk.write_text("", encoding="utf-8")
        created.append(gk)


def stub_md(path: Path, title: str, purpose: str, created: list[Path]) -> None:
    write(path, f"---\ntype: stub\nstatus: stub\n---\n# {title}\n\n{purpose}\n", created)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Workspace root folder")
    root = Path(ap.parse_args().root)
    created: list[Path] = []

    # agents
    for key, (title, phase, purpose, inputs, read, wr, nxt, restr) in AGENTS.items():
        write(root / "agents" / f"{key}.md",
              AGENT_TMPL.format(name=key, title=title, phase=phase, purpose=purpose, inputs=inputs,
                                read=read, write=wr, next_agent=nxt, restrictions=restr), created)

    # methodology skills + templates
    for domain, skills, templates in (("competitor_analysis", CA_SKILLS, CA_TEMPLATES),
                                      ("content_creation", CC_SKILLS, CC_TEMPLATES)):
        for name, val in skills.items():
            purpose, extra = val if isinstance(val, tuple) else (val, "")
            write(root / domain / "skills" / f"{name}.md",
                  SKILL_DOC_TMPL.format(name=name, purpose=purpose, extra=extra), created)
        for name, purpose in templates.items():
            body = TEMPLATE_BODIES.get((domain, name)) or TEMPLATE_TMPL.format(name=name, purpose=purpose)
            write(root / domain / "templates" / f"{name}.md", body, created)

    # shared
    for rel, purpose in SHARED.items():
        body = FRONTMATTER_SCHEMA if rel == "schemas/frontmatter.md" else \
            f"---\ntype: stub\nstatus: stub\n---\n# {Path(rel).stem}\n\n{purpose}\n"
        write(root / "shared" / rel, body, created)

    # per-project templates (copied by init_project.py)
    for fname, purpose in BRAND_FILES.items():
        stub_md(root / "brand" / "_template" / fname, fname[:-3].replace("_", " ").title(), purpose, created)
    for d in ("assets/reference_images",):
        keep(root / "brand" / "_template" / d, created)
    stub_md(root / "brand" / "_template" / "assets" / "colors.md", "Colors", "Brand colors (hex, role).", created)
    stub_md(root / "brand" / "_template" / "assets" / "fonts.md", "Fonts", "Brand fonts (heading, body).", created)

    for d in ("sources", "raw", "analysis/content", "analysis/hooks", "analysis/performance", "insights", "reports"):
        keep(root / "competitor_analysis" / "projects" / "_template" / d, created)
    for d in ("planning", "briefs", "drafts", "review", "scheduled", "published"):
        keep(root / "content_creation" / "projects" / "_template" / d, created)
    for fname, purpose in MEMORY_FILES.items():
        stub_md(root / "memory" / "_template" / fname, fname[:-3].replace("_", " ").title(), purpose, created)
    for d in ("raw", "weekly", "monthly"):
        keep(root / "performance" / "_template" / d, created)
    stub_md(root / "performance" / "_template" / "performance_summary.md", "Performance summary",
            "Rolling summary of published-content performance vs baseline.", created)
    for fname in STATE_FILES:
        stub_md(root / "state" / "_template" / fname, fname[:-3].replace("_", " ").title(),
                "Operational state for this project.", created)

    print(f"Created {len(created)} items under {root}")
    for p in created[:5]:
        print("  ", p.relative_to(root))
    if len(created) > 5:
        print("   ...")


if __name__ == "__main__":
    main()
