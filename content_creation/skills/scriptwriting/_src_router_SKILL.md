---
source: social-media-automation 0.2.0 / social-media-scriptwriting/SKILL.md (adapt into agents/reel_creator.md routing, Phase 3)
copied: 2026-10-31
---
---
name: social-media-scriptwriting
description: Router skill for writing and improving short-form social media video scripts, hooks, story structures and CTAs. Use whenever the user wants to write a video script, write or fix a hook, pick a content format, structure the body of a script, write a call to action, improve retention or watch time, understand why a video flopped or got views but no leads, learn storytelling for short-form, research what hooks work in their niche, model a competitor's transcript, or asks for feedback on an existing script. Triggers include "write me a script", "help me with my hook", "why did this video flop", "make this more engaging", "how do I open this video", "review my script", "what hook should I use", "what format should this be", "what CTA should I use", "TikTok/Reels/Shorts script", "improve retention". Always route through this skill rather than answering from general knowledge.
---

# Social Media Scriptwriting

Helps write short-form video scripts and hooks that hold attention and convert. This skill is a router: identify which job the request is, load the file for that job, work from it.

## Routing

Files are organised by job, not by topic. Each job file is self-contained, so one load should answer the request.

| The job | Load |
|---|---|
| Write a full script, end to end | `references/writing-a-script.md`, plus the matching row of `references/formats.md` and `references/ctas.md` |
| Write or rewrite a hook, fix an opening | `references/writing-a-hook.md` |
| Diagnose something that already exists: a flop, a script review, views without leads | `references/diagnosing.md`, then only the file it points to |
| Improve retention or watch time, fix a boring middle, tighten pacing | `references/diagnosing.md` to locate the drop-off, then the file that row names |
| Pick a format, or work out the shape of the body | `references/formats.md` |
| Write or fix a call to action | `references/ctas.md` |
| Model or rewrite someone else's transcript | `references/writing-a-script.md` section 7 |
| Find hooks proven in the user's own niche | `references/hook-research.md` |
| Shoot or edit a script that is already written | `references/production-notes.md` |
| Understand or teach why any of this works | `references/psychology.md` |

**Lookup files**, read for the relevant part rather than start to finish: `formats.md`, `ctas.md`, `hook-examples.md`.

**Depth files**, loaded only when the job file is not enough: `psychology.md` for why a rule exists, `hook-examples.md` for real wins and flops with links, `production-notes.md` for execution.

**Two files is normally the ceiling.** Loading a job file plus one lookup file covers almost every request. If it feels like four files are needed, the job has probably been misidentified, so re-read the request instead of loading more.

**When the job is unclear**, the split that matters is whether something already exists. If the user has brought a script, a transcript or a video, the job is diagnosis, so start with `references/diagnosing.md`. If they have brought a topic and nothing else, the job is writing, so start with `references/writing-a-script.md`. When it is still ambiguous, ask rather than loading both.

## How to work

1. **Get the inputs before writing.** The topic, who it is for (the specific viewer, not "everyone"), the pain point or interest being served, and what the user believes that most people in that audience do not. That last one is the whole engine.
2. **Find the contrarian take before writing a single line.** Most of the effort belongs here, not in polishing wording. If there is no real contrast, say so plainly and help find one rather than writing a competent script on a dull premise.
3. **Pick the format.** The format decides the shape of the body. Never write a body freehand when a proven structure exists.
4. **Load the job file.** Do not paraphrase these principles from memory. The reference files exist because the specifics matter more than the gist.
5. **Write to the structure in the reference**, not to a generic template.
6. **Self-check against the checklist** in the job file before presenting anything.
7. **Offer variants.** For hooks, give 3 to 4 options with different angles rather than one polished line. Hooks are tested, not chosen.

## Rules that apply to everything

These are the constraints that hold across every job. The reasoning behind them is in `references/psychology.md`.

- Hooks are the first 2 to 6 seconds and deserve 30 to 40% of total effort on the video.
- A hook is four components working together: text, visual, spoken, audio. Never write only the spoken line.
- Every script needs at least one moment of contrast: what they believe vs what is actually true. Plus smaller contrast words ("but actually", "the truth is") re-hooking through the body.
- Give context and stakes before tactics. The brain consumes top down, and tactics without a container feel like noise.
- Write at a 6th-grade reading level. Short sentences. Active voice. Varied sentence length so the right edge of the script looks jagged, not straight.
- Use "you/your" over "me/my/I" unless the personal framing is the point and is highly relatable. Write to one viewer, not a crowd.
- Signal proof early, as a casual aside, never a boast.
- Every script ends with a CTA, preferably a lead CTA. Place it where the story flow allows, not wherever is convenient.
- Treat every sentence as if it costs $100. If the viewer would not pay for it, cut it.

## Presenting examples

When showing an example from the reference files, always include its link so the user can watch the original. Never present an example without its URL.
