from unittest import TestCase
from pathlib import Path
from tempfile import TemporaryDirectory

from src.jobmeta_harvester.dashboard import (
    _demo_options,
    _harvest_limit,
    _load_demo_selection,
    _profile_search_terms,
    _query_batches,
)
from src.jobmeta_harvester.database import list_jobs


class DashboardHarvestTest(TestCase):
    def test_harvest_limit_uses_allowed_steps(self):
        self.assertEqual(_harvest_limit(0), 50)
        self.assertEqual(_harvest_limit(51), 100)
        self.assertEqual(_harvest_limit(249), 250)
        self.assertEqual(_harvest_limit(10000), 500)

    def test_profile_search_terms_prefers_specific_profile_keywords(self):
        profile = {
            "positive_keywords": {
                "remote": 4,
                "hamburg": 4,
                "metadata": 10,
                "data quality": 14,
                "documentation": 10,
            },
            "title_boost_keywords": ["metadata"],
        }

        terms = _profile_search_terms(profile, max_terms=5)

        self.assertIn("data quality", terms)
        self.assertIn("metadata", terms)
        self.assertIn("documentation", terms)
        self.assertNotIn("remote", terms)
        self.assertNotIn("hamburg", terms)

    def test_query_batches_follow_search_mode(self):
        profile = {"positive_keywords": {"metadata": 10}}

        self.assertEqual(_query_batches("broad", ["manual"], profile), [[]])
        self.assertEqual(_query_batches("manual", ["metadata"], profile), [["metadata"]])
        self.assertEqual(_query_batches("manual", [], profile), [[]])
        self.assertEqual(_query_batches("profile", [], profile), [["metadata"]])

    def test_demo_options_expose_three_profiles_and_datasets(self):
        options = _demo_options()

        self.assertEqual(len(options["profiles"]), 3)
        self.assertEqual(len(options["datasets"]), 3)
        profile_keys = {item["key"] for item in options["profiles"]}
        dataset_keys = {item["key"] for item in options["datasets"]}
        self.assertEqual(profile_keys, {"information_management", "statistics", "it_support"})
        self.assertEqual(dataset_keys, {"information_management", "statistics", "it_support"})

    def test_load_demo_selection_imports_profile_and_dataset(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "jobs.sqlite"
            profile_path = root / "profile.json"

            result = _load_demo_selection(
                profile_key="statistics",
                dataset_key="statistics",
                reset_demo=False,
                db_path=db_path,
                profile_path=profile_path,
            )
            rows = list_jobs(db_path)

            self.assertEqual(result["profile_label"], "Statistik / Datenanalyse")
            self.assertEqual(result["dataset_label"], "Statistik / Data Analysis")
            self.assertGreaterEqual(result["stats"]["new"], 20)
            self.assertEqual(len(rows), result["stats"]["incoming"])
            self.assertTrue(profile_path.exists())
            self.assertTrue(any(row["source"] == "snapshot-linkedin" for row in rows))

    def test_load_demo_selection_can_reset_previous_demo_jobs(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "jobs.sqlite"
            profile_path = root / "profile.json"

            _load_demo_selection(
                profile_key="information_management",
                dataset_key="information_management",
                reset_demo=False,
                db_path=db_path,
                profile_path=profile_path,
            )
            result = _load_demo_selection(
                profile_key="it_support",
                dataset_key="it_support",
                reset_demo=True,
                db_path=db_path,
                profile_path=profile_path,
            )
            rows = list_jobs(db_path)

            self.assertGreater(result["deleted_demo_jobs"], 0)
            self.assertEqual(len(rows), result["stats"]["incoming"])
            self.assertGreaterEqual(len(rows), 20)
            self.assertTrue(any(row["source"].startswith("snapshot-") for row in rows))
