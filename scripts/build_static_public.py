from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

# public/ ist reiner Build-Output fuer Vercel und wird nicht versioniert.
# Die Dashboard-Oberflaeche hat eine Quelle: app/index.html.
FILES = [
    "index.html",
    "app.css",
    "manifest.webmanifest",
    "service-worker.js",
    "offline.html",
    "version.json",
    "static-api-shim.js",
]
DIRS = ["app", "local", "assets", "data"]


def copy_file(src_rel: str, dest_rel: str | None = None) -> None:
    src = ROOT / src_rel
    dest = PUBLIC / (dest_rel or src_rel)
    if not src.exists():
        raise SystemExit(f"missing static file: {src_rel}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_dir(src_rel: str, dest_rel: str | None = None) -> None:
    src = ROOT / src_rel
    dest = PUBLIC / (dest_rel or src_rel)
    if not src.exists():
        raise SystemExit(f"missing static directory: {src_rel}")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def main() -> int:
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    for rel in FILES:
        copy_file(rel)
    for rel in DIRS:
        copy_dir(rel)

    # /demo/ nutzt dieselbe Dashboard-Shell wie /app/; nur der URL-Modus unterscheidet sich.
    copy_file("app/index.html", "demo/index.html")
    copy_dir("demo/check", "demo/check")

    favicon = ROOT / "assets" / "favicon.ico"
    if favicon.exists():
        shutil.copy2(favicon, PUBLIC / "favicon.ico")

    print("Vercel static output prepared in public/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
