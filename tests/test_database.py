from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from src.jobmeta_harvester.database import (
    delete_all_jobs,
    delete_jobs_by_source_prefixes,
    import_jobs_csv,
    import_tracking_csv,
    list_jobs,
    rescore_jobs,
    update_tracking,
    upsert_jobs,
)
from src.jobmeta_harvester.exporters import export_records_csv
from src.jobmeta_harvester.models import JobPosting


PROFILE = {
    "base_score": 40,
    "positive_keywords": {"metadata": 12, "remote": 8},
    "negative_keywords": {"senior": -14},
    "preferred_locations": ["remote"],
    "title_boost_keywords": ["metadata"],
}


class DatabaseTest(TestCase):
    def test_upsert_preserves_tracking_fields(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            job = _job(title="Metadata Assistant")

            first = upsert_jobs([job], PROFILE, db_path)
            second = upsert_jobs([job], PROFILE, db_path)
            rows = list_jobs(db_path)

            self.assertEqual(first["new"], 1)
            self.assertEqual(second["updated"], 1)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["seen_count"], 2)

    def test_import_tracking_csv_updates_status_and_notes(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            csv_path = Path(directory) / "jobs.csv"
            upsert_jobs([_job(title="Metadata Assistant")], PROFILE, db_path)
            rows = list_jobs(db_path)
            rows[0]["application_status"] = "interesting"
            rows[0]["notes"] = "Check portfolio fit"
            export_records_csv(rows, csv_path)

            updated = import_tracking_csv(csv_path, db_path)
            imported = list_jobs(db_path)

            self.assertEqual(updated, 1)
            self.assertEqual(imported[0]["application_status"], "interesting")
            self.assertEqual(imported[0]["notes"], "Check portfolio fit")

    def test_update_tracking_updates_one_job(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            upsert_jobs([_job(title="Metadata Assistant")], PROFILE, db_path)
            job_key = list_jobs(db_path)[0]["job_key"]

            updated = update_tracking(
                db_path,
                job_key,
                application_status="applied",
                notes="Sent application",
                decision="bewerben",
                interest="hoch",
                priority="hoch",
                application_deadline="2026-07-01",
                next_action="Portfolio anpassen",
                url="https://example.org/jobs/direct-12345",
            )
            rows = list_jobs(db_path)

            self.assertTrue(updated)
            self.assertEqual(rows[0]["application_status"], "applied")
            self.assertEqual(rows[0]["notes"], "Sent application")
            self.assertEqual(rows[0]["decision"], "bewerben")
            self.assertEqual(rows[0]["interest"], "hoch")
            self.assertEqual(rows[0]["priority"], "hoch")
            self.assertEqual(rows[0]["application_deadline"], "2026-07-01")
            self.assertEqual(rows[0]["next_action"], "Portfolio anpassen")
            self.assertEqual(rows[0]["url"], "https://example.org/jobs/direct-12345")

    def test_import_jobs_csv_adds_analysis_fields(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            csv_path = Path(directory) / "import.csv"
            csv_path.write_text(
                "source,url,company,title,role_cluster,location_remote_start,"
                "must_skills,gap_blocking,gap_learnable,decision,notes\n"
                "manual,https://example.org,Example Org,Technical Writer,"
                "Technical Writing,Hamburg Remote,Documentation,None,"
                "Redaktionssystem lernen,beobachten,Good fit\n",
                encoding="utf-8",
            )

            stats = import_jobs_csv(csv_path, PROFILE, db_path)
            rows = list_jobs(db_path)

            self.assertEqual(stats["new"], 1)
            self.assertEqual(rows[0]["role_cluster"], "Technical Writing")
            self.assertEqual(rows[0]["gap_learnable"], "Redaktionssystem lernen")
            self.assertEqual(rows[0]["decision"], "beobachten")
            self.assertEqual(rows[0]["notes"], "Good fit")

    def test_upsert_manual_record_scores_and_stores_job(self):
        from src.jobmeta_harvester.database import upsert_job_records

        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            record = {
                "source": "manual",
                "url": "https://example.org/manual",
                "company": "Manual Org",
                "title": "Metadata Documentation Assistant",
                "location_remote_start": "Hamburg / Remote",
                "priority": "mittel",
                "application_deadline": "2026-07-15",
                "next_action": "Anzeige pruefen",
                "main_tasks": "Metadata documentation and research",
                "must_skills": "metadata, documentation",
                "notes": "Pasted manually",
            }

            stats = upsert_job_records([record], PROFILE, db_path)
            rows = list_jobs(db_path)

            self.assertEqual(stats["new"], 1)
            self.assertEqual(rows[0]["company"], "Manual Org")
            self.assertEqual(rows[0]["priority"], "mittel")
            self.assertEqual(rows[0]["application_deadline"], "2026-07-15")
            self.assertEqual(rows[0]["next_action"], "Anzeige pruefen")
            self.assertEqual(rows[0]["notes"], "Pasted manually")
            self.assertGreater(rows[0]["match_score"], 40)

    def test_rescore_jobs_updates_existing_match_scores(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            upsert_jobs([_job(title="Metadata Assistant")], PROFILE, db_path)
            old_score = list_jobs(db_path)[0]["match_score"]
            new_profile = {
                "base_score": 10,
                "positive_keywords": {"documentation": 5},
                "negative_keywords": {},
                "preferred_locations": [],
                "title_boost_keywords": [],
            }

            updated = rescore_jobs(new_profile, db_path)
            rows = list_jobs(db_path)

            self.assertEqual(updated, 1)
            self.assertLess(rows[0]["match_score"], old_score)

    def test_delete_jobs_by_source_prefixes_only_deletes_matching_sources(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            upsert_jobs(
                [
                    _job(title="Demo Metadata", source="demo"),
                    _job(title="Demo IT", source="demo-it"),
                    _job(title="Manual Metadata", source="manual"),
                ],
                PROFILE,
                db_path,
            )

            deleted = delete_jobs_by_source_prefixes(db_path, ["demo"])
            rows = list_jobs(db_path)

            self.assertEqual(deleted, 2)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["source"], "manual")


    def test_delete_all_jobs_clears_database_but_keeps_schema(self):
        with TemporaryDirectory() as directory:
            db_path = Path(directory) / "jobs.sqlite"
            upsert_jobs(
                [
                    _job(title="Demo Metadata", source="demo"),
                    _job(title="Manual Metadata", source="manual"),
                ],
                PROFILE,
                db_path,
            )

            deleted = delete_all_jobs(db_path)
            rows = list_jobs(db_path)

            self.assertEqual(deleted, 2)
            self.assertEqual(rows, [])


def _job(title: str, source: str = "sample") -> JobPosting:
    return JobPosting(
        source=source,
        source_id=title,
        title=title,
        company="Example",
        location="Remote",
        remote=True,
        url="https://example.org/jobs/1",
        date_posted="2026-06-01",
        description="Metadata work in a remote role.",
        tags=["metadata"],
    )
