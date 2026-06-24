from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
REQUIRED = [
    "index.html",
    "app/index.html",
    "demo/index.html",
    "demo/check/index.html",
    "local/index.html",
    "app.css",
    "static-api-shim.js",
    "manifest.webmanifest",
    "service-worker.js",
    "offline.html",
    "version.json",
    "favicon.ico",
    "assets/icon-192.png",
    "assets/icon-512.png",
    "data/static-api-data.json",
]


def fail(message: str) -> None:
    print(f"Vercel public check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not PUBLIC.exists():
        fail("public/ does not exist; run python scripts/build_static_public.py first")
    missing = [rel for rel in REQUIRED if not (PUBLIC / rel).exists()]
    if missing:
        fail("missing files in public/: " + ", ".join(missing))
    if (PUBLIC / "README.md").exists():
        fail("public/README.md should not exist; README belongs only to the repository root")
    html = (PUBLIC / "demo" / "index.html").read_text(encoding="utf-8")
    if "/static-api-shim.js" not in html or "JobMeta Dashboard" not in html:
        fail("public/demo/index.html does not contain the shared dashboard shell")
    print("Vercel public output: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
