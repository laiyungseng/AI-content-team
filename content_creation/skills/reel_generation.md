---
type: methodology
name: reel_generation
status: active
phase: 3
adapted_from: UPT viral-sales-video-clone, ugc anti-slop rules, Seedance prompt formula, shot list template, Higgsfield script-to-video
read_by: [reel_creator, content_reviewer]
---
# reel_generation

**Purpose:** turn one approved reel brief into a script, a shot list and, optionally, AI-generated shots. Script craft (hooks, structure, diagnosing weak videos) is in `content_creation/skills/scriptwriting/`; hook types in `shared/frameworks/hooks.md`; CTAs in `shared/frameworks/cta.md`. This file covers the plan from a winning reference to a shot list, the generation prompt format, and the cost and safety rules.

Reel timing default: 0 to 3s hook · 3 to 10s problem · 10 to 30s value · 30 to 45s proof · 45 to 60s CTA. The reference video's own structure outranks the default.

## Two ways to start
- **From a brief only:** write the script with `scriptwriting/writing-a-script.md`, then step 4 onward.
- **From a reference video** (a competitor item marked Adapt in the intelligence run): learn its structure, then write our own. Steps 1 to 3.

## Process
1. **Material.** Take the reference from the intelligence run: the item's media, its transcript (when step 10, `transcribe.py`, has run), key frames, and the `hook_analyzer` breakdown. No transcript: the structure and hook can be described from frames, but the spoken rhythm is a guess, so say so and cap confidence at medium. Only use public content or files the user supplied. Never go around private access, captchas, DRM or paywalls; if a link will not open after a few honest tries, ask for the file instead of guessing.
2. **Take the reference apart,** in time order: each segment's visual (cuts, framing, action, props, setting), what is said (verbatim from the transcript, never reworded or guessed), and why it works (hook logic, emotion turn, cognitive load). Then at least three reasons it works as a whole (pacing and information density, emotional reversal, a short path to the offer).
3. **Plan our version.** Decide per segment what we **keep**, what we **replace**, and what we **drop**:
   - *Keep (the mechanism):* the hook type and the first-second action, the number and function of shots, where proof, objection-handling and CTA land, the emotional curve and information density.
   - *Replace (the brand):* brand, industry, audience, offer, the three proof points, setting, props, who appears, CTA wording.
   - *Never copy:* distinctive lines, brand assets, someone's personal story, or footage. The 1:1 mirror rule of the source method is dropped: we rebuild the mechanism for our angle, we do not clone. Add or merge a shot when our angle needs it, and say why in the plan.
   - Proof must be real and in the brand files. Never invent numbers or certifications.
4. **Check the five things** before writing the final version: brand, audience (specific), exactly three hard selling points (numbers, firm promises, or sharp contrasts; "good service" is not one), market or place, voice and language. Missing one: ask for it. A selling point that is vague gets replaced by something verifiable; an unproven number gets confirmed with the user.
5. **Write the script** (spoken words) and the shot list. A shot's time is set by speech: roughly 4 to 4.5 characters per second for Chinese, 2.5 to 3 words per second for English. 60 characters squeezed into 8 seconds produces unnatural speed and ruined gestures; lengthen the shot or cut words. Typical shot lengths: hook or pain 5 to 8s, solution 7 to 10s, proof 5 to 10s, CTA 3 to 5s (short and rising).
6. **Prompts** (only if generating video): format below.
7. **Review.** `content_reviewer` scores the script and shot list against the brief; claims are checked against `shared/platform_rules/` and `prohibited_claims.md`. Generation does not start until the script is approved.
8. **Generate a sample first.** One shot, preflight cost shown, the user approves the cost and later the sample. Then the rest.

## Shot list columns
Use `content_creation/templates/reel.md`. One row per shot: **Shot and function** · **English generation prompt (six parts)** · **Voice-over** (spoken form) · **Reference prep** (images, audio, on-screen text) · **Prompt in the working language (optional)** · **Full prompt** (reference block + style block + shot block + voice block, below). Shot count follows the plan from step 3, not a fixed number. No voice-over: write `[no voiceover]` and mark lip-sync not applicable.

