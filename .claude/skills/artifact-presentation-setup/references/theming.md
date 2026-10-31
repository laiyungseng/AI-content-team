# Theming from a user reference

A theme is a JSON file (see `assets/themes/default.json`):
`fonts_url` (a Google Fonts CSS URL), `fonts{display, body, mono}`, `radius`, and `light{}` / `dark{}` colour maps with the keys
`bg, surface, surface-2, fg, muted, line, accent, accent-fg, good, warn, bad, info`.

## Turning a reference into a theme
1. **Identify the reference.** A URL (open it with the built-in browser, read the computed colours and fonts), a screenshot or image (look at it), a Figma file (use the Figma connector if authorized), or brand files already in `brand/<project>/assets/` (`colors.md`, `fonts.md`).
2. **Extract:** one background, one surface, text, one accent, and the corner radius (sharp = 2-4px, soft = 12-16px). Pick fonts: the reference's display font and body font if they exist on Google Fonts; otherwise the closest Google font, and tell the user which one was substituted.
3. **Build both modes.** If the reference is light, derive the dark palette by lowering lightness of bg/surface and raising the accent's lightness until text and accent keep contrast. If it is dark, derive light the same way in reverse. Do not just invert.
4. **Check contrast:** `fg` on `bg` and `accent-fg` on `accent` at least 4.5:1; `muted` on `bg` at least 3:1 for large text, aim for 4.5:1.
5. **Neutrals lean toward the accent hue** (a slight tint) so the page looks deliberate.
6. Save to `brand/<project>/assets/artifact_theme.json`, rebuild, and show the user.

## Tuning requests
- "More playful": larger `radius`, rounder display font, a warmer accent.
- "More serious": smaller `radius`, tighter neutrals, one restrained accent.
- "Match our brand": use the brand palette from `brand/<project>/assets/colors.md` as accent and neutrals.
Change the theme file only; do not edit templates for colour or font changes.
