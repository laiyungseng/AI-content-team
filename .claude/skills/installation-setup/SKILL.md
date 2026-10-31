---
name: installation-setup
description: Set up the AI content team on any machine (Windows, macOS, Linux) from scratch or repair a broken setup - uv, git, node, ffmpeg, Python libraries, workspace folders, MCP connectors (Apify, Zernio, Perplexity, NotebookLM, nanobanana, Notion, Figma), and an offline smoke test. Use this whenever the user starts on a new PC, just cloned the project, says "set up", "install", "get ready", "missing tool", "ffmpeg not found", "connect Apify/Zernio/Perplexity", or when any other skill fails because a tool, library or connector is missing, even if they never say "installation". Also run it as step 0 of business-onboarding.
---

# Installation setup

Get a machine ready so later skills do not fail halfway. All logic is in one cross-platform script, `scripts/setup.py`,
run through uv (uv also downloads the right Python, so no system Python is needed). Reuse it; do not retype install commands.
The user-facing beginner guide is the "Install" section of `README.md`; keep the two in step.

## Workflow
Run every command from the workspace root. `$S` = `.claude/skills/installation-setup/scripts`.

0. **No uv yet?** (fresh machine) Ask, then run the launcher: Windows `powershell -ExecutionPolicy Bypass -File setup.ps1`,
   macOS/Linux `sh setup.sh`. It installs uv and then runs `setup.py all`, so skip to step 5 when it succeeds.
1. **Check** - `uv run python $S/setup.py check`. Prints the tool table and writes `state/installation_status.md`
   (tools + phase table). Exit 1 = a required tool (uv, git) is missing.
2. **Install missing tools** - say exactly what will be installed (tool, package manager, purpose) and wait for a yes,
   because installing changes their system. Then `uv run python $S/setup.py install <tool...> --yes`.
   It uses winget (Windows), Homebrew (macOS) or apt (Linux). `node` is only needed for the Perplexity connector,
   `ffmpeg` only for reels. If no package manager exists, use `references/manual_install.md`.
   The script reloads PATH itself; if a tool still shows MISSING, the user needs a new terminal (or Claude Code restart).
3. **Python + folders** - `setup.py python` (`uv sync`), then `setup.py scaffold`. Add `--media` to `python` only when the user
   wants reel download/transcription; it is a large download, so say so first.
4. **Smoke test** - `setup.py smoke`. Runs the real pipeline offline on a throwaway project `zz_smoketest` and deletes it.
   Setup is not done until this passes. `setup.py all` runs steps 1, 3 and 4 in one go.
5. **Connectors** - ask what the user wants to do first, then follow `references/connectors.md` for that tier only.
   For image/video generation, ask which they prefer: **nanobanana**, **Higgsfield**, both, or set up later (Apify + Perplexity
   are enough to start). Record the choice; skipped ones stay unticked in the checklist, not failed.
   You cannot sign in or enter API keys for them; never ask them to paste keys into chat.
6. **Checklist and report** - copy `assets/install_checklist.md` to `state/install_checklist.md`, tick each item from
   `state/installation_status.md` and the connector checks, and show it to the user. Setup is finished only when every
   required item is ticked and each optional item is ticked or marked "later". Summarise what works, what is missing and what the
   user must do. Then point to `source-manager` (add competitor URLs). `business-onboarding` waits until they start production.

## Rules
- Ask before installing or downloading anything; state the package and size when known.
- Check before acting: every phase is safe to re-run, so on "set up" again just read the status file and continue from the first phase that is not `done`.
- Log tool failures or user overrides in `memory/_system/` (see CLAUDE.md memory rules).
- If a task needs a new script, save it in this skill's `scripts/` and add it to the "Reusable code" table in `CLAUDE.md`.

## Bundled resources
- `scripts/setup.py` - `check` / `install` / `python` / `scaffold` / `smoke` / `all`
- `scripts/smoke_test.py` - offline end-to-end test (called by `setup.py smoke`)
- `scripts/scaffold_workspace.py --root <folder>` - rebuilds base folders, agent stubs and templates; never overwrites
- `../../../setup.ps1`, `../../../setup.sh` - launchers at the workspace root (install uv, then `setup.py all`)
- `../../../.mcp.json` - local MCP servers for this project (keys come from environment variables)
- `references/connectors.md` - connector tiers, account vs local, how to enable each per OS
- `references/manual_install.md` - fallbacks when no package manager is available
- `assets/install_checklist.md` - checklist template for the final report
- `evals/` - test prompts
