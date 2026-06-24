from __future__ import annotations

from io import BytesIO
from pathlib import Path


class ProfileBuildError(RuntimeError):
    """Raised when a CV file cannot be read for profile generation."""


def extract_cv_text(filename: str, content: bytes) -> str:
    suffix = Path(filename or "").suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf_text(content)
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ProfileBuildError("Die Datei konnte nicht als Text gelesen werden.")


def build_profile_from_cv(text: str) -> tuple[dict, list[str]]:
    lower_text = text.lower()
    positive_keywords = _selected_keywords(lower_text, _POSITIVE_KEYWORDS)
    negative_keywords = dict(_NEGATIVE_KEYWORDS)
    signals = _signals(lower_text)

    profile = {
        "profile_name": "CV-based information management profile",
        "base_score": 28,
        "positive_keywords": positive_keywords,
        "negative_keywords": negative_keywords,
        "preferred_locations": [
            "remote",
            "home office",
            "hybrid",
            "hamburg",
            "germany",
            "deutschland",
        ],
        "title_boost_keywords": [
            "data quality",
            "datenqualität",
            "documentation",
            "dokumentation",
            "knowledge",
            "wissensmanagement",
            "information",
        "metadata",
        "metadaten",
        "review",
        "trust",
        "statistics",
        "statistik",
        "analysis",
        "analyse",
        "reporting",
    ],
        "profile_source": "cv_import",
        "profile_notes": "Generated from CV text. Review weights after testing real job imports.",
    }
    return profile, signals


def _extract_pdf_text(content: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ProfileBuildError(
            "PDF-Import braucht das Paket pypdf. Installiere es mit: py -3 -m pip install pypdf"
        ) from exc

    reader = PdfReader(BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(page.strip() for page in pages if page.strip())
    if not text.strip():
        raise ProfileBuildError("Aus dem PDF konnte kein Text extrahiert werden.")
    return text


def _selected_keywords(text: str, bank: dict[str, tuple[int, tuple[str, ...]]]) -> dict[str, int]:
    selected: dict[str, int] = {}
    for keyword, (weight, triggers) in bank.items():
        if keyword in text or any(trigger in text for trigger in triggers):
            selected[keyword] = weight
    return selected


def _signals(text: str) -> list[str]:
    labels = []
    for label, needles in _SIGNALS.items():
        if any(needle in text for needle in needles):
            labels.append(label)
    return labels


_POSITIVE_KEYWORDS: dict[str, tuple[int, tuple[str, ...]]] = {
    "data quality": (14, ("datenqualität", "daten- und prozessqualität")),
    "datenqualität": (14, ("data quality", "daten- und prozessqualität")),
    "quality assurance": (11, ("qa-checkliste", "qualitätssicherung")),
    "ai review": (12, ("ki-gestützte", "human-in-the-loop")),
    "trust & safety": (12, ("trust & safety",)),
    "identity verification": (10, ("digital identity", "identitätsprüfung")),
    "digital identity": (10, ("identity verification", "identitätsprüfung")),
    "regelbasierte prüfung": (10, ("regelbasierter prüfung", "prüfvorgaben")),
    "plausibilitätsprüfung": (9, ("plausibilitätsprüfung",)),
    "compliance": (7, ("compliance",)),
    "documentation": (10, ("dokumentation", "readme")),
    "dokumentation": (10, ("documentation", "nutzeranleitungen")),
    "technical documentation": (8, ("technische dokumentation",)),
    "knowledge base": (10, ("wissensmanagement", "knowledge base")),
    "wissensmanagement": (10, ("knowledge base", "wissensorganisation")),
    "information management": (10, ("informationsmanagement",)),
    "informationsmanagement": (10, ("information management",)),
    "metadata": (10, ("metadaten", "metadatenmanagement")),
    "metadaten": (10, ("metadata", "metadatenmanagement")),
    "taxonomy": (8, ("taxonomie",)),
    "taxonomie": (8, ("taxonomy",)),
    "klassifikation": (8, ("klassifikation",)),
    "katalogisierung": (8, ("rda", "k10plus")),
    "recherche": (6, ("literaturrecherche", "research")),
    "research": (6, ("recherche",)),
    "statistics": (12, ("statistik", "statistische analyse", "statistical analysis")),
    "statistik": (12, ("statistics", "statistische analyse", "statistical analysis")),
    "quantitative analysis": (11, ("quantitative analyse", "quantitative methoden")),
    "datenanalyse": (10, ("data analysis", "datenanalyse")),
    "data analysis": (10, ("datenanalyse",)),
    "reporting": (8, ("reporting", "berichte", "dashboard")),
    "power bi": (7, ("power bi", "powerbi")),
    "spss": (7, ("spss",)),
    "rstudio": (7, ("rstudio", "r studio")),
    "python": (5, ("python",)),
    "sql": (5, ("sql",)),
    "csv": (4, ("csv",)),
    "json": (4, ("json",)),
    "openrefine": (5, ("openrefine",)),
    "markdown": (5, ("markdown", "readme")),
    "github": (4, ("git/github", "github")),
    "git": (4, ("git/github",)),
    "linux": (4, ("linux", "terminal")),
    "html": (3, ("html/css",)),
    "css": (3, ("html/css",)),
    "javascript": (3, ("javascript",)),
    "remote": (4, ("remote",)),
    "hybrid": (3, ("hybrid",)),
    "working student": (5, ("werkstudent", "studentische hilfskraft")),
    "werkstudent": (5, ("working student", "studentische hilfskraft")),
    "junior": (5, ("einstieg", "junior")),
}

_NEGATIVE_KEYWORDS = {
    "senior": -18,
    "lead": -14,
    "principal": -14,
    "head of": -18,
    "teamleiter": -14,
    "teamleitung": -14,
    "5+ years": -12,
    "5 years": -12,
    "mehrjährige berufserfahrung": -10,
    "mid-level": -8,
    "sales": -10,
    "vertrieb": -10,
    "akquise": -10,
    "telefonakquise": -12,
    "provision": -8,
    "fullstack senior": -14,
    "java expert": -10,
    "sap hcm": -5,
}

_SIGNALS = {
    "Data Quality": ("data quality", "datenqualität", "daten- und prozessqualität"),
    "AI Review / Trust & Safety": ("ai review", "trust & safety", "ki-gestützte"),
    "Dokumentation": ("dokumentation", "readme", "nutzeranleitungen"),
    "Informationsmanagement": ("informationsmanagement", "metadaten", "katalogisierung"),
    "Statistik / Analyse": ("statistik", "statistics", "quantitative analyse", "datenanalyse", "spss"),
    "Reporting": ("reporting", "power bi", "dashboard"),
    "Technische Grundlagen": ("python", "sql", "github", "linux"),
    "Remote/Hybrid offen": ("remote", "hybrid", "relocation"),
}
