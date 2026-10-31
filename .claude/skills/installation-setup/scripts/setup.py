#!/usr/bin/env python3
"""Cross-platform setup for the AI content team (Windows, macOS, Linux). Run through uv from the workspace root:

    uv run python .claude/skills/installation-setup/scripts/setup.py <command>

    check                      tool table + phase table -> state/installation_status.md (exit 1 if a required tool is missing)
    install <tool...> [--yes]  install tools with winget / brew / apt; asks per tool unless --yes (only after the user said yes)
    python [--media]           uv sync (core); --media adds yt-dlp + faster-whisper (large download)
    scaffold                   recreate missing base folders and _template files (never overwrites)
    smoke                      offline end-to-end pipeline test (smoke_test.py)
    all                        check -> python -> scaffold -> smoke, then list what still needs the user

Tools: uv, git (required); node (Perplexity connector runs via npx); ffmpeg (reels, with --media).
Python itself is managed by uv, so no system Python is needed.
"""
from __future__ import annotations

import datetime as dt
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STATUS = ROOT / "state" / "installation_status.md"
OS = {"Windows": "windows", "Darwin": "macos"}.get(platform.system(), "linux")

# name: (version args, required, why, {os: package id})
TOOLS = {
    "uv":     (["--version"], True,  "Python + libraries",            {"windows": "astral-sh.uv", "macos": "uv", "linux": None}),
    "git":    (["--version"], True,  "clone and update the project",  {"windows": "Git.Git", "macos": "git", "linux": "git"}),
    "node":   (["--version"], False, "Perplexity connector (npx)",    {"windows": "OpenJS.NodeJS.LTS", "macos": "node", "linux": "nodejs"}),
    "ffmpeg": (["-version"],  False, "reel audio (media group)",      {"windows": "Gyan.FFmpeg", "macos": "ffmpeg", "linux": "ffmpeg"}),
}
UV_SCRIPT = {"windows": 'powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"',
             "macos": "curl -LsSf https://astral.sh/uv/install.sh | sh", "linux": "curl -LsSf https://astral.sh/uv/install.sh | sh"}
PHASES = ["check", "tools", "python", "scaffold", "connectors", "smoke"]


