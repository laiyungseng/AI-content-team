---
source: social-media-automation 0.2.0 / initial-brand-folder-setup/SKILL.md (adapt)
copied: 2026-10-31
---
---
name: initial-brand-folder-setup
description: Interviews the user to set up this project's brand knowledge folder: 01-brand/brand.md, 02-guidelines/voice-and-rules.md, and one platform playbook under 03-platforms/. Use whenever the user wants to set up, fill in, complete, or rework their brand file, voice and tone, content rules, visual direction, or a platform guide (captions, hashtags, CTAs, cadence, format specs), or asks "set up my brand folder", "fill in brand.md", "help me define my voice", "set up my Instagram", "add TikTok", or points at any of those files. Runs one file at a time, presents a first draft by the fifth turn, then keeps asking until the file has enough real information to sign off. Do NOT use it to write posts (that is the content pipeline), build strategy or pillars (content-strategist), or write video scripts (social-media-scriptwriting).
---

# Initial Brand Folder Setup

Interview the user to fill three files, in this order:

| Stage | File | Reference |
|---|---|---|
| 1 | `01-brand/brand.md` | `references/brand.md` |
| 2 | `02-guidelines/voice-and-rules.md` | `references/voice.md` |
| 3 | `03-platforms/<platform>/<platform>.md` | `references/platform.md` |

Load the stage reference when you start that stage. Each reference holds two lists: **Core** (the minimum the file needs before sign-off) and **Topics to explore** (raise them, keep what the user gives you). `references/examples.md` holds pickable option banks for fields users stall on; pull from it instead of writing an open question twice.

The user is not a marketer. Ask plain questions. Explain a term in one line the first time you use it.

## The two rules that shape every file

**1. The interview must get real information.** These files steer every future post, so a file built on thin answers is worse than a short file built on true ones.

- Raise every Core item with the user. A Core item is covered only when the answer is specific enough to write from. "Quality", "good service", or "everyone" do not count; push for the real thing (see "Asking well").
- Raise every Topic to explore at least once, even if only as a quick bundled question ("Any of these apply to you: awards, press mentions, a founding story worth telling?"). A topic may be dropped only after the user has been asked.
- Do not sign a file off while a Core item is still uncovered. Keep asking after turn 5 until it is covered, or until the user explicitly says they cannot answer it.

**2. The file holds only what the user gave you.** The structure is fluid, not a template.

- Write a section only when there is real content for it: the user's answers, their material, or a proposal they accepted. If they were asked and had nothing, leave the section out entirely, heading included. No empty headings, no placeholder text, no "[to revisit]".
- Shape the headings around this brand. A service business gets no Products section. A solo founder may merge Mission and Story into one paragraph. A brand with one product does not need a "Products" heading over a single block. Name sections in the user's terms where it reads better.
- Do not number sections or parts ("section 5", "Part C"). Other files refer to sections by heading name, and numbers break as soon as sections differ between brands.
- Do not copy the topic list's order or wording into the file. Order sections by what matters most to this brand.

**Exception, always asked and always written:** banned claims (brand.md) and hard rules and legal limits (voice-and-rules.md). Ask directly. If the user confirms there are none, write one line: "None stated by the user as of YYYY-MM-DD." That line tells the pre-publish check the question was asked, which an absent section cannot.

## Turn budget: first draft by turn 5

1. **Turn 1.** Say which file you are filling and roughly what it covers. Ask for their real material (see below). Ask the first 2 to 3 Core questions.
2. **Turns 2 to 4.** 2 to 3 questions per turn, Core items first, then Topics to explore. Offer options from `references/examples.md` so they pick and edit rather than compose from blank.
3. **Turn 5.** Write the draft and show it. Then list, in chat, any Core items still uncovered and ask about them.
4. **After turn 5.** Keep asking until every Core item is covered, then ask what they want to add, change, or cut. Keep editing until they sign off. There is no turn limit here; the turn-5 budget exists to get a real file in front of them fast, not to stop asking.

Do not start the next stage until the current file is signed off. Do not fill fields belonging to another stage's file.

## Asking well

- 2 to 3 questions per turn, then stop.
- Give options to react to. "Which of these five is closest, and what is wrong with it?" gets a truer answer than "what is your voice?"
- Follow a pick with "what made you choose that?" so their reasoning lands in the file.
- Push past generic answers. Ask what a competitor honestly could not say.
- Use their words in the file, not marketing phrasing.

## Ask for their real material

At the start of each stage, ask the user to paste or point you at:

- Past posts, captions, emails, or even texts to a customer (stage 2 needs these most: how they already write is their voice).
- Two or three competitor or admired accounts, with one line on what they like about each.
- Their website, menu, price list, or pitch deck, if they have one. Read it and reflect back what you found instead of re-asking it.

Real material beats any answer they give in the abstract. If they have none, keep going.

## When the user does not know

Work down this list, one rung at a time:

1. **Shrink it.** Not "what are your values?" but "tell me about a time you turned down money because the job felt wrong."
2. **Offer examples to pick from.** `references/examples.md` has banks per field. Ask which is closest and what they would change.
3. **Let the AI decide, with a disclaimer.** Only for judgment items, and only if they say "you decide" or "make something up". Write it, tag it `[AI guess, confirm]`, and tell them plainly in chat: this is my guess, not your brand, and it will steer every future post until you fix it. Never do this for facts.
4. **Drop it.** If it is a Topic to explore, leave it out of the file and move on. If it is a Core item, say so plainly, add it to `open-questions:` in the frontmatter, and keep the file at `status: draft`.

**Never guess a fact.** Brand name, founding year, prices, product names, website, handles, legal or compliance rules, banned claims: these come from the user or are left out. An invented fact ships as truth.

## Reuse what exists

Read any file that is already filled before asking about it: `01-brand/brand.md`, `02-guidelines/voice-and-rules.md`, `04-strategy/strategy.md`. Reflect back what you found and ask them to correct it rather than re-asking. Never block on an empty file.

When reworking an existing file, keep every section that still holds real content, even if it is not on the current topic list. Remove a section only if the user says it is wrong or no longer true.

## Writing the file

Rewrite the whole file from the interview; do not fill in the skeleton's instructions. The skeleton only carries frontmatter and a one-line purpose.

Frontmatter, every time:

```yaml
---
status: draft            # skeleton → draft → filled
last-updated: YYYY-MM-DD # today
owner:                   # keep whatever was there
open-questions: []       # Core items still uncovered, in plain words; omit the key when empty
---
```

Keep any `platform:` line. Set `status: draft` once the first draft is written. Set `status: filled` only when every Core item is covered and the user has signed off; remove `open-questions:` at that point.

Under the title, keep one line saying what the file is for, then the sections.
