from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PwaDemoTest(unittest.TestCase):
    def test_root_manifest_is_installable_shape(self) -> None:
        manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["id"], "/app/")
        self.assertEqual(manifest["start_url"], "/app/")
        self.assertEqual(manifest["scope"], "/")
        self.assertEqual(manifest["display"], "standalone")
        self.assertIn("icons", manifest)
        self.assertIn("shortcuts", manifest)
        sizes = {icon["sizes"] for icon in manifest["icons"]}
        for size in ["48x48", "128x128", "192x192", "512x512"]:
            self.assertIn(size, sizes)

    def test_static_api_data_contains_three_profiles_and_datasets(self) -> None:
        data = json.loads((ROOT / "data" / "static-api-data.json").read_text(encoding="utf-8"))
        self.assertEqual(data["version"], "v55")
        self.assertEqual(len(data["profiles"]), 3)
        self.assertEqual(len(data["datasets"]), 3)
        self.assertEqual(len(data["scored"]), 3)
        self.assertGreaterEqual(len(data["scored"]["information_management"]["information_management"]["jobs"]), 30)
        self.assertGreaterEqual(len(data["scored"]["statistics"]["statistics"]["jobs"]), 20)
        self.assertGreaterEqual(len(data["scored"]["it_support"]["it_support"]["jobs"]), 20)

    def test_root_index_is_mode_selector(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Demo ansehen", html)
        self.assertIn("Werkzeug öffnen", html)
        self.assertIn('./demo/', html)
        self.assertIn('./app/', html)
        self.assertNotIn('demoBackdrop', html)

    def test_app_and_demo_routes_use_real_dashboard_shell(self) -> None:
        for route in ["app", "demo"]:
            html = (ROOT / route / "index.html").read_text(encoding="utf-8")
            self.assertIn("JobMeta Dashboard", html)
            self.assertIn("Demo-Daten laden", html)
            self.assertIn("demoBackdrop", html)
            self.assertIn("quick-actions", html)
            self.assertIn("Status und Notizen", html)
            self.assertIn('/static-api-shim.js', html)
            self.assertIn("Die feste Leiste am unteren Fensterrand scrollt die Tabelle horizontal", html)
            self.assertNotIn("Jobanzeigen als Metadaten analysieren", html)
            self.assertNotIn("jobmeta_demo_state_v48", html)
            self.assertNotIn("topPublicExportButton", html)
            self.assertNotIn("GitHub-Paket erstellen", html)

    def test_horizontal_scroll_uses_single_dock(self) -> None:
        html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
        self.assertIn("overflow-x: hidden", html)
        self.assertIn("height: 48px", html)
        self.assertIn("background: var(--bg)", html)
        self.assertIn("scrollbar-width: auto", html)

    def test_demo_mode_lock_is_released_after_loading(self) -> None:
        html = (ROOT / "demo" / "index.html").read_text(encoding="utf-8")
        self.assertIn("demo-choice-required", html)
        self.assertIn("setDemoChoiceLock(locked)", html)
        self.assertIn("enableDemoInteractionAfterLoad();", html)
        self.assertIn('shell.removeAttribute("inert")', html)
        self.assertIn('"topHarvestButton", "topImportButton", "topCvButton", "topProfileButton"', html)

    def test_static_api_shim_provides_local_api_endpoints(self) -> None:
        script = (ROOT / "static-api-shim.js").read_text(encoding="utf-8")
        for marker in ["/api/jobs", "/api/load-demo", "/api/analytics", "/api/export-csv", "jobmeta_static_demo_jobs_v55"]:
            self.assertIn(marker, script)

    def test_root_service_worker_references_core_assets_and_offline_fallback(self) -> None:
        service_worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
        for asset in ["./index.html", "./app/index.html", "./demo/index.html", "./offline.html", "./static-api-shim.js", "./data/static-api-data.json", "./manifest.webmanifest", "./assets/favicon.ico", "./assets/icon.svg", "./assets/icon-32.png", "./version.json"]:
            self.assertIn(asset, service_worker)
        self.assertIn("jobmeta-demo-v55", service_worker)
        self.assertIn("request.mode === 'navigate'", service_worker)

    def test_local_full_version_page_is_styled_and_useful(self) -> None:
        html = (ROOT / "local" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Lokale Vollversion", html)
        self.assertIn("python -m jobmeta_harvester --dashboard", html)
        self.assertIn("SQLite", html)
        self.assertIn("../app.css", html)

    def test_vercel_routes_root_app_demo_and_check(self) -> None:
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        rewrites = {(item["source"], item["destination"]) for item in config["rewrites"]}
        self.assertIn(("/", "/index.html"), rewrites)
        self.assertIn(("/app", "/app/index.html"), rewrites)
        self.assertIn(("/demo", "/demo/index.html"), rewrites)
        self.assertIn(("/demo/check", "/demo/check/index.html"), rewrites)
        self.assertIn(("/local", "/local/index.html"), rewrites)

    def test_vercelignore_excludes_private_and_local_files(self) -> None:
        ignore = (ROOT / ".vercelignore").read_text(encoding="utf-8")
        for pattern in ["*.sqlite", "config/profile.json", "dist/", "__pycache__/", "src/", "tests/"]:
            self.assertIn(pattern, ignore)

    def test_package_json_contains_pwa_build_script(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertIn("vercel-build", package["scripts"])
        self.assertIn("node --check static-api-shim.js", package["scripts"]["vercel-build"])

    def test_local_demo_check_no_longer_404s(self) -> None:
        self.assertTrue((ROOT / "demo" / "check" / "index.html").exists())
        version = json.loads((ROOT / "version.json").read_text(encoding="utf-8"))
        self.assertEqual(version["version"], "v55")
        self.assertEqual(version["route"], "/")
        self.assertEqual(version["demo_route"], "/demo/")
        self.assertEqual(version["app_route"], "/app/")

    def test_obsolete_separate_demo_files_removed(self) -> None:
        obsolete = [
            "app.js",
            "demo/app.js",
            "demo/app.css",
            "demo/manifest.webmanifest",
            "demo/service-worker.js",
            "demo/version.json",
            "demo/offline.html",
            "data/demo-data.json",
            "demo/data/demo-data.json",
            "demo/assets",
        ]
        for relative in obsolete:
            self.assertFalse((ROOT / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
