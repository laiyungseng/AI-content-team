#!/usr/bin/env python3
"""
Carousel HTML — Render Script
读 work_dir/config.json → 套 layout templates → 注入 brand kit → Chrome headless 截图 → 出 1080x1350 PNG

Usage:
    python3 render.py --work-dir content_creation/projects/demo/drafts/C001
    # config.json + brand-kit slug 都在 work_dir 里指定，brand-kit 文件从 carousel_render/assets/brand-kits/ 读
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent  # carousel_render/
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
BRAND_KITS_DIR = SKILL_DIR / "assets" / "brand-kits"
BASE_CSS_PATH = TEMPLATES_DIR / "_base.css"

CHROME_PATHS = [
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    # Linux
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    # Windows（Git Bash / WSL 都吃得到这些路径）
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/c/Program Files/Google/Chrome/Application/chrome.exe",
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
]


def find_chrome():
    # 1) 环境变量优先（Chrome 装在非标准位置时，设置 CHROME_PATH）
    env_chrome = os.environ.get("CHROME_PATH", "").strip()
    if env_chrome and Path(env_chrome).exists():
        return env_chrome

    # 2) 常见安装位置
    for p in CHROME_PATHS:
        if Path(p).exists():
            return p

    # 3) PATH 里找得到就用
    for name in ("google-chrome", "chromium", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found

    print(
        "[ERROR] 找不到 Chrome。这个 skill 需要 Chrome 来把网页截成图片。\n"
        "        装一个 Chrome（https://www.google.com/chrome/）之后再跑一次，\n"
        "        或设置环境变量 CHROME_PATH 指向 chrome.exe。",
        file=sys.stderr,
    )
    sys.exit(1)


def load_brand_kit(slug: str) -> dict:
    """Load brand kit JSON by slug."""
    path = BRAND_KITS_DIR / f"{slug}.json"
    if not path.exists():
        print(f"[ERROR] Brand kit not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def render_base_css(brand_kit: dict) -> str:
    """Substitute brand kit values into _base.css."""
    css = BASE_CSS_PATH.read_text(encoding="utf-8")
    colors = brand_kit["colors"]
    fonts = brand_kit["fonts"]
    replacements = {
        "{{BRAND_PRIMARY}}": colors["primary"],
        "{{BRAND_DARK}}": colors["dark"],
        "{{BRAND_LIGHT}}": colors["light"],
        "{{BRAND_BODY}}": colors.get("body", "#2A2A2A"),
        "{{BRAND_MUTED}}": colors.get("muted", "#6B7280"),
        "{{BRAND_WATERMARK}}": colors.get("watermark", colors["light"]),
        "{{BRAND_PILL_FILL}}": colors.get("pill_fill", colors["light"]),
        "{{FONT_SANS}}": fonts["sans"],
        "{{FONT_SERIF}}": fonts.get("serif", fonts["sans"]),
    }
    for k, v in replacements.items():
        css = css.replace(k, v)
    return css


def embed_image_base64(image_path: str) -> str:
    """Read user image → return data: URI."""
    p = Path(image_path)
    if not p.exists():
        print(f"[WARN] Image not found, skipping: {image_path}", file=sys.stderr)
        return ""
    raw = p.read_bytes()
    ext = p.suffix.lower().lstrip(".")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime = mime_map.get(ext, "image/jpeg")
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def render_page(layout: str, slots: dict, base_css: str, brand_kit: dict) -> str:
    """Read layout template → substitute base CSS + slots → return final HTML."""
    template_path = TEMPLATES_DIR / f"{layout}.html"
    if not template_path.exists():
        # Try with .html extension if missing
        alt = TEMPLATES_DIR / f"{layout}"
        if alt.exists():
            template_path = alt
        else:
            print(f"[ERROR] Template not found: {template_path}", file=sys.stderr)
            sys.exit(1)
    html = template_path.read_text(encoding="utf-8")

    # Inject base CSS into placeholder
    html = html.replace("{{BASE_CSS}}", base_css)

    # Brand kit derived slots (always available to every template)
    brand_slots = {
        "HANDLE": brand_kit.get("handle", "@brand"),
        "BRAND_NAME": brand_kit.get("name", "Brand"),
        "TAGLINE": brand_kit.get("tagline", ""),
        "SLOGAN_FOOTER": brand_kit.get("slogan_footer", brand_kit.get("tagline", "")),
    }

    # Merge slots (page-specific overrides brand defaults)
    all_slots = {**brand_slots, **slots}

    # Handle IMAGE_PATH special case → base64
    if "IMAGE_PATH" in all_slots and all_slots["IMAGE_PATH"]:
        all_slots["IMAGE_DATA"] = embed_image_base64(all_slots["IMAGE_PATH"])

    # Replace all {{KEY}} with values
    def replace_placeholder(m):
        key = m.group(1).strip()
        return str(all_slots.get(key, ""))

    html = re.sub(r"\{\{\s*([A-Z_][A-Z0-9_]*)\s*\}\}", replace_placeholder, html)

    # Post-process: remove empty list items (checklist/step/stat)
    html = cleanup_empty_items(html)

    return html


def cleanup_empty_items(html: str) -> str:
    """Remove empty .item / .step / .stat blocks left by un-filled slots."""
    patterns = [
        # 05-checklist empty item (check + empty text + empty note span)
        r'<div class="item"><div class="check">[^<]+</div><div class="text">\s*<span class="note">\s*</span>\s*</div></div>\s*',
        # 04-numbered-step empty step (num + empty title + empty desc)
        r'<div class="step"><div class="num">[^<]+</div><div><div class="s-title">\s*</div><div class="s-desc">\s*</div></div></div>\s*',
        # 06-stat-cards empty stat (empty num + empty label)
        r'<div class="stat"><div class="stat-num">\s*</div><div class="stat-label">\s*</div></div>\s*',
    ]
    for pat in patterns:
        html = re.sub(pat, '', html)
    return html


def screenshot_html(chrome: str, html_path: Path, png_path: Path):
    """Use Chrome headless to screenshot HTML → PNG at 1080x1350."""
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1080,1350",
        "--default-background-color=00000000",
        f"--screenshot={png_path}",
        "--virtual-time-budget=5000",
        f"file://{html_path.resolve()}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if not png_path.exists():
        print(f"[ERROR] Screenshot failed for {html_path.name}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False
    return True


def main():
    # Windows consoles default to cp1252 and crash on the arrow / Chinese text below
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Render carousel HTML → PNG batch")
    ap.add_argument("--work-dir", required=True, help="Work directory containing config.json")
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    config_path = work_dir / "config.json"
    if not config_path.exists():
        print(f"[ERROR] Missing config.json in {work_dir}", file=sys.stderr)
        sys.exit(1)

    config = json.loads(config_path.read_text(encoding="utf-8"))
    brand_kit_slug = config.get("brand_kit")
    if not brand_kit_slug:
        print("[ERROR] config.json must specify 'brand_kit'", file=sys.stderr)
        sys.exit(1)

    brand_kit = load_brand_kit(brand_kit_slug)
    base_css = render_base_css(brand_kit)
    chrome = find_chrome()

    pages = config.get("pages", [])
    if not pages:
        print("[ERROR] config.json has no 'pages'", file=sys.stderr)
        sys.exit(1)

    total = len(pages)
    rendered = []
    for i, page in enumerate(pages, start=1):
        layout = page.get("layout")
        slots = page.get("slots", {})
        # Auto-inject page numbering if not provided
        slots.setdefault("PAGE_NUM", f"{i:02d} / {total:02d}")

        html = render_page(layout, slots, base_css, brand_kit)
        html_path = work_dir / f"page{i}.html"
        html_path.write_text(html, encoding="utf-8")

        png_path = work_dir / f"page{i}.png"
        ok = screenshot_html(chrome, html_path, png_path)
        if ok:
            size_kb = png_path.stat().st_size // 1024
            print(f"[OK] page{i} ({layout}) → {png_path.name} ({size_kb} KB)")
            rendered.append(str(png_path))
        else:
            print(f"[FAIL] page{i} ({layout})")

    print(f"\nDone: {len(rendered)}/{total} pages rendered")
    print(f"Output dir: {work_dir}")


if __name__ == "__main__":
    main()
