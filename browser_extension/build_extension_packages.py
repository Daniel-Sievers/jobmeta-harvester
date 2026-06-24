from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXTENSION_ROOT = PROJECT_ROOT / "browser_extension" / "jobmeta-clipper"
DIST_ROOT = PROJECT_ROOT / "dist" / "browser_extension"
COMMON_FILES = [
    "popup.html",
    "popup.css",
    "popup.js",
    "icons/icon-16.png",
    "icons/icon-32.png",
    "icons/icon-48.png",
    "icons/icon-128.png",
]

TARGETS = {
    "chromium": {
        "manifest": "manifest.chromium.json",
        "zip_name": "jobmeta-clipper-chromium.zip",
    },
    "firefox": {
        "manifest": "manifest.firefox.json",
        "zip_name": "jobmeta-clipper-firefox.zip",
    },
}


def build_package(target: str, output_dir: Path) -> Path:
    if target not in TARGETS:
        raise ValueError(f"Unknown target: {target}")
    config = TARGETS[target]
    output_dir.mkdir(parents=True, exist_ok=True)
    package_path = output_dir / config["zip_name"]
    if package_path.exists():
        package_path.unlink()

    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(EXTENSION_ROOT / config["manifest"], "manifest.json")
        for relative in COMMON_FILES:
            source = EXTENSION_ROOT / relative
            archive.write(source, relative)
    return package_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build JobMeta Clipper extension packages.")
    parser.add_argument("--target", choices=["chromium", "firefox", "all"], default="all")
    parser.add_argument("--output-dir", type=Path, default=DIST_ROOT)
    args = parser.parse_args()

    targets = list(TARGETS) if args.target == "all" else [args.target]
    for target in targets:
        package = build_package(target, args.output_dir)
        print(package)


if __name__ == "__main__":
    main()
