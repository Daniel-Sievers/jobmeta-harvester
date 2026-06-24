from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path
from unittest import TestCase

from src.jobmeta_harvester.public_export import create_public_export


class PublicExportTests(TestCase):
    def test_public_export_excludes_private_and_generated_files(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "public.zip"

            result = create_public_export(project_root, output_path)

            self.assertTrue(result.zip_path.exists())
            with zipfile.ZipFile(result.zip_path) as archive:
                names = archive.namelist()

            root = f"{project_root.name}-public"
            self.assertIn(f"{root}/config/profile.json", names)
            self.assertIn(f"{root}/config/profile.example.json", names)
            self.assertIn(f"{root}/PUBLIC_EXPORT_CHECKLIST.md", names)
            self.assertIn(f"{root}/data/.gitkeep", names)
            self.assertFalse(any(name.endswith(".sqlite") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".pyc") for name in names))
            self.assertFalse(any("/dist/" in name for name in names))

    def test_public_export_uses_neutral_profile(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "public.zip"

            result = create_public_export(project_root, output_path)

            with zipfile.ZipFile(result.zip_path) as archive:
                root = f"{project_root.name}-public"
                profile_text = archive.read(f"{root}/config/profile.json").decode("utf-8")

            self.assertIn("Example information management profile", profile_text)
            self.assertIn("example_profile", profile_text)
