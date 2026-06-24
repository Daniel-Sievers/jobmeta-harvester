from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path
from unittest import TestCase

from src.jobmeta_harvester.database import import_jobs_csv, list_jobs
from src.jobmeta_harvester.profile_builder import build_profile_from_cv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DemoAssetsTests(TestCase):
    def test_sample_jobs_are_valid_demo_records(self) -> None:
        sample_path = PROJECT_ROOT / "examples" / "sample_jobs.json"
        rows = json.loads(sample_path.read_text(encoding="utf-8"))

        self.assertGreaterEqual(len(rows), 8)
        for row in rows:
            self.assertTrue(row["title"])
            self.assertTrue(row["company"])
            self.assertTrue(row["url"].startswith("https://example.org/jobs/"))
            self.assertIsInstance(row["tags"], list)

    def test_demo_jobmeta_csv_imports_into_sqlite(self) -> None:
        csv_path = PROJECT_ROOT / "examples" / "demo_jobmeta_import.csv"
        profile_path = PROJECT_ROOT / "config" / "profile.example.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "jobs.sqlite"
            stats = import_jobs_csv(csv_path, profile, db_path)
            jobs = list_jobs(db_path)

        self.assertEqual(stats["incoming"], 8)
        self.assertEqual(stats["new"], 8)
        self.assertEqual(len(jobs), 8)
        self.assertTrue(any(job["priority"] == "hoch" for job in jobs))
        self.assertTrue(any(job["gap_blocking"] for job in jobs))

    def test_demo_jobmeta_csv_has_expected_columns(self) -> None:
        csv_path = PROJECT_ROOT / "examples" / "demo_jobmeta_import.csv"
        with csv_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)

        self.assertIn("gap_blocking", reader.fieldnames or [])
        self.assertIn("gap_learnable", reader.fieldnames or [])
        self.assertIn("next_action", reader.fieldnames or [])
        self.assertIn("notes", reader.fieldnames or [])
        self.assertEqual(len(rows), 8)

    def test_demo_it_jobs_csv_imports_into_sqlite(self) -> None:
        csv_path = PROJECT_ROOT / "examples" / "demo_it_jobs.csv"
        profile_path = PROJECT_ROOT / "config" / "profile.example.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "jobs.sqlite"
            stats = import_jobs_csv(csv_path, profile, db_path)
            jobs = list_jobs(db_path)

        self.assertEqual(stats["incoming"], 8)
        self.assertEqual(stats["new"], 8)
        self.assertEqual(len(jobs), 8)
        self.assertTrue(any("Application Support" in job["title"] for job in jobs))
        self.assertTrue(any(job["decision"] == "ablehnen" for job in jobs))

    def test_demo_cv_builds_profile_signals(self) -> None:
        cv_path = PROJECT_ROOT / "examples" / "demo_cv_it_profile.txt"
        text = cv_path.read_text(encoding="utf-8")

        profile, signals = build_profile_from_cv(text)

        self.assertIn("Dokumentation", signals)
        self.assertIn("Informationsmanagement", signals)
        self.assertIn("Technische Grundlagen", signals)
        self.assertIn("python", profile["positive_keywords"])
        self.assertIn("sql", profile["positive_keywords"])
        self.assertIn("documentation", profile["positive_keywords"])

    def test_demo_statistics_cv_builds_different_profile_signals(self) -> None:
        cv_path = PROJECT_ROOT / "examples" / "demo_cv_statistics_profile.txt"
        text = cv_path.read_text(encoding="utf-8")

        profile, signals = build_profile_from_cv(text)

        self.assertIn("Statistik / Analyse", signals)
        self.assertIn("Reporting", signals)
        self.assertIn("statistics", profile["positive_keywords"])
        self.assertIn("statistik", profile["positive_keywords"])
        self.assertIn("quantitative analysis", profile["positive_keywords"])
        self.assertIn("reporting", profile["positive_keywords"])
        self.assertIn("spss", profile["positive_keywords"])

    def test_demo_information_management_cv_builds_profile_signals(self) -> None:
        cv_path = PROJECT_ROOT / "examples" / "demo_cv_information_management.txt"
        text = cv_path.read_text(encoding="utf-8")

        profile, signals = build_profile_from_cv(text)

        self.assertIn("Dokumentation", signals)
        self.assertIn("Informationsmanagement", signals)
        self.assertIn("metadata", profile["positive_keywords"])
        self.assertIn("metadaten", profile["positive_keywords"])
        self.assertIn("knowledge base", profile["positive_keywords"])

    def test_demo_statistics_jobs_csv_imports_into_sqlite(self) -> None:
        csv_path = PROJECT_ROOT / "examples" / "demo_statistics_jobs.csv"
        profile_path = PROJECT_ROOT / "config" / "profile.example.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "jobs.sqlite"
            stats = import_jobs_csv(csv_path, profile, db_path)
            jobs = list_jobs(db_path)

        self.assertEqual(stats["incoming"], 8)
        self.assertEqual(stats["new"], 8)
        self.assertEqual(len(jobs), 8)
        self.assertTrue(any(job["source"] == "demo-stat" for job in jobs))
        self.assertTrue(any("Reporting" in job["role_cluster"] for job in jobs))

    def test_research_snapshot_csvs_import_into_sqlite(self) -> None:
        profile_path = PROJECT_ROOT / "config" / "profile.example.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        snapshot_paths = sorted((PROJECT_ROOT / "examples" / "research_snapshots").glob("jobs_*_snapshot_2026-06-21.csv"))

        self.assertEqual(len(snapshot_paths), 3)
        for csv_path in snapshot_paths:
            with self.subTest(csv_path=csv_path.name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    db_path = Path(temp_dir) / "jobs.sqlite"
                    stats = import_jobs_csv(csv_path, profile, db_path)
                    jobs = list_jobs(db_path)

                self.assertGreaterEqual(stats["incoming"], 12)
                self.assertEqual(stats["new"], stats["incoming"])
                self.assertEqual(len(jobs), stats["incoming"])
                self.assertTrue(all(job["source"].startswith("snapshot-") for job in jobs))
                self.assertTrue(all("Recherche-Snapshot 2026-06-21" in job["notes"] for job in jobs))

class ResearchSnapshotManifestTests(TestCase):
    def test_research_snapshot_manifest_exists_and_matches_files(self) -> None:
        manifest_path = PROJECT_ROOT / "examples" / "research_snapshots" / "snapshot_manifest_2026-06-21.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["snapshot_date"], "2026-06-21")
        self.assertEqual(len(manifest["datasets"]), 3)
        for dataset in manifest["datasets"]:
            csv_path = PROJECT_ROOT / "examples" / "research_snapshots" / dataset["file"]
            self.assertTrue(csv_path.exists())
            with csv_path.open(newline="", encoding="utf-8") as handle:
                row_count = sum(1 for _ in csv.DictReader(handle))
            self.assertEqual(row_count, dataset["rows"])
            self.assertGreaterEqual(row_count, 20)
