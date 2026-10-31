---
name: business-onboarding
description: Learn the user's business and turn it into a brand guideline for the AI content team - studies examples (website, social accounts, best posts, competitors, logo), interviews the user one question at a time, then writes brand/[project]/ files and presents them for approval. Use this at the very start of any project and whenever the user says "set up my business", "learn about my brand", "create a brand guideline", "onboard a new client/brand", "define my voice/audience/positioning", or when a brand folder is missing, empty or still a stub, even if they only say "let's get started".
---

# Business onboarding

The content team is only as good as its understanding of the business. This skill gathers evidence first, then interviews the user, then writes the brand guideline that every other agent reads. The interview is one question at a time because owners answer a single focused question well and a list of ten badly.

## Steps

### 0. Environment and project
- Run the `installation-setup` check (`setup.py check`). If a required tool is missing, hand over to that skill and come back. Do not start the interview with a broken setup.
- Ask for the project name (short, lowercase, underscores, e.g. `penang_cakes`) and create the folders:
  `uv run python .claude/skills/business-onboarding/scripts/init_project.py <project>`
  This copies the `_template` folders into brand, competitor_analysis, content_creation, memory, performance and state, so the same name is used everywhere.
- Create `state/<project>/onboarding_progress.md` from `assets/progress_template.md`. Update it after every answer so the interview can resume in a later session.

### 1. Study examples first
Ask what the user can share, following `references/study_checklist.md`: website, social accounts, best and worst posts, logo and colours, product or price sheets, testimonials, past ads, 3-5 competitors, brands they admire. Ask for these in one short message, since it is a single "what do you have" question, and accept "none" for any item.
Then study what they gave you: read pages with the built-in browser or web fetch, and pull public posts with Apify if connected (confirm the connector first). Write what you learned into the progress file as "Known" so you never ask for it again. Show the user a 4-5 line summary of what you understood and ask whether it is right.

### 2. Interview, one question at a time
Use `references/interview_questions.md`. Rules that keep it comfortable:
- One question per message. Wait for the answer.
- Skip anything already known from the examples or earlier answers. If you are unsure, state your guess and ask the user to confirm instead of asking cold.
- When the answer is probably a choice (tone, goal, platform), offer 3-4 options plus "something else".
- Acknowledge in a few words, reflect back unclear answers in plain language, and never lecture on marketing theory.
- If an answer is vague ("good quality"), ask for a concrete example once, then move on.
- After roughly 8 answers, show a short draft of what you have so far, so the user can correct the direction early.
- Stop when every guideline section has enough real content to be useful; do not ask all questions for the sake of it. "I don't know yet" is a valid answer: record it as an open question.

### 3. Write the guideline
Collect the answers into a JSON file shaped like `assets/answers_example.json` (save it as `brand/<project>/answers.json`, the source of truth), then:
`uv run python .claude/skills/business-onboarding/scripts/render_brand_files.py --project <project> --answers brand/<project>/answers.json --artifact-data brand/<project>/guideline.data.json`
This writes `brand_guideline.md`, `brand_voice.md`, `audience.md`, `positioning.md`, `products_services.md`, `offers.md`, `prohibited_claims.md`, `assets/colors.md`, `assets/fonts.md`, and lists competitors in `competitor_analysis/projects/<project>/sources/competitors.md`. Files that already hold real content are kept unless you pass `--force`. Copy logo and reference images into `brand/<project>/assets/` by hand.

### 4. Approval
Use the `artifact-presentation-setup` skill with the `brand-guideline` template and `guideline.data.json`. The user approves or comments section by section. Apply their comments to `answers.json`, re-render, and re-present until they approve. Only then set `status: approved` in `brand_guideline.md` and tell the user the next step: competitor research (Phase 1 of the roadmap).

## Rules
- Prohibited claims matter most: ask about them explicitly (health, income, guarantees, competitor naming, legal limits). The reviewer agent will enforce them later.
- Store only what the user told you or you verified from their own channels. Mark assumptions as assumptions.
- Never ask for passwords or API keys; connectors are authorized by the user in their own settings.
- If the user pastes a lot of material at once, extract, confirm, and ask only about the gaps.
- Reusable code lives in `scripts/`; extend those scripts instead of writing new one-off code, and add new ones to the table in `CLAUDE.md`.

## Bundled resources
- `scripts/init_project.py`, `scripts/render_brand_files.py`
- `references/interview_questions.md` - the question bank by guideline section
- `references/study_checklist.md` - what examples to ask for and what to read in each
- `assets/answers_example.json` - answers schema; `assets/progress_template.md` - resume file
- `evals/` - test prompts
