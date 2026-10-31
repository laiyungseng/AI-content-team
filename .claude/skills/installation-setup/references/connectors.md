# Connectors for the AI content team

Which connector supports which stage, and how to enable it on a new machine. Check what is already available in the
session first (tools named `mcp__<server>__*`, or the user runs `/mcp`). Authorization is always done by the user, never by Claude.

| Connector | Kind | Used for | Stage | Needed when |
|---|---|---|---|---|
| **Apify** | account | Scrape Instagram/TikTok/Meta Ad Library/XHS posts and metrics | research, performance | analysing competitors or own accounts |
| **Perplexity** | local | Web-grounded research, market/competitor context | research | business-onboarding research, trend checks |
| **nanobanana** (Gemini image) | local | Generate/edit images for static posts, flyers | generation | static content creation |
| **Zernio** | account | Schedule/publish posts, analytics, best time to post | schedule, publish, measure | Phase 6 publishing, performance pulls |
| **NotebookLM** | local | Source-grounded Q&A over uploaded docs, transcripts | analysis | many transcripts / long documents |
| **Notion** | account | Optional content calendar / docs sync | schedule | user keeps planning in Notion |
| **Figma** | account | Read brand design files, design references | brand setup | user supplies a Figma reference |

## Tiers (enable only what the user's goal needs)
- **Intelligence MVP (Phase 1):** Apify + Perplexity.
- **Strategy + generation (Phases 2-3):** add nanobanana.
- **Publishing + measurement (Phases 5-6):** add Zernio.
- **Optional on request:** NotebookLM, Notion, Figma.

## Account connectors (Apify, Zernio, Notion, Figma)
These belong to the user's Claude account, not the machine, so they follow the login to any PC.
1. Confirm the user is signed into Claude Code with the same account as on their other machine.
2. If the tools are missing, the user adds or authorizes the connector: Claude desktop app > Settings > Connectors,
   or `/mcp` in a Claude Code terminal. Key-based ones (Apify, Zernio) ask for the key in the connector's own form, never in chat.
3. Verify with one cheap read-only call (Apify: search for an actor; Zernio: list accounts).

## Local servers (Perplexity, nanobanana, NotebookLM)
Declared in the project `.mcp.json`, so a clone already knows how to start them. Claude Code asks the user once to approve
the project's servers. They need:

| Server | Needs | Key variable | Get the key |
|---|---|---|---|
| perplexity | node (`npx`) | `PERPLEXITY_API_KEY` | perplexity.ai > Settings > API |
| nanobanana | uv (`uvx`) | `GEMINI_API_KEY` | aistudio.google.com > Get API key |
| notebooklm-mcp | uv (`uvx`) | none; sign in once | user runs `uvx --from notebooklm-mcp-cli nlm login` in their own terminal (opens a browser) |

The user sets each key **themselves in their own terminal** (not through Claude, so the key never enters the chat):
- Windows (PowerShell): `setx PERPLEXITY_API_KEY "paste-key-here"`
- macOS (zsh): `echo 'export PERPLEXITY_API_KEY="paste-key-here"' >> ~/.zshrc`
- Linux (bash): `echo 'export PERPLEXITY_API_KEY="paste-key-here"' >> ~/.bashrc`

Then **fully restart Claude Code** (the desktop app or the terminal), because environment variables only reach programs started afterwards.
Verify with one cheap call (Perplexity: a short `perplexity_search`; nanobanana: `show_output_stats`; NotebookLM: `notebook_list`).

## Record
Write the result to the `connectors` row of `state/installation_status.md` (status `done` / `partial` and a note listing
what is enabled), e.g. by editing the row directly.

## Not listed here?
Search the registry (`mcp-registry` search/suggest tools, if available) or ask the user for the connector's URL, then follow the same steps.
Add a row to this file and, for a local server, an entry in `.mcp.json` with the key as `${VAR}`.
