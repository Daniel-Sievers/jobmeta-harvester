from __future__ import annotations

import unittest

from src.jobmeta_harvester.dashboard import (
    DASHBOARD_HTML,
    DASHBOARD_MANIFEST,
    DASHBOARD_OFFLINE_HTML,
    DASHBOARD_SERVICE_WORKER,
)


class DashboardPwaTest(unittest.TestCase):
    def test_dashboard_html_exposes_pwa_manifest_and_service_worker(self) -> None:
        self.assertIn('rel="manifest" href="/manifest.webmanifest"', DASHBOARD_HTML)
        self.assertIn('navigator.serviceWorker.register("/service-worker.js")', DASHBOARD_HTML)
        self.assertIn('name="theme-color" content="#2f6f5e"', DASHBOARD_HTML)
        self.assertIn('href="/favicon.ico"', DASHBOARD_HTML)
        self.assertIn('href="/assets/icon.svg"', DASHBOARD_HTML)

    def test_dashboard_manifest_is_installable_shape(self) -> None:
        self.assertEqual(DASHBOARD_MANIFEST["id"], "/")
        self.assertEqual(DASHBOARD_MANIFEST["start_url"], "/")
        self.assertEqual(DASHBOARD_MANIFEST["scope"], "/")
        self.assertEqual(DASHBOARD_MANIFEST["display"], "standalone")
        sizes = {icon["sizes"] for icon in DASHBOARD_MANIFEST["icons"]}
        self.assertIn("192x192", sizes)
        self.assertIn("512x512", sizes)
        self.assertIn("48x48", sizes)
        self.assertIn("128x128", sizes)

    def test_dashboard_service_worker_uses_dashboard_assets_not_separate_demo(self) -> None:
        self.assertIn("jobmeta-dashboard-v55", DASHBOARD_SERVICE_WORKER)
        self.assertIn("/manifest.webmanifest", DASHBOARD_SERVICE_WORKER)
        self.assertIn("/offline.html", DASHBOARD_SERVICE_WORKER)
        self.assertIn("/favicon.ico", DASHBOARD_SERVICE_WORKER)
        self.assertIn("/assets/icon.svg", DASHBOARD_SERVICE_WORKER)
        self.assertIn("url.pathname.startsWith('/api/')", DASHBOARD_SERVICE_WORKER)

    def test_dashboard_offline_page_explains_local_server(self) -> None:
        self.assertIn("JobMeta ist gerade offline", DASHBOARD_OFFLINE_HTML)
        self.assertIn("python -m jobmeta_harvester --dashboard", DASHBOARD_OFFLINE_HTML)

    def test_dashboard_normal_toolbar_has_no_public_export_button(self) -> None:
        self.assertNotIn("topPublicExportButton", DASHBOARD_HTML)
        self.assertNotIn("GitHub-Paket erstellen", DASHBOARD_HTML)
        self.assertIn("overflow-x: hidden", DASHBOARD_HTML)
        self.assertIn("height: 48px", DASHBOARD_HTML)


if __name__ == "__main__":
    unittest.main()