## Generation prompt format (Seedance style)
Six parts, English first:
```
Use @Image2 for the [scene] context. 1 shot, [N]s, 9:16.
[Subject] who is in frame: look, clothing, props
[Action] gesture by gesture, in order
[Setting] where, light, background
[Camera] shot size, point of view, movement, angle
[Style] authentic phone footage, raw, natural skin texture, no VFX
```
Declare the reference on the first line; give exact seconds; actions in order (the model parses them in order); style keywords repeat the anti-slop terms.

Reference slots: `@Image1` character face (one consistent person, so the face does not change per shot) · `@Image2` scene (street-view screenshot, real photo, or render) · `@Image3` outfit · `@Audio1` accent and voice reference · further `@Image`/`@Audio` for props, secondary people, ambient sound.

**Full prompt, four blocks, fixed order:** (1) reference list with how each asset is made or collected, (2) global style block, (3) the shot (subject, action, setting, camera, "not a gimbal, not a smooth tracking shot"), (4) voice block with the full line. Spoken lines are rewritten to be said aloud: numbers in the way people say them, long English figures or units shortened for lip-sync.

Add a **reference collection list** under the table: for each `@Image`/`@Audio`, what to prepare and the requirements (clear signage, empty entrance, natural daylight; 30+ seconds of voice that contains the target keywords).

### Global style block (anti-slop)
Every shot's full prompt embeds this block word for word, between the references and the shot:
```
[Global style: real UGC]
First-person short video from a friend's point of view. Native phone footage, unretouched, vertical 9:16, natural handheld shake with slight breathing sway, occasional slight focus drift. Candid vertical short-video look, amateur feel, slightly imperfect framing. Soft natural ambient light, no added lighting, real skin texture with visible pores. Strictly forbidden: captions, music, overlays, effects, colour grading, cinematic look, gimbal-smooth moves, crisp high-definition sharpness, professional camera moves.
```
Why: video models drift towards a cinematic, stabilised ad look, and viewers swipe away when the first second looks like an ad. Only replace it when the brief explicitly asks for a different look (office-professional: steadier phone, light text cues allowed, no music or grading; outdoor vlog: handheld, natural ambient sound, jump cuts allowed). Check before delivering: the block is complete (not summarised), the forbidden list is intact, and it is in every shot.

## Cost and tools
- **Higgsfield (Seedance 2.0), only if the brand uses it.** Not required; the script and shot list are useful without it. Credits cost real money: show the preflight cost before any generation (`get_cost: true`, no credit used). Rough scale from the source: 5s about 15 credits, 8s about 25, 12s about 36 at 720p 9:16. Generate one sample shot, get the user's approval on face, scene, gestures and voice, then batch the rest in parallel and join them (the web tool calls this a Hyperframe; the MCP tool is `explainer_video`).
- Lessons worth keeping: select the team workspace first (the default free workspace refuses reference roles with a 403 "plan required" error even when the balance looks fine); use `image_references` and `audio_references` roles, not `start_image` or `audio`; use the MCP tools, not the CLI, for multi-reference; the audio reference teaches voice and accent, it is not a hard lip-sync file (say in the prompt: speak these lines in the reference accent and natural pace); no composite first frame is needed when native multi-reference is available; do not use street-view for building signs when a real photo exists; no stock photos; follow the approved script word for word, with no "improving" the wording.
- Generation time: about 3 to 5 minutes for 12s at 720p; parallel jobs queue.
- **Without Higgsfield:** deliver the script, shot list and reference list for filming, or use whichever video generator the user names. The rules above still hold.

## Safety
- Never put tokens, keys, cookies or logins in files or logs.
- Do not modify the user's original media; work in a separate folder.
- Real people and brands: faces are generated or provided with rights; no real trademark names or logos in generated scenes.

## Output
`drafts/<content id>/script.md`, `shots.md` (the table, with the reference list), and any media. Statuses and approval as in [[carousel_generation]] step 7.

## Review checks (for `content_reviewer`)
- Script follows the reference's mechanism, not its words.
- Exactly three hard selling points, all supported by brand files.
- Hook within 3s, named type from `hooks.md`; CTA type named.
- Speech fits shot times.
- Style block complete in every shot; reference list present.
- No invented proof, no prohibited claim, no real brand marks in scenes.
