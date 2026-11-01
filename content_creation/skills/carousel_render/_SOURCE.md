---
source: UPT-course-setup-v2.skill / course-skills/carousel-html
copied: 2026-10-31
status: adapted
destination: Phase 3 production (plan step 8b)
---
# carousel_render: where these files came from

HTML templates, `_base.css`, brand-kit `_template.json` and the five presets are byte-identical copies of the `carousel-html` skill's assets.
They are kept in the original `assets/` layout so `assets/scripts/render.py` finds them without path changes.

`render.py` is the original with five small text edits (usage example path, two comments, the missing-Chrome message now points to `CHROME_PATH`, one path hint) and one fix: stdout/stderr are switched to UTF-8 at the start of `main()`, because the original crashed on Windows consoles (cp1252) when printing its arrow. Rendering logic is untouched.

Not copied on purpose: client and personal brand kits, the three creator-specific templates, the `claude` brand kit, and the GPT-image-2 path (we use nanobanana).

How it renders: each page is an HTML template with `{{SLOT}}` placeholders plus a brand kit (colours, fonts, handle). Headless Chrome screenshots every page to a 1080x1350 PNG. Needs Chrome, Chromium or Edge.

Still to build: `brand_kit.py`, which generates a kit from `brand/[project]/` so no preset has to be picked by hand.

Method docs are rewritten into `content_creation/skills/carousel_generation.md` and `carousel_recipes.md`; the staged originals were deleted (2026-11-01).
