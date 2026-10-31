---
source: social-media-automation 0.2.0 / initial-brand-folder-setup/references/platform.md (adapt paths to brand/[project]/)
copied: 2026-10-31
---
# Stage 3: the platform playbook

Everything for writing content on one platform: the account and its role, caption style, and format specs.

This is a menu, not a template. The file gets a section only for what the user actually gave you or accepted, grouped and named to suit the platform.

## Which platform first

Recommend Instagram first when the brand is on it: the caption style, hook patterns, and CTA bank built there get reused on every other platform. If the user is not on Instagram, or still prefers another platform after hearing the reason, set up their platform first. Their call, not yours.

## You duplicate the folder, not the user

Never assume the folder exists. Before starting a platform:

1. Check whether `03-platforms/<platform>/` exists.
2. If not, copy the whole `03-platforms/_platform-template/` folder to `03-platforms/<platform>/`, rename `platform-guide.md` to `<platform>.md`, and set `platform: <platform>` in the frontmatter.
3. Then run the interview on that file.

For Instagram the folder already exists; use `03-platforms/instagram/instagram.md`.

After the playbook is signed off, add the platform to the platform roles in `04-strategy/strategy.md`, or tell the user to. If this is not Instagram, also update the "Platform specs checked" line of the pre-publish checklist in `06-content/workflow.md` so it names every platform playbook.

## Ask for their material on turn 1

- Their own best and worst past posts on this platform, if any. Ask what they think made the difference.
- Two or three competitor or admired accounts on this platform, and one line on what they like about each.

Read these before drafting hooks, hashtags, or CTAs. A bank built from their niche beats a generic one.

## Read first

- `01-brand/brand.md`: customers, products, the customer's own words.
- `04-strategy/strategy.md`: pillars, content mix, platform role.
- `02-guidelines/voice-and-rules.md`: the voice, so caption examples sound right.

Do not block if any is empty or missing a section.

## Core (needed before sign-off)

1. **Account.** Handle and account type (business or creator). **Fact.**
2. **Role of this platform.** One primary objective (awareness, community, or sales) and who it is for here. Propose from `strategy.md` if it exists.
3. **Posting cadence.** Posts per week by format. Anchor to what they can sustain: "what is the most you have actually kept up for a month straight?"
4. **Caption structure.** Hook line, body length, CTA placement, hashtag placement if used. Show it with one real example built from their topics, and get it confirmed.
5. **Hooks and CTAs.** At least 3 hook patterns and 3 CTAs they approve. **Draft generously, then make them prune.** A bank is not done until they have cut some, picked favourites, and added at least one of their own. Draft from their real topics; see the hook and CTA banks in `examples.md`.
6. **Formats they use.** One block per format they actually post (or plan to within a month), with current specs. Leave out formats they do not use.

## Topics to explore (raise each at least once)

### Platform guide
- Current bio and link-in-bio setup. **Fact.**
- Content mix: ratio across pillars and value-versus-promo split. Must match `strategy.md` if it exists.
- Tone here: how the voice flexes on this platform.
- Community management: reply-time target, how to reply to praise, questions, and complaints (point to the holding statements in `brand.md` if they exist), interactive features they use.
- Growth tactics: approved (collabs, UGC, trends) and banned (buying followers, pods). Propose defaults, have them confirm.
- What wins here: start it from their own best past posts. Skip if they have none.
- Best posting times, if they know them from their own data.

### Caption style
- Formatting: line breaks, emoji rules (pull from `voice-and-rules.md`), mentions.
- Target caption length per intent.
- Hashtag bank: brand hashtags, then 5 to 10 per pillar mixing broad, medium, and niche, plus a count and placement rule. Only if this platform uses hashtags.
- CTA rotation rule (default in `examples.md`).
- Language(s) captions are written in, if different from the voice file.
- Model posts: 3 once real ones exist, one per major intent, with why each works.

### Formats and specs
- Per format: dimensions, ideal length, hook rule (first 2 seconds, slide 1), slide or subtitle rules, audio, cover image, bundle.social publishing parameters.
- Cross-format rules: how one idea adapts, what never gets cross-posted.

Specs are not judgment, but they are facts that drift. Check current specs with a web search when you can. If you cannot, propose them from what you know, tag each `[AI guess, confirm]`, and tell the user to verify them quarterly. Draft this part fully and have them confirm rather than asking them to supply dimensions.
