from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import TestCase

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(TestCase):
    def test_browser_extension_workflow_doc_and_mockup_exist(self) -> None:
        doc = PROJECT_ROOT / "docs" / "browser_extension_workflow.md"
        svg = PROJECT_ROOT / "docs" / "assets" / "screenshots" / "browser-extension-workflow.svg"

        self.assertTrue(doc.exists())
        self.assertTrue(svg.exists())
        text = doc.read_text(encoding="utf-8")
        self.assertIn("kein Plattform-Scraping", text)
        self.assertIn("aktuell geöffnete Seite", text)
        ET.parse(svg)

    def test_readme_links_to_extension_workflow_assets(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/browser_extension_workflow.md", readme)
        self.assertIn("docs/assets/screenshots/browser-extension-workflow.svg", readme)
        self.assertIn("Browser-Clipper", readme)

    def test_markdown_links_in_readme_resolve_for_local_docs(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
        local_links = [link for link in links if not link.startswith(("http://", "https://", "#"))]

        self.assertTrue(local_links)
        for link in local_links:
            target = PROJECT_ROOT / link
            self.assertTrue(target.exists(), f"Missing README link target: {link}")
