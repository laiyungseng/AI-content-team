---
type: methodology
name: carousel_generation
status: active
phase: 3
adapted_from: UPT carousel-html (method, design rules, industry recipes, content ideas)
read_by: [carousel_creator, content_reviewer]
---
# carousel_generation

**Purpose:** turn one approved carousel brief into 1080x1350 PNG pages, rendered from HTML templates by headless Chrome. Text is always exact (no image-model text), and one brand kit gives every page the same look. Used by `carousel_creator` (one brief per run); `content_reviewer` uses the audit in step 6.

Files: `content_creation/skills/carousel_render/` (`assets/templates/` 11 layouts + `_base.css`, `assets/brand-kits/` presets and `_template.json`, `assets/scripts/render.py`). Needs Chrome, Chromium or Edge (`CHROME_PATH` if installed elsewhere). `_SOURCE.md` there records provenance.

## Process
1. **Brief.** Read the brief (`content_creation/templates/content_brief.md`): hook, angle, audience, claims to avoid, CTA. Stop if the brief is not `brief_ready` or the angle has no [[angle_evaluation]] score.
2. **Brand kit.** `brand/[project]/` is the source. In order:
   1. `assets/brand-kits/<project>.json` exists: use it.
   2. Build one from `brand/[project]/` (colours, fonts, handle, tagline) with `brand_kit.py` (to be built; until then write the JSON by hand from `_template.json` and show it to the user before saving).
   3. The user gave a reference image: read it, propose colours and tone (hex by eye, give a range), confirm, then save.
   4. Nothing yet: offer a preset (below), copy it to `<project>.json`, set name, slug, handle, tagline.
   Never save a kit the user has not confirmed. The fallback font chains already cover macOS and Windows; do not import web fonts (headless timeouts).
3. **Sequence.** Pick a content type and its pages (below). Industry hints: [[carousel_recipes]]. A free mix of the 11 layouts is allowed.
4. **Write the copy** per page into the layout's slots, within the character limits. Over a limit: shorten, split into two pages or change layout. Never pretend it fits. No emoji unless the brand voice asks for them.
5. **Render.** Work folder `content_creation/projects/[project]/drafts/<content id>/`. Write `config.json`:
   ```json
   { "brand_kit": "<slug>", "pages": [ { "layout": "01-cover", "slots": { "HEADLINE": "...", "SUBTITLE": "..." } } ] }
   ```
   then `uv run python content_creation/skills/carousel_render/assets/scripts/render.py --work-dir <folder>`. Photos go in as `IMAGE_PATH` (absolute path; the script embeds them as base64, relative paths break). `PAGE_NUM`, `HANDLE`, `BRAND_NAME`, `TAGLINE` and `SLOGAN_FOOTER` fill themselves from the kit.
6. **Verify, two layers, never skipped.** Open every PNG.
   - *Technical:* script-correct glyphs (no tofu boxes or garbage); brand colours match the kit; no overflow or cut text; header (handle, page counter) and footer (slogan, swipe or end) present on every page; photos placed, not stretched; 1080x1350; sensible whitespace.
   - *Design:* run the 22-item audit below. Hand this layer to `content_reviewer` (the creator never approves its own work). Each fix means re-render, re-open, re-check.
7. **Deliver** the PNGs to `drafts/<id>/page<N>.png` with `config.json`, set the brief to `draft_ready`, and present through `artifact-presentation-setup`. Publishing is blocked until `status: approved` and `publish_authorized: true`.

## Layout slots and limits
Limits are for the roman-letter or CJK count shown; for English roughly double them when the headline font is not CJK. When in doubt render and look.

| Layout | Slot (limit) |
|---|---|
| `01-cover` | HEADLINE (14), SUBTITLE (40) |
| `02-big-statement` | HEADLINE (16), SUBTITLE (35) |
| `03-title-body` | TITLE (16), BODY (80; `<br>`, `<strong>` allowed) |
| `04-numbered-step` | TITLE (12), STEP_N_TITLE (14), STEP_N_DESC (25) |
| `05-checklist` | TITLE (14), ITEM_N (16), ITEM_N_NOTE (22) |
| `06-stat-cards` | TITLE (14), STAT_N_NUM (4), STAT_N_LABEL (12) |
| `07-quote` | QUOTE (30), ATTRIBUTION (20) |
| `08-comparison` | TITLE (12), LEFT/RIGHT_HEADER (18), LEFT/RIGHT_BODY (45) |
| `09-testimonial` | QUOTE (60), CUSTOMER_NAME (8), RESULT_NUM (6) |
| `10-image-caption` | IMAGE_PATH, HEADLINE (18), CAPTION (45), TAG |
| `11-cta-closing` | HEADLINE (14), CTA_TEXT (10) |

Unused `ITEM_N`, `STEP_N` and `STAT_N` slots are removed by the script. Do not invent new layouts; if one is truly missing, ask first.

## Content types and page sequences
| Type | Pages | Sequence |
|---|---|---|
| How-to | 7 | cover, steps 1 to 5, CTA |
| Listicle | 8 | cover, items 1 to 6, CTA |
| Quote poster | 1 to 3 | big-statement or quote |
| Mistakes to avoid | 6 | cover, 5 mistakes (comparison or title-body), CTA |
| Case breakdown | 7 | cover, starting point, key actions, result, CTA |
| Testimonials | 3 to 5 | cover, testimonial 1 to 3, CTA |
| Numbers | 4 to 6 | cover, stat cards, conclusion, CTA |
| Before / after | 5 | cover, before, after, comparison, CTA |

