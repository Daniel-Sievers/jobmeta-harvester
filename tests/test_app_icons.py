from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


class AppIconAssetsTest(unittest.TestCase):
    def test_pwa_icon_assets_exist_in_single_shared_assets_folder(self) -> None:
        for name in [
            "favicon.ico",
            "icon.svg",
            "icon-16.png",
            "icon-32.png",
            "icon-48.png",
            "icon-128.png",
            "icon-192.png",
            "icon-512.png",
        ]:
            path = ASSETS / name
            self.assertTrue(path.exists(), f"Missing app icon asset: {path}")
            self.assertGreater(path.stat().st_size, 100)

    def test_duplicated_demo_assets_folder_removed(self) -> None:
        self.assertFalse((ROOT / "demo" / "assets").exists())


if __name__ == "__main__":
    unittest.main()
