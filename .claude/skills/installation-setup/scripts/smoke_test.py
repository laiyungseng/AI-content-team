#!/usr/bin/env python3
"""Offline end-to-end check that a fresh install works. No connectors or internet needed.

    uv run python smoke_test.py [--root <workspace>] [--keep]

Creates a throwaway project `zz_smoketest`, writes fake sources and fake actor output, then runs the real
pipeline scripts: run.py init -> normalise.py build -> build_report.py select -> build_report.py build.
Passes when report.html is built. The test project is deleted afterwards (in all six domains) unless --keep.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
PROJECT = "zz_smoketest"
DOMAINS = ["brand", "competitor_analysis/projects", "content_creation/projects", "memory", "performance", "state"]

SOURCES = """---
type: sources
status: active
---
# Sources

## Platforms
| Platform | Enabled | Max posts | Date range |
|---|---|---|---|
| meta | yes | 30 | 90d |
| instagram | yes | 30 | 90d |
| tiktok | yes | 30 | 90d |
| xhs | no | 20 | 90d |

## Topics

| Key | Label |
|---|---|

# Competitors

## Meta
| Name | URL | Profile or page | Active |
|---|---|---|---|
| Rival One | https://www.facebook.com/ads/library/?view_all_page_id=111 | page | yes |

## Instagram
| Name | URL | Profile or page | Active |
|---|---|---|---|
| rivalone | https://www.instagram.com/rivalone/ | profile | yes |
| privateco | https://www.instagram.com/privateco/ | profile | yes |

## TikTok
| Name | URL | Profile or page | Active |
|---|---|---|---|
| rivalone | https://www.tiktok.com/@rivalone | profile | yes |

## XHS
| Name | URL | Profile or page | Active |
|---|---|---|---|

# Ours

## Meta
| Name | URL | Profile or page | Active |
|---|---|---|---|

## Instagram
| Name | URL | Profile or page | Active |
|---|---|---|---|
| usbrand | https://www.instagram.com/usbrand/ | profile | yes |

## TikTok
| Name | URL | Profile or page | Active |
|---|---|---|---|

## XHS
| Name | URL | Profile or page | Active |
|---|---|---|---|
"""


def py(script: Path, *args: str) -> str:
    """Run a pipeline script with this interpreter; stop with its output on failure."""
    r = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"{script.name} {' '.join(args[:1])} failed:\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def cleanup(root: Path) -> None:
    for rel in DOMAINS:
        d = root / rel / PROJECT
        if d.exists():
            shutil.rmtree(d)


def fake_analysis(run: Path) -> None:
    """Stand-ins for the verdicts and comparison Claude writes in a real run."""
    sys.path.insert(0, str(SKILLS / "competitor-intelligence" / "scripts"))
    import build_report as br  # noqa: E402
    an = run / "analysis"
    ids = json.loads((an / "selected.json").read_text(encoding="utf-8"))["ids"]
    verdicts = {"items": [{"id": i, "verdict": "adapt", "reason": "Smoke test item."} for i in ids]}
    comp = {"headline": "Smoke test", "strategy": "n/a", "positioning": "n/a", "postCounts": {},
            "rows": [{"dimension": d, "stronger": "unclear", "ours": "", "theirs": ""} for d in br.DIMENSIONS]}
    (an / "verdicts.json").write_text(json.dumps(verdicts), encoding="utf-8")
    (an / "comparison.json").write_text(json.dumps(comp), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parents[3]))
    ap.add_argument("--keep", action="store_true", help="leave the test project for inspection")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    ci = SKILLS / "competitor-intelligence" / "scripts"
    cleanup(root)
    try:
        py(SKILLS / "business-onboarding" / "scripts" / "init_project.py", PROJECT, "--root", str(root))
        (root / "competitor_analysis" / "projects" / PROJECT / "sources.md").write_text(SOURCES, encoding="utf-8")
        run = Path(py(ci / "run.py", "init", PROJECT, "--root", str(root)).splitlines()[-1])
        py(ci / "make_test_fixtures.py", str(run))
        py(ci / "normalise.py", "build", str(run))
        py(ci / "build_report.py", "select", str(run))
        fake_analysis(run)
        print(py(ci / "build_report.py", "build", str(run)))
        if not (run / "report.html").exists():
            raise RuntimeError("report.html was not written")
        print("SMOKE TEST PASSED")
        return 0
    except Exception as e:  # report and fail, cleanup still runs
        print(f"SMOKE TEST FAILED: {e}")
        return 1
    finally:
        if not args.keep:
            cleanup(root)


if __name__ == "__main__":
    sys.exit(main())