More ideas by frequency. **Common:** how-to, quote poster, mistakes to avoid, tool recommendations, case breakdown, testimonials, X-vs-Y comparison, numbers. **Medium:** thinking framework or formula, listicle, Q&A, trend roundup, glossary, mini course, resource list, teaser or reveal. **Rare but differentiating:** personal story or journey, before/after, public ledger or transparency, client onboarding walk-through, behind the scenes, holiday or news hijack, event recap, course cliff-notes. A type is not a layout: content is written by the brief, the skill only lays it out. Anything the competitor evidence shows winning in this account's niche outranks this list.

## Design rules (defaults; a brand kit or reference image can override any)
1. **Warm palette lock:** off-white or cream background, never pure white; warm near-black text, never `#000`; no cold blue, purple, green or grey. Dark-mode kits keep the same temperature discipline.
2. **Corner brackets:** thin L-shaped marks (0.75 to 2px, 80 to 100px), either top-left and bottom-right, or all four, in the accent or muted ink.
3. **Ghost watermark word:** one huge outlined or tonal word, 35 to 50% of page height, a shade off the background (no opacity tricks), partly cropped; the headline floats above it.
4. **Header:** handle left, page counter right (`01 / 10`, tabular numerals), about 80 to 110px tall.
5. **Footer:** brand slogan left (same on every page), `SWIPE →` right (`END` or a CTA pill on the last page), a 1px hairline above.
6. **Type pairing:** headline in a heavy serif (weight 700 to 900), body in a regular or medium sans. Sizes roughly: H1 96 to 150px, sub-head 60 to 90, body 28 to 42, eyebrow 18 to 32. At least four size levels. Space between CJK and Latin characters.
7. **Eyebrow label** over the headline: small, caps, tracked +180 or more, in the accent or muted ink (`STEP 03`, `REALITY CHECK`).
8. **Big numeral** as the visual anchor on step and list pages (110 to 220px), not an icon.
9. **Accent discipline:** the accent colour appears in only three or four fixed slots per page (one headline word, eyebrow underline, divider, quote mark or pill). Rare accent has punch.
10. **Divider:** a short accent stub (80 to 180px wide, 3 to 5px tall) under H1, not a full-width rule; a 1px full-width hairline between header, body and footer.
11. **Pill chips:** fully rounded, 15 to 20% tint of the accent, small caps or mono text, no shadow.
12. **No drop shadow:** create lift with cream background against white cards. At most `0 8px 24px rgba(0,0,0,0.06)`.
Stat cards always get a `2px solid rgba(0,0,0,0.08)` border so a white kit does not melt into the page. Use a curly quote mark in serif quotes.

**Style presets** (a starting point for a kit): *Editorial cream* (cream background, vermilion accent, serif heavy; coaches, knowledge, premium training) · *Dark glow gradient* (warm black, magenta to orange gradient accent; agency, warning, high-contrast sales) · *Magazine* (cream or forest dual mode, champagne accent; luxury, personal brand) · *Notebook* (parchment with a faint grid, coral accent, pastel chips; tech and SaaS). Ready kits in `assets/brand-kits/presets/`: modern-minimal (SaaS, tools, B2B consulting) · bold-marketing (agency, coaching, sales, courses) · editorial (writers, consultants) · luxury (premium services, property, legal) · warm-coach (coaching, personal brand, parenting).

**Per-layout upgrades** worth applying when editing a template: cover gets brackets, eyebrow and watermark and a headline near 110px; big-statement uses the accent on one word only; title-body uses a short hairline; numbered-step uses a serif numeral; checklist adds warm/white contrast and 32px row gap; stat-cards darkens only one card; quote gets a bracket frame; comparison uses warm coral against warm sage, not red/green; testimonial adds an eyebrow and a serif result number; image-caption uses a bottom-fade overlay, not a heavy full overlay; CTA uses an organic gradient angle with corner blooms.

## Design audit (22 items; every one must pass)
**Colour:** 1 background not pure white · 2 text not pure black · 3 accent only 3 to 4 times per page · 4 no cold colours · 5 whole palette on one temperature.
**Type:** 6 H1 heavy serif · 7 body sans regular or medium · 8 at least four size levels · 9 eyebrow tracking +180 or more · 10 spacing between CJK and Latin.
**Layout:** 11 header has handle and page counter · 12 footer has slogan, swipe and hairline · 13 header and footer identical on every page · 14 at least 64px breathing space between content and header/footer.
**Detail:** 15 at least one bracket, watermark or hairline · 16 short accent divider under H1 · 17 no drop shadow · 18 pills fully rounded.
**Quality:** 19 no overflow or cut text · 20 no tofu boxes · 21 1080x1350 · 22 one clear focal point per page.
Common beginner mistakes to flag: pure white or black, accent used as decoration, sans headline, no eyebrow, no consistent footer, shadows for depth, 8px-radius pills.

## Do not
- Use an image model for layout-led pages. Text-led pages come from the templates; photo or illustrated pages go through [[static_post_generation]] with nanobanana. A hybrid (generated decoration embedded in an HTML page) is allowed when the text must be exact and the decoration illustrated.
- Send PNGs as "done" before the technical checks.
- Make up a layout, or ignore the limits.
- Add claims the brief or `brand/[project]/prohibited_claims.md` forbids.

## Output
`drafts/<content id>/page<N>.png`, `config.json`, and a short note for the reviewer: kit used, layouts used, anything shortened. Costs: Chrome only, no credits.
