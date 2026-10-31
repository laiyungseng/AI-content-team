# AI Content Team

A Claude-driven content intelligence and production system. It researches your competitors, finds what works, and
(later phases) plans and writes content for you. This folder is also an Obsidian vault.

---

## Install (new PC, from scratch)

Works on **Windows, macOS and Linux**. It takes about 10 minutes, most of it waiting for downloads.
You do not need to install Python yourself; the setup handles it.

### What you need
- A Claude account with Claude Code access (Pro, Max, Team or Enterprise).
- Access to this GitHub repository (it is private: ask the owner to add your GitHub account).
- Internet.

### Step 1: Install Claude Code
Pick one:
- **Desktop app (easiest):** download from https://claude.ai/download, install, sign in, open the **Code** tab.
- **Terminal:**
  - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
  - macOS / Linux: `curl -fsSL https://claude.ai/install.sh | bash`

  Then type `claude` and sign in.

### Step 2: Install git
Check first by opening a terminal and typing `git --version`. If you see a version number, skip this step.
- Windows: `winget install --id Git.Git -e` (or download from https://git-scm.com/download/win)
- macOS: `xcode-select --install`
- Linux: `sudo apt-get install -y git`

Close the terminal and open a new one afterwards.

> Windows only, recommended once: `git config --global core.longpaths true` (avoids "Filename too long" errors in deep folders).

### Step 3: Download the project
In a terminal, go to the folder you want the project in (for example `cd D:\program`), then:

```bash
git clone https://github.com/laiyungseng/AI-content-team.git
```

```bash
cd AI-content-team
```

The first time, git asks you to sign in to GitHub (a browser window opens on Windows). On macOS/Linux, if it asks for a
password, use a GitHub personal access token or sign in with the GitHub CLI (`gh auth login`).

### Step 4: Run the setup
Still inside the project folder:
- **Windows:** `powershell -ExecutionPolicy Bypass -File setup.ps1`
- **macOS / Linux:** `sh setup.sh`

This installs `uv` (the Python manager) if needed, downloads Python and the libraries, checks the folders, and runs a
**smoke test** (a full offline test run on fake data). You should finish with:

```
SMOKE TEST PASSED
=== summary ===
  check     ok
  python    ok
  scaffold  ok
  smoke     ok
```

If `check` says a required tool is missing, run the command it prints (for example
`uv run python .claude/skills/installation-setup/scripts/setup.py install git`) and then run the setup again.

**Shortcut:** you can skip typing these commands. Open the folder in Claude Code and say **"set up this project"**;
Claude follows the same steps (the `installation-setup` skill) and asks before installing anything.

### Step 5: Open the project in Claude Code
- Desktop app: Code tab, choose the `AI-content-team` folder.
- Terminal: `cd AI-content-team`, then `claude`.

Claude Code asks once whether to trust the folder and whether to enable the project's MCP servers (`.mcp.json`).
Say yes to both.

### Step 6: Connect the services
Tell Claude **"set up the connectors"** and say what you want to do first. You only need the ones for your goal:

| Goal | Connectors |
|---|---|
| Research competitors (start here) | Apify, Perplexity |
| Make images for posts | + nanobanana (Gemini) |
| Schedule and publish | + Zernio |

There are two kinds:
- **Account connectors** (Apify, Zernio, Notion, Figma) belong to your Claude account. If you already use them on another PC,
  they come with your login. Otherwise add them in the desktop app under **Settings > Connectors**, or run `/mcp` in the terminal.
- **API-key connectors** (Perplexity, nanobanana) read their key from your computer. Set the key **yourself** in a terminal
  (never paste keys into the Claude chat):
  - Windows: `setx PERPLEXITY_API_KEY "your-key"` and `setx GEMINI_API_KEY "your-key"`
  - macOS: `echo 'export PERPLEXITY_API_KEY="your-key"' >> ~/.zshrc` (same for `GEMINI_API_KEY`)

  Get keys at perplexity.ai (Settings > API) and aistudio.google.com (Get API key). Then **fully close and reopen Claude Code**.
- NotebookLM (optional) needs a one-time sign-in: `uvx --from notebooklm-mcp-cli nlm login`.

### Step 7: First run
In Claude Code, say:
1. **"show my sources"**: add your competitors' and your own Instagram / TikTok / Meta Ad Library / XHS links.
2. **"research competitors"**: collects their posts and builds a 2-page report for you to approve.

When you are ready to make content, say **"set up my business"** (creates your brand guideline).

### Troubleshooting
| Problem | Fix |
|---|---|
| `uv` or `git` "not recognized" right after installing | Close the terminal and open a new one, then run the setup again |
| "Filename too long" during clone (Windows) | `git config --global core.longpaths true`, delete the folder, clone again |
| "running scripts is disabled" (Windows) | Use the exact command in Step 4 (it includes `-ExecutionPolicy Bypass`) |
| `SMOKE TEST FAILED` | Copy the output into Claude Code and say "the setup smoke test failed" |
| Perplexity / nanobanana tools missing | Check the key is set (`echo $env:PERPLEXITY_API_KEY` on Windows), then fully restart Claude Code |
| Check the status any time | `uv run python .claude/skills/installation-setup/scripts/setup.py check`, or read `state/installation_status.md` |

### Update to the latest version
```bash
git pull
```
Then run the Step 4 command again (safe to repeat; nothing is overwritten).

### For Claude (AI setup instructions)
Follow `.claude/skills/installation-setup/SKILL.md`. All install logic is in
`.claude/skills/installation-setup/scripts/setup.py` (`check` / `install` / `python` / `scaffold` / `smoke` / `all`);
connector steps are in `references/connectors.md`. Ask before installing anything and never ask for keys in chat.

---

## What is in the repo (and what is not)
Shared through git: skills, agents, templates, shared frameworks, `memory/_system` (how the skills perform), docs.
**Kept local only:** your projects' brand files, research runs, memory and state (see `.gitignore`), so client data never
reaches GitHub. Back those up separately.

## Skills (`.claude/skills/`)
| Skill | What it does |
|---|---|
| `installation-setup` | Sets up any PC: tools, Python, folders, smoke test, connectors |
| `source-manager` | Edit the list of competitor and own accounts to research |
| `competitor-intelligence` | Research run: collect, compare, Adapt / Copy / Ignore, 2-page report |
| `business-onboarding` | Studies your business, interviews you, writes `brand/[project]/` |
| `artifact-presentation-setup` | Interactive Claude Artifact pages to present output and collect approval |

## Layout
See `CLAUDE.md` for the full map. Short version: `agents/` (who), `.claude/skills/` (how), `brand/` (identity),
`competitor_analysis/` and `content_creation/` (work), `memory/` (lessons), `performance/`, `state/`, `shared/`.

## Roadmap
1. Intelligence MVP  2. Strategy engine  3. Content generation  4. Obsidian dashboards  5. Performance loop  6. Publishing automation.
Agents and methodology files for later phases are stubs until their phase.
