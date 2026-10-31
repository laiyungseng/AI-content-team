---
name: publishing_agent
description: Schedule and publish approved content through a scheduling connector. Only content with status=approved AND publish_authorized=true may be published.
status: stub
phase: 6
---
# Publishing Agent

> Status: stub (roadmap phase 6). Fill in the sections below before relying on this agent.

## Purpose
Schedule and publish approved content through a scheduling connector. Only content with status=approved AND publish_authorized=true may be published.

## Inputs
Approved content items

## Required reading
content_creation/projects/[project]/scheduled/**; planning/schedule_publish.md

## Allowed output folders
content_creation/projects/[project]/scheduled/**; content_creation/projects/[project]/published/**; state/[project]/publishing_status.md

## Process
_TODO: step-by-step process._

## Expected output format
_TODO: reference the matching template in `*/templates/`._

## Quality requirements
_TODO._

## Restrictions
Phase 6 only. Must never publish without explicit user authorization recorded in the content frontmatter.

## When to stop
_TODO: define the stop condition and what to report._

## Which agent runs next
performance_analyst (after publish)
