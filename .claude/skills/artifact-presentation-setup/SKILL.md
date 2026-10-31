---
name: artifact-presentation-setup
description: Present work to the user as an interactive, themeable Claude Artifact page and collect their approval - approval boards for briefs and drafts, reel/carousel/static previews, competitor intelligence reports, publishing calendars, and brand guideline reviews. Use this whenever output needs to be shown, reviewed, approved, compared or "presented", when the user says "show me", "let me review", "approve", "preview the content", "make it look nicer", "use this design/reference/style", or when any other skill (business-onboarding, strategy, generation, review) reaches an approval gate, even if the user never says "artifact" or "presentation".
---

# Artifact presentation

Walls of markdown in the terminal are hard to read and hard to approve. This skill turns structured output into a clean page the user can browse, then records their decisions so the workflow can continue. Templates already exist; your job is to fill them with data, apply the right theme, publish, and read the decisions back.

## Pick a template

| Need | Template | Records decisions? |
|---|---|---|
| Review briefs, strategy items, any list needing approve / changes / reject | `approval-board` | yes |
| See reel scenes, carousel slides, static posts as they will look | `content-preview` | yes |
| Present competitor / performance intelligence | `intelligence-report` | no |
| Show the publishing schedule and campaign chains | `publishing-calendar` | no |
| Review and approve the brand guideline section by section | `brand-guideline` | yes |

`python scripts/build_artifact.py --list` lists what exists. No template fits? Add a new one to `assets/templates/` (copy the closest; keep the `/*__THEME__*/`, `/*__SHARED_CSS__*/`, `/*__SHARED_JS__*/`, `__DATA__` placeholders) and note it in `references/data_schemas.md`, so the next run reuses it instead of starting over.

## Workflow

1. **Shape the data.** Write a JSON file following `references/data_schemas.md`. Save it next to the work it presents, e.g. `content_creation/projects/<project>/review/<name>.data.json`. Use real content from the project files, never invented figures. Item `id`s must be stable (C001, PAT-0041) because decisions are keyed on them.
2. **Build.** `uv run python .claude/skills/artifact-presentation-setup/scripts/build_artifact.py --template <name> --data <data.json> --project <project> --out <same folder>/<name>.html`
   The script picks the theme (see below) and writes one self-contained HTML file. It performs the data checks; do not hand-edit the HTML, rebuild instead.
3. **Publish.** Load the `artifact-design` skill and, for pages that record decisions, the `artifact-capabilities` skill, then call the Artifact tool with the built file. Pass `capabilities: {"db": {}}` for `approval-board`, `content-preview` and `brand-guideline`; omit capabilities for the read-only templates. Give it a short `description` and an `icon` on first publish. The file has no `<html>/<head>/<body>` on purpose, because the tool adds the skeleton.
4. **Hand over.** Give the link and say in one line what the user should do ("Approve or comment on each brief, then tell me you are done").
5. **Read decisions.** When the user says they are done, read the page's `decisions` collection with the `ArtifactData` tool (`list`, collection `decisions`). Each document id is the item id with unsafe characters replaced by `_`; fields are `decision` (`approve` / `revise` / `reject`), `comment`, `item`, `at`. If the database is unavailable the page tells the user to use **Copy summary** and paste it into chat; parse that text instead. Details in `references/approvals.md`.
6. **Apply.** `approve` -> set the item's `status: approved`; `revise` -> `status: revision` and pass the comment to the creator agent; `reject` -> back to `idea` or removed, with the reason saved in `memory/<project>/decisions.md` if it teaches something. An approval click never sets `publish_authorized: true`; that needs the user to say they authorize publishing.
7. **Save and reuse.** The built `.html` and `.data.json` stay in the project folder. To refresh a page, rebuild and publish again with the same file path so the link stays the same.

## Theme and user references

The default theme is in `assets/themes/default.json`. Theme precedence: `--theme <file>`, then `brand/<project>/assets/artifact_theme.json`, then the default.
When the user supplies a reference ("make it look like this site", a screenshot, a Figma file, brand colours, "darker", "more playful"):
1. Read `references/theming.md` for how to turn a reference into the theme JSON (tokens, fonts, radius).
2. Save the result as `brand/<project>/assets/artifact_theme.json` so every later page matches without being asked again.
3. Rebuild the current page and show it; keep iterating on the theme file, not on the HTML.
Fonts must come from Google Fonts or be embedded; mention the substitution if the reference font is not available there.

## Design rules (already built in; keep them when you add templates)
- Every colour is a token with light and dark values, so the page follows the viewer's theme.
- Phone-width friendly, no horizontal page scroll, keyboard focus visible.
- Summary and status first, detail on demand (`<details>`); one clear action per decision.
- Copy is plain and specific; no filler text.

## Bundled resources
- `scripts/build_artifact.py` - template + data + theme -> single HTML (`--standalone` for a local preview file)
- `assets/templates/` - `_shared.css`, `_shared.js`, five page templates
- `assets/themes/default.json` - default theme
- `assets/sample_data/` - example data for each template, useful for tests and as a schema example
- `references/data_schemas.md`, `references/theming.md`, `references/approvals.md`
- `evals/` - test prompts
