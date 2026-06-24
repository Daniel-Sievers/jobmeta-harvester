from __future__ import annotations

import json
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from browser_extension.build_extension_packages import build_package


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXTENSION_ROOT = PROJECT_ROOT / "browser_extension" / "jobmeta-clipper"


class BrowserExtensionTests(TestCase):
    def test_manifest_v3_and_required_files_exist(self) -> None:
        manifest = json.loads((EXTENSION_ROOT / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["manifest_version"], 3)
        self.assertEqual(manifest["action"]["default_popup"], "popup.html")
        self.assertIn("activeTab", manifest["permissions"])
        self.assertIn("scripting", manifest["permissions"])
        self.assertIn("http://127.0.0.1:8765/*", manifest["host_permissions"])
        self.assertTrue((EXTENSION_ROOT / "popup.html").exists())
        self.assertTrue((EXTENSION_ROOT / "popup.css").exists())
        self.assertTrue((EXTENSION_ROOT / "popup.js").exists())

    def test_firefox_manifest_has_gecko_settings(self) -> None:
        manifest = json.loads((EXTENSION_ROOT / "manifest.firefox.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["manifest_version"], 3)
        self.assertEqual(manifest["action"]["default_popup"], "popup.html")
        self.assertIn("browser_specific_settings", manifest)
        self.assertIn("gecko", manifest["browser_specific_settings"])
        self.assertIn("http://127.0.0.1:8765/*", manifest["host_permissions"])

    def test_extension_icons_exist(self) -> None:
        for size in (16, 32, 48, 128):
            icon = EXTENSION_ROOT / "icons" / f"icon-{size}.png"
            self.assertTrue(icon.exists(), f"Missing icon: {icon}")
            self.assertGreater(icon.stat().st_size, 100)

    def test_popup_uses_cross_browser_api_wrapper(self) -> None:
        popup_js = (EXTENSION_ROOT / "popup.js").read_text(encoding="utf-8")

        self.assertIn("globalThis.browser || globalThis.chrome", popup_js)
        self.assertIn("usesPromiseApi", popup_js)
        self.assertIn("extensionApi.scripting.executeScript", popup_js)
        self.assertIn("/api/manual-job", popup_js)
        self.assertIn("browser-extension, clipped", popup_js)
        self.assertIn("jobposting", popup_js)
        self.assertIn("Dashboard nicht erreichbar", popup_js)
        self.assertIn("inferSourceFromUrl", popup_js)
        self.assertIn("date_posted:", popup_js)

    def test_dashboard_allows_local_extension_cors(self) -> None:
        dashboard_py = (PROJECT_ROOT / "src" / "jobmeta_harvester" / "dashboard.py").read_text(encoding="utf-8")

        self.assertIn("def do_OPTIONS", dashboard_py)
        self.assertIn("Access-Control-Allow-Origin", dashboard_py)
        self.assertIn("Access-Control-Allow-Methods", dashboard_py)
        self.assertIn("Access-Control-Allow-Headers", dashboard_py)

    def test_extension_package_builder_creates_chromium_and_firefox_zips(self) -> None:
        with TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            chromium = build_package("chromium", output_dir)
            firefox = build_package("firefox", output_dir)

            self.assertTrue(chromium.exists())
            self.assertTrue(firefox.exists())

            with zipfile.ZipFile(chromium) as archive:
                manifest = json.loads(archive.read("manifest.json"))
                self.assertNotIn("browser_specific_settings", manifest)
                self.assertIn("popup.js", archive.namelist())

            with zipfile.ZipFile(firefox) as archive:
                manifest = json.loads(archive.read("manifest.json"))
                self.assertIn("browser_specific_settings", manifest)
                self.assertIn("popup.js", archive.namelist())

    def test_popup_has_dashboard_connection_button(self) -> None:
        popup_html = (EXTENSION_ROOT / "popup.html").read_text(encoding="utf-8")
        popup_js = (EXTENSION_ROOT / "popup.js").read_text(encoding="utf-8")

        self.assertIn('id="checkDashboard"', popup_html)
        self.assertIn("checkDashboardConnection", popup_js)
        self.assertIn("/api/jobs", popup_js)

    def test_popup_knows_common_job_sources(self) -> None:
        popup_js = (EXTENSION_ROOT / "popup.js").read_text(encoding="utf-8")

        for source in ("LinkedIn", "StepStone", "Indeed", "XING", "Remotive", "Workday", "Greenhouse"):
            self.assertIn(source, popup_js)
