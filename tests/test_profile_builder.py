from unittest import TestCase

from src.jobmeta_harvester.profile_builder import build_profile_from_cv, extract_cv_text


class ProfileBuilderTest(TestCase):
    def test_build_profile_from_cv_selects_relevant_signals(self):
        cv_text = """
        Bibliotheks- und Informationsmanagement, Data Quality, Trust & Safety,
        AI Review, technische Dokumentation, Knowledge Base, Python, SQL,
        Metadaten und Katalogisierung nach RDA.
        """

        profile, signals = build_profile_from_cv(cv_text)

        self.assertIn("data quality", profile["positive_keywords"])
        self.assertIn("trust & safety", profile["positive_keywords"])
        self.assertIn("python", profile["positive_keywords"])
        self.assertIn("Data Quality", signals)
        self.assertIn("AI Review / Trust & Safety", signals)
        self.assertEqual(profile["profile_source"], "cv_import")

    def test_extract_cv_text_reads_plain_text_files(self):
        text = extract_cv_text("lebenslauf.txt", "Datenqualität und Dokumentation".encode("utf-8"))

        self.assertIn("Datenqualität", text)