def refresh_path() -> None:
    """Pick up PATH entries added by installers after this shell started (Windows keeps them in the registry)."""
    extra = [str(Path.home() / ".local" / "bin")]
    if OS == "windows":
        import winreg
        for hive, key in ((winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
                          (winreg.HKEY_CURRENT_USER, "Environment")):
            try:
                with winreg.OpenKey(hive, key) as k:
                    extra += os.path.expandvars(winreg.QueryValueEx(k, "Path")[0]).split(";")
            except OSError:
                pass
    else:
        extra += ["/opt/homebrew/bin", "/usr/local/bin"]
    os.environ["PATH"] = os.pathsep.join(dict.fromkeys(os.environ["PATH"].split(os.pathsep) + [p for p in extra if p]))


def version(name: str) -> str:
    exe = shutil.which(name)
    if not exe:
        return ""
    try:
        out = subprocess.run([exe, *TOOLS[name][0]], capture_output=True, text=True, timeout=20)
        return (out.stdout or out.stderr).strip().splitlines()[0][:60]
    except (OSError, subprocess.SubprocessError, IndexError):
        return "?"


# --------------------------------------------------------------------------- status file
def read_phases() -> dict[str, tuple[str, str, str]]:
    phases = {p: ("pending", "", "") for p in PHASES}
    if STATUS.exists():
        for m in re.finditer(r"^\| (\w+) \| (\w+) \| ([^|]*) \| ([^|]*) \|$", STATUS.read_text(encoding="utf-8"), re.M):
            if m.group(1) in phases:
                phases[m.group(1)] = (m.group(2), m.group(3).strip(), m.group(4).strip())
    return phases


def write_status(tools: dict[str, str], phases: dict[str, tuple[str, str, str]]) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    md = ["---", "type: status", f"checked: {now}", f"os: {OS}", "---", "# Installation status", "",
          "Written by `installation-setup/scripts/setup.py`. Re-run `setup.py all` to refresh.", "",
          "## Tools", "| Tool | Installed | Required | Version | Why |", "|---|---|---|---|---|"]
    for n, v in tools.items():
        md.append(f"| {n} | {'yes' if v else 'MISSING'} | {TOOLS[n][1]} | {v} | {TOOLS[n][2]} |")
    md += ["", "## Phases", "| Phase | Status | Checked | Note |", "|---|---|---|---|"]
    md += [f"| {p} | {s} | {c} | {n} |" for p, (s, c, n) in phases.items()]
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text("\n".join(md) + "\n", encoding="utf-8")


def mark(phase: str, status: str, note: str = "") -> None:
    phases = read_phases()
    phases[phase] = (status, dt.datetime.now().strftime("%Y-%m-%d %H:%M"), note.replace("|", "/")[:120])
    write_status({n: version(n) for n in TOOLS}, phases)


# --------------------------------------------------------------------------- commands
def check() -> int:
    refresh_path()
    tools = {n: version(n) for n in TOOLS}
    print(f"OS: {OS}")
    for n, v in tools.items():
        print(f"  {n:7} {'ok  ' if v else 'MISSING'}  {'required' if TOOLS[n][1] else 'optional'}  {v or TOOLS[n][2]}")
    missing = [n for n, v in tools.items() if not v and TOOLS[n][1]]
    optional = [n for n, v in tools.items() if not v and not TOOLS[n][1]]
    phases = read_phases()
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    phases["check"] = ("done" if not missing else "failed", stamp, f"missing: {', '.join(missing)}" if missing else "")
    phases["tools"] = ("done" if not missing and not optional else "partial" if not missing else "failed", stamp,
                       f"optional missing: {', '.join(optional)}" if optional else "")
    write_status(tools, phases)
    if missing:
        print(f"MISSING required: {', '.join(missing)}  ->  setup.py install {' '.join(missing)}")
    return 1 if missing else 0


def install(names: list[str], yes: bool) -> int:
    refresh_path()
    failed = []
    for n in names:
        if n not in TOOLS:
            print(f"Unknown tool: {n} (known: {', '.join(TOOLS)})"); failed.append(n); continue
        if shutil.which(n):
            print(f"{n} already installed."); continue
        pkg = TOOLS[n][3][OS]
        if OS == "windows" and shutil.which("winget"):
            cmd = f"winget install --id {pkg} -e --accept-package-agreements --accept-source-agreements"
        elif OS == "macos" and shutil.which("brew"):
            cmd = f"brew install {pkg}"
        elif OS == "linux" and pkg and shutil.which("apt-get"):
            cmd = f"sudo apt-get install -y {pkg}"
        elif n == "uv":
            cmd = UV_SCRIPT[OS]
        else:
            print(f"No package manager found for {n}. See references/manual_install.md"); failed.append(n); continue
        if not yes and input(f"Install {n} with: {cmd} ? [y/N] ").strip().lower() not in ("y", "yes"):
            print(f"Skipped {n}."); continue
        print(f"> {cmd}")
        if subprocess.run(cmd, shell=True).returncode != 0:
            failed.append(n)
    refresh_path()
    check()
    if failed:
        print(f"Not installed: {', '.join(failed)}")
    print("If a tool still shows MISSING, open a new terminal (PATH changes reach new shells only) and run check again.")
    return 1 if failed else 0


def python_libs(media: bool) -> int:
    cmd = ["uv", "sync"] + (["--group", "media"] if media else [])
    ok = subprocess.run(cmd, cwd=ROOT).returncode == 0
    if ok:
        ok = subprocess.run([sys.executable, "-c", "import yaml, frontmatter, jinja2, pandas, PIL"]).returncode == 0
    mark("python", "done" if ok else "failed", "core + media" if media and ok else "core" if ok else "uv sync or import failed")
    return 0 if ok else 1


def scaffold() -> int:
    r = subprocess.run([sys.executable, str(HERE / "scaffold_workspace.py"), "--root", str(ROOT)])
    mark("scaffold", "done" if r.returncode == 0 else "failed")
    return r.returncode


def smoke() -> int:
    r = subprocess.run([sys.executable, str(HERE / "smoke_test.py"), "--root", str(ROOT)])
    mark("smoke", "done" if r.returncode == 0 else "failed", "" if r.returncode == 0 else "see smoke_test.py output")
    return r.returncode


def run_all() -> int:
    steps = [("check", check), ("python", lambda: python_libs(False)), ("scaffold", scaffold), ("smoke", smoke)]
    results = {}
    for name, fn in steps:
        print(f"\n=== {name} ===")
        results[name] = fn()
        if name == "check" and results[name]:
            print("Install the required tools first, then run `setup.py all` again.")
            return 1
    print("\n=== summary ===")
    for name, rc in results.items():
        print(f"  {name:9} {'ok' if rc == 0 else 'FAILED'}")
    optional = [n for n in TOOLS if not TOOLS[n][1] and not shutil.which(n)]
    if optional:
        print(f"  optional tools missing: {', '.join(optional)}  ->  setup.py install {' '.join(optional)}")
    print("  connectors: open Claude Code in this folder and say 'set up the connectors' (see references/connectors.md)")
    return 0 if all(rc == 0 for rc in results.values()) else 1


def main() -> int:
    sys.stdout.reconfigure(line_buffering=True)  # keep our lines in order with child-process output
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 1
    cmd, rest = args[0], args[1:]
    if cmd == "check":
        return check()
    if cmd == "install":
        return install([a for a in rest if not a.startswith("--")], "--yes" in rest)
    if cmd == "python":
        return python_libs("--media" in rest)
    if cmd == "scaffold":
        return scaffold()
    if cmd == "smoke":
        return smoke()
    if cmd == "all":
        return run_all()
    print(__doc__); return 1


if __name__ == "__main__":
    sys.exit(main())
