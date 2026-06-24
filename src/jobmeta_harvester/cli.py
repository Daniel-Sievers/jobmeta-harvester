from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dashboard import run_dashboard
from .database import import_jobs_csv, import_tracking_csv, list_jobs, upsert_jobs
from .exporters import export_jobs_csv, export_records_csv
from .http import FetchError
from .models import JobPosting
from .normalization import clean_tags, clean_text
from .public_export import create_public_export
from .sources import fetch_arbeitnow_jobs, fetch_remotive_jobs


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE = PROJECT_ROOT / "config" / "profile.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "jobs.csv"
DEFAULT_DB = PROJECT_ROOT / "data" / "jobs.sqlite"
SAMPLE_JOBS = PROJECT_ROOT / "examples" / "sample_jobs.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Harvest job postings, score them against a profile, and export CSV metadata."
    )
    parser.add_argument(
        "--source",
        choices=["all", "arbeitnow", "remotive"],
        default="all",
        help="Job source to fetch.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of jobs per source.",
    )
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        help="Search keyword. Can be used multiple times.",
    )
    parser.add_argument(
        "--profile",
        type=Path,
        default=DEFAULT_PROFILE,
        help="Path to profile JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output CSV path.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help="SQLite database path.",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Use bundled sample jobs instead of live APIs.",
    )
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Export directly to CSV without storing jobs in SQLite.",
    )
    parser.add_argument(
        "--export-only",
        action="store_true",
        help="Export the existing SQLite database to CSV without fetching jobs.",
    )
    parser.add_argument(
        "--import-csv",
        type=Path,
        help="Import application_status and notes from an edited CSV.",
    )
    parser.add_argument(
        "--import-jobs",
        type=Path,
        help="Import job rows from a CSV file and score them.",
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Start the local browser dashboard.",
    )
    parser.add_argument(
        "--prepare-github-release",
        action="store_true",
        help="Create a sanitized public zip without local databases, caches, or private profile data.",
    )
    parser.add_argument(
        "--release-output",
        type=Path,
        default=PROJECT_ROOT / "dist" / "jobmeta-harvester-public.zip",
        help="Output path for --prepare-github-release.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Dashboard host.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Dashboard port.",
    )
    args = parser.parse_args(argv)

    if args.prepare_github_release:
        result = create_public_export(PROJECT_ROOT, args.release_output)
        print(f"Created public GitHub package: {result.zip_path}")
        print(f"Included files: {result.included_files}")
        print(f"Excluded private/generated files: {result.excluded_files}")
        print("Checklist:")
        for item in result.checklist:
            print(f"- {item}")
        return 0

    profile = _load_profile(args.profile)

    if args.dashboard:
        run_dashboard(args.db, profile_path=args.profile, host=args.host, port=args.port)
        return 0

    if args.import_jobs:
        stats = import_jobs_csv(args.import_jobs, profile, args.db)
        records = list_jobs(args.db)
        export_records_csv(records, args.output)
        print(
            "Imported jobs into "
            f"{args.db} (incoming={stats['incoming']}, new={stats['new']}, "
            f"updated={stats['updated']}, duplicates={stats['duplicates']})"
        )
        print(f"Exported {len(records)} database jobs to {args.output}")
        return 0

    if args.import_csv:
        updated = import_tracking_csv(args.import_csv, args.db)
        print(f"Updated tracking fields for {updated} jobs in {args.db}")
        export_records_csv(list_jobs(args.db), args.output)
        print(f"Exported database to {args.output}")
        return 0

    if args.export_only:
        records = list_jobs(args.db)
        export_records_csv(records, args.output)
        print(f"Exported {len(records)} database jobs to {args.output}")
        return 0

    jobs = _load_sample_jobs() if args.sample else _fetch_jobs(args.source, args.limit, args.query)

    if not jobs:
        print("No jobs found. Try --sample or a different source/query.")
        return 1

    if args.no_db:
        export_jobs_csv(jobs, profile, args.output)
        print(f"Exported {len(jobs)} jobs to {args.output}")
        return 0

    stats = upsert_jobs(jobs, profile, args.db)
    records = list_jobs(args.db)
    export_records_csv(records, args.output)
    print(
        "Stored jobs in "
        f"{args.db} (incoming={stats['incoming']}, new={stats['new']}, "
        f"updated={stats['updated']}, duplicates={stats['duplicates']})"
    )
    print(f"Exported {len(records)} database jobs to {args.output}")
    return 0


def _load_profile(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _fetch_jobs(source: str, limit: int, query: list[str]) -> list[JobPosting]:
    fetchers = []
    if source in {"all", "arbeitnow"}:
        fetchers.append(("arbeitnow", fetch_arbeitnow_jobs))
    if source in {"all", "remotive"}:
        fetchers.append(("remotive", fetch_remotive_jobs))

    jobs: list[JobPosting] = []
    for source_name, fetcher in fetchers:
        try:
            jobs.extend(fetcher(limit=limit, query=query))
        except FetchError as exc:
            print(f"Skipped {source_name}: {exc}")
    return jobs


def _load_sample_jobs() -> list[JobPosting]:
    with SAMPLE_JOBS.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    return [
        JobPosting(
            source=clean_text(row.get("source")),
            source_id=clean_text(row.get("source_id")),
            title=clean_text(row.get("title")),
            company=clean_text(row.get("company")),
            location=clean_text(row.get("location")),
            remote=row.get("remote"),
            url=clean_text(row.get("url")),
            date_posted=clean_text(row.get("date_posted")),
            description=clean_text(row.get("description")),
            tags=clean_tags(row.get("tags")),
        )
        for row in rows
    ]
