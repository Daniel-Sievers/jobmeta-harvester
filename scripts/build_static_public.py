from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

FILES = [
    "index.html",
    "app.css",
    "manifest.webmanifest",
    "service-worker.js",
    "offline.html",
    "version.json",
    "static-api-shim.js",
    "README.md",
]
DIRS = ["app", "demo", "local", "assets", "data"]


def copy_file(src_rel: str) -> None:
    src = ROOT / src_rel
    dest = PUBLIC / src_rel
    if not src.exists():
        raise SystemExit(f"missing static file: {src_rel}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_dir(src_rel: str) -> None:
    src = ROOT / src_rel
    dest = PUBLIC / src_rel
    if not src.exists():
        raise SystemExit(f"missing static directory: {src_rel}")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main() -> int:
    # Keep /demo/ on the exact same dashboard shell as /app/.
    app_index = ROOT / "app" / "index.html"
    demo_index = ROOT / "demo" / "index.html"
    if app_index.exists():
        demo_index.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(app_index, demo_index)

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    for rel in FILES:
        copy_file(rel)
    for rel in DIRS:
        copy_dir(rel)

    favicon = ROOT / "assets" / "favicon.ico"
    if favicon.exists():
        shutil.copy2(favicon, PUBLIC / "favicon.ico")

    print("Vercel static output prepared in public/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
