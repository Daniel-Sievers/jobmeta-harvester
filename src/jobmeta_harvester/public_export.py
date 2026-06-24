from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path


PUBLIC_PROFILE = {
    "profile_name": "Example information management profile",
    "base_score": 28,
    "positive_keywords": {
        "data quality": 14,
        "datenqualität": 14,
        "documentation": 10,
        "dokumentation": 10,
        "technical documentation": 8,
        "knowledge base": 10,
        "wissensmanagement": 10,
        "information management": 10,
        "informationsmanagement": 10,
        "metadata": 10,
        "metadaten": 10,
        "taxonomy": 8,
        "taxonomie": 8,
        "research": 6,
        "recherche": 6,
        "python": 5,
        "sql": 5,
        "csv": 4,
        "json": 4,
        "markdown": 5,
        "github": 4,
        "git": 4,
        "remote": 4,
        "hybrid": 3,
        "junior": 5,
    },
    "negative_keywords": {
        "senior": -18,
        "lead": -14,
        "principal": -14,
        "head of": -18,
        "teamleiter": -14,
        "teamleitung": -14,
        "5+ years": -12,
        "5 years": -12,
        "sales": -10,
        "vertrieb": -10,
        "akquise": -10,
    },
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
        "documentation",
        "knowledge",
        "information",
        "metadata",
        "review",
    ],
    "profile_source": "example_profile",
    "profile_notes": "Example profile for public GitHub demos. Replace with your own local profile for real use.",
}


CHECKLIST = [
    "SQLite-Datenbanken wurden nicht in die Public-ZIP übernommen.",
    "Python-Cache-Dateien wurden nicht in die Public-ZIP übernommen.",
    "Lokale Rohdaten- und Exportordner wurden nicht übernommen.",
    "config/profile.json wurde durch ein neutrales Beispielprofil ersetzt.",
    "config/profile.example.json wurde als Vorlage ergänzt.",
    "Beispieldaten aus examples/ bleiben für Demo und Tests erhalten.",
]


@dataclass(frozen=True)
class PublicExportResult:
    zip_path: Path
    root_name: str
    included_files: int
    excluded_files: int
    checklist: list[str]


def create_public_export(project_root: Path, output_path: Path | None = None) -> PublicExportResult:
    """Create a sanitized zip archive suitable for a public GitHub upload."""

    project_root = project_root.resolve()
    if output_path is None:
        output_path = project_root / "dist" / "jobmeta-harvester-public.zip"
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    root_name = f"{project_root.name}-public"
    included_files = 0
    excluded_files = 0

    with tempfile.TemporaryDirectory(prefix="jobmeta-public-") as temp_dir:
        public_root = Path(temp_dir) / root_name
        public_root.mkdir(parents=True, exist_ok=True)

        for source in sorted(project_root.rglob("*")):
            if source == output_path or output_path in source.parents:
                continue
            relative = source.relative_to(project_root)
            if _should_exclude(relative, source):
                if source.is_file():
                    excluded_files += 1
                continue

            target = public_root / relative
            if source.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue

            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            included_files += 1

        _write_public_profile(public_root)
        _write_public_data_placeholder(public_root)
        _write_public_report(public_root, root_name)
        included_files += 3

        if output_path.exists():
            output_path.unlink()
        with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in sorted(public_root.rglob("*")):
                if file_path.is_file():
                    archive.write(file_path, file_path.relative_to(public_root.parent))

    return PublicExportResult(
        zip_path=output_path,
        root_name=root_name,
        included_files=included_files,
        excluded_files=excluded_files,
        checklist=list(CHECKLIST),
    )


def _should_exclude(relative: Path, source: Path) -> bool:
    parts = set(relative.parts)
    if ".git" in parts or "__pycache__" in parts or ".pytest_cache" in parts:
        return True
    if ".venv" in parts or "venv" in parts or "dist" in parts:
        return True
    if source.is_file() and source.suffix.lower() in {".pyc", ".pyo", ".sqlite", ".sqlite3", ".db"}:
        return True
    if source.is_file() and source.suffix.lower() == ".zip":
        return True
    if relative.parts[:1] == ("data",):
        return True
    return False


def _write_public_profile(public_root: Path) -> None:
    config_dir = public_root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    text = json.dumps(PUBLIC_PROFILE, ensure_ascii=False, indent=2) + "\n"
    (config_dir / "profile.json").write_text(text, encoding="utf-8")
    (config_dir / "profile.example.json").write_text(text, encoding="utf-8")


def _write_public_data_placeholder(public_root: Path) -> None:
    data_dir = public_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / ".gitkeep").write_text(
        "Local SQLite databases are created here when you run the app.\n",
        encoding="utf-8",
    )


def _write_public_report(public_root: Path, root_name: str) -> None:
    lines = [
        "# Public Export Checklist",
        "",
        f"Generated package root: `{root_name}`",
        "",
        "This archive is intended for a public GitHub upload or portfolio review.",
        "",
        "## Automatic cleanup",
        "",
    ]
    lines.extend(f"- [x] {item}" for item in CHECKLIST)
    lines.extend(
        [
            "",
            "## Manual review before publishing",
            "",
            "- [ ] Review screenshots before adding them to the repository.",
            "- [ ] Do not commit real CV files, private notes, or real application tracking data.",
            "- [ ] Use demo data from `examples/` for screenshots and demos.",
            "- [ ] Run `python -m unittest discover tests` before publishing.",
            "",
        ]
    )
    (public_root / "PUBLIC_EXPORT_CHECKLIST.md").write_text("\n".join(lines), encoding="utf-8")
