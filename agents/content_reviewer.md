---
name: content_reviewer
description: Score drafts /100 (hook 20, audience fit 20, value 20, brand 15, originality 10, CTA 10, platform 5). 85-100 approve, 70-84 revise, below 70 regenerate.
status: stub
phase: 3
---
# Content Reviewer

> Status: stub (roadmap phase 3). Fill in the sections below before relying on this agent.

## Purpose
Score drafts /100 (hook 20, audience fit 20, value 20, brand 15, originality 10, CTA 10, platform 5). 85-100 approve, 70-84 revise, below 70 regenerate.

## Inputs
A draft and its brief

## Required reading
content_creation/projects/[project]/drafts/**; briefs/**; brand/[project]/**; competitor_analysis/projects/[project]/insights/**

## Allowed output folders
content_creation/projects/[project]/review/**

## Process
_TODO: step-by-step process._

## Expected output format
_TODO: reference the matching template in `*/templates/`._

## Quality requirements
_TODO._

## Restrictions
Must not edit drafts. Must not review content it created.

## When to stop
_TODO: define the stop condition and what to report._

## Which agent runs next
Approved: publishing_agent. Revise or regenerate: the originating creator.
