from unittest import TestCase

from src.jobmeta_harvester.matching import score_job
from src.jobmeta_harvester.models import JobPosting


PROFILE = {
    "base_score": 40,
    "positive_keywords": {
        "metadata": 12,
        "documentation": 9,
        "python": 7,
        "remote": 8,
        "junior": 8,
    },
    "negative_keywords": {
        "senior": -14,
        "sales": -10,
    },
    "preferred_locations": ["remote", "hamburg"],
    "title_boost_keywords": ["metadata", "documentation", "python", "junior"],
}


class ScoreJobTest(TestCase):
    def test_scores_relevant_junior_information_role_high(self):
        job = JobPosting(
            source="sample",
            source_id="1",
            title="Junior Metadata Documentation Specialist",
            company="Example",
            location="Hamburg / Remote",
            remote=True,
            url="https://example.org",
            date_posted="2026-06-01",
            description="Use Python basics for metadata quality and documentation.",
            tags=["metadata", "documentation"],
        )

        result = score_job(job, PROFILE)

        self.assertGreaterEqual(result.score, 85)
        self.assertIn("metadata", result.keywords_found)
        self.assertIn("documentation", result.keywords_found)

    def test_penalizes_senior_sales_role(self):
        job = JobPosting(
            source="sample",
            source_id="2",
            title="Senior Sales Lead",
            company="Example",
            location="On site",
            remote=False,
            url="https://example.org",
            date_posted="2026-06-01",
            description="Senior sales role.",
            tags=["sales"],
        )

        result = score_job(job, PROFILE)

        self.assertLess(result.score, 40)
        self.assertIn("senior", result.keywords_found)
        self.assertIn("sales", result.keywords_found)
