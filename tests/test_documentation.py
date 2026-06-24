from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(TestCase):
    def test_browser_extension_workflow_doc_exists(self) -> None:
        doc = PROJECT_ROOT / "docs" / "browser_extension_workflow.md"

        self.assertTrue(doc.exists())
        text = doc.read_text(encoding="utf-8")
        self.assertIn("kein Plattform-Scraping", text)
        self.assertIn("aktuell geöffnete Seite", text)

    def test_readme_links_to_real_png_screenshots(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        screenshots = [
            "docs/assets/screenshots/01-dashboard-start.png",
            "docs/assets/screenshots/02-research-prompt.png",
            "docs/assets/screenshots/03-job-detail.png",
            "docs/assets/screenshots/04-fullscreen-ratings.png",
            "docs/assets/screenshots/05-reset-empty-state.png",
        ]

        for screenshot in screenshots:
            self.assertIn(screenshot, readme)
            self.assertTrue((PROJECT_ROOT / screenshot).exists(), f"Missing screenshot: {screenshot}")

        old_mockups = [
            "docs/assets/screenshots/dashboard-overview.svg",
            "docs/assets/screenshots/job-details.svg",
            "docs/assets/screenshots/public-export.svg",
            "docs/assets/screenshots/browser-extension-workflow.svg",
        ]
        for old_mockup in old_mockups:
            self.assertNotIn(old_mockup, readme)

    def test_markdown_links_in_readme_resolve_for_local_docs(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
        local_links = [link for link in links if not link.startswith(("http://", "https://", "#"))]

        self.assertTrue(local_links)
        for link in local_links:
            target = PROJECT_ROOT / link
            self.assertTrue(target.exists(), f"Missing README link target: {link}")

    def test_public_readme_is_not_generated_or_tracked(self) -> None:
        self.assertFalse((PROJECT_ROOT / "public" / "README.md").exists())
        build_script = (PROJECT_ROOT / "scripts" / "build_static_public.py").read_text(encoding="utf-8")
        self.assertNotIn('"README.md"', build_script)

    def test_browser_extension_workflow_doc_has_no_deleted_screenshot_link(self) -> None:
        doc = (PROJECT_ROOT / "docs" / "browser_extension_workflow.md").read_text(encoding="utf-8")
        self.assertNotIn("browser-extension-workflow.svg", doc)

    def test_public_readme_is_not_generated(self) -> None:
        # public/ is generated Vercel output. Keeping a second README there makes
        # GitHub show stale/broken screenshot links under /public/README.md.
        self.assertFalse((PROJECT_ROOT / "public" / "README.md").exists())

