from unittest import TestCase

from src.jobmeta_harvester.analytics import build_skill_gap_summary


class AnalyticsTest(TestCase):
    def test_build_skill_gap_summary_counts_learning_priorities(self):
        rows = [
            {
                "match_score": 82,
                "gap_blocking": "Redaktionserfahrung",
                "gap_learnable": "Redaktionssysteme, Doku-Probe",
                "gap_bonus": "Normen",
                "must_skills": "Dokumentation, Redaktionssysteme",
                "tools_systems": "MS Office, Redaktionssysteme",
                "already_have": "Recherche, Struktur",
            },
            {
                "match_score": 64,
                "gap_blocking": "keine",
                "gap_learnable": "Redaktionssysteme",
                "gap_bonus": "Branchenwissen",
                "must_skills": "Dokumentation",
                "tools_systems": "MS Office",
                "already_have": "Recherche",
            },
        ]

        summary = build_skill_gap_summary(rows, top_n=3)

        self.assertEqual(summary["total_jobs"], 2)
        self.assertEqual(summary["strong_jobs"], 1)
        self.assertEqual(summary["learnable_gaps"][0]["label"], "Redaktionssysteme")
        self.assertEqual(summary["learnable_gaps"][0]["count"], 2)
        self.assertEqual(summary["learning_priorities"][0]["label"], "Redaktionssysteme")
        self.assertGreater(summary["learning_priorities"][0]["count"], 2)
