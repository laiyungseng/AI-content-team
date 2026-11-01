---
type: methodology
name: static_post_generation
status: active
phase: 3
adapted_from: UPT sample-clone (replace-the-copy method), carousel-html photo and decoration paths
read_by: [static_content_creator, content_reviewer]
---
# static_post_generation

**Purpose:** produce one static post or ad image from an approved brief. Two routes: **text-led** (HTML templates, exact text) and **image-led** (an image model, here nanobanana, for photographic or illustrated pictures). Caption copy comes from [[ad_copy_longform]]; carousels from [[carousel_generation]].

## Choose the route
| The post is... | Route |
|---|---|
| Mostly words (quote, stat, checklist, announcement) | HTML template via `carousel_render` with one page |
| A photo-like or illustrated scene with little text | nanobanana |
| A proven layout from a competitor (an Adapt verdict) with new copy | the layout-replace method below, with nanobanana |
| Needs exact copy over a generated picture | generate the picture without text, then place the text in an HTML template (hybrid) |

Image models draw letters; they do not type them. Long or exact text, prices, phone numbers and legal wording are always set in HTML, never drawn by the model.

## Layout-replace method (from the source, kept as an idea)
The reference is the template, not inspiration. The model's job is only to keep an existing layout and swap the words; writing a fresh design brief makes it redesign the picture and the text goes wrong. In the source's test, a 600-word design brief gave four mixed fonts and wrong characters; a replace-table on the same image gave a faithful layout with accurate text.

1. **Inputs:** the reference image (from the intelligence run, for study only) and the new copy. The user rarely supplies the old copy; read it from the picture.
2. **Read the old text exactly** (punctuation, spacing, capitals) into a table with the new text beside it:
   ```
   Headline         OLD TEXT      -> NEW TEXT
   Badge 1          OLD           -> NEW
   Corner logo      [old name]    -> (blank, we overlay the real logo)
   Unchanged slot   OLD           -> (keep)
   ```
   List unchanged slots as "keep". Show the table to the user and wait for approval. A misread old line makes the model miss the line and improvise.
3. **Measure the reference size** and produce the same size, since a different canvas forces a new layout.
4. **Prompt in three parts, 100 to 300 words, not 500:** (a) output size and "copy the attached image's design, layout, colours, fonts, badge style and overall tone 100%"; (b) the replace table; (c) the one visual difference, or "no visual change, text only". If the scene changes, say the whole scene changes (do not say "keep the composition", which yields half-changed pictures). Always end with: no real brand names, logos or sign text anywhere in the picture; leave brand positions blank or use meaningless abstract shapes (models invent real trademarks as props).
5. **Generate with nanobanana,** default model and a medium quality tier; raise the tier only for print or a client who pays for it, and ask first. Do not rely on automatic model routing.
6. **Edit in the same conversation:** one or two changes at a time, with an explicit "everything else unchanged" line. A new conversation re-reads the reference from scratch and loses earlier work.
7. **Logos are invented by the model.** Ask before generating: leave the logo area blank and overlay the real logo afterwards, or accept the generated mark.
8. **Check the output:** read every character against the table, count fonts, check the layout against the reference.

**Anti-patterns:** a fresh three-part design brief; describing layout the image already shows; "use the tone but design freely"; skipping the replace table; many changes in one prompt; a new conversation per edit.

**Boundary:** to extract a formula and make something deliberately different, work from the `hook_analyzer` and `competitor_analyzer` outputs and write an original brief. Never reproduce a competitor's creative, claims or brand assets: the layout idea is adapted, the words, people and marks are ours. Competitor work is a hypothesis, not a licence to copy. See `shared/platform_rules/meta.md`.

## Process (any route)
1. Read the brief (angle, hook, claims to avoid, CTA, platform, size). Check the platform's size and safe zones in `shared/platform_rules/`.
2. Choose the route; get the brand kit (see [[carousel_generation]] step 2).
3. Write the text (headline, support line, CTA) within the template's limits; caption via [[ad_copy_longform]].
4. Generate or render. Cost: Chrome only is free; image-model tiers cost credits, so show the cost before a batch and approve one sample first.
5. Verify: exact text, brand colours, safe zones, no invented brand marks, nothing in `prohibited_claims.md`.
6. Save `drafts/<content id>/post.png`, `caption.md`, and the prompt or `config.json`; hand to `content_reviewer`; approval and `publish_authorized` as in [[carousel_generation]] step 7.

## Review checks (for `content_reviewer`)
- Text exact and legible at phone size; no model-drawn long text.
- Layout is adapted, not a copy of a competitor's creative.
- No real trademarks, no unverified claim, regulated wording per `meta.md`.
- Size and safe zones correct for the platform.
