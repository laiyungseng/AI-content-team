# Manual install fallbacks (no winget / Homebrew / apt)

| Tool | Windows | macOS | Linux | Verify |
|---|---|---|---|---|
| uv | `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 \| iex"` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | same as macOS | `uv --version` |
| git | https://git-scm.com/download/win | `xcode-select --install` | distro package manager | `git --version` |
| node | https://nodejs.org (LTS installer) | https://nodejs.org (LTS .pkg) | https://nodejs.org or nvm | `node --version` |
| ffmpeg | https://www.gyan.dev/ffmpeg/builds/ (release essentials zip), unzip, add `bin` to PATH | https://evermeet.cx/ffmpeg/ | distro package manager | `ffmpeg -version` |
| Homebrew (macOS) | - | https://brew.sh (one-line installer) | - | `brew --version` |
| winget (Windows) | "App Installer" from the Microsoft Store | - | - | `winget --version` |

Python does not need a separate install: `uv` downloads the version `pyproject.toml` asks for.
After editing PATH, open a new terminal (or restart Claude Code) before verifying.
