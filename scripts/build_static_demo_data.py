from __future__ import annotations

import json
import tempfile
from pathlib import Path

from jobmeta_harvester.dashboard import DEMO_DATASETS, DEMO_PROFILES
from jobmeta_harvester.database import import_jobs_csv_text, init_db, list_jobs
from jobmeta_harvester.profile_builder import build_profile_from_cv, extract_cv_text

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'static-api-data.json'


def build() -> dict:
    profiles = []
    datasets = []
    scored = {}
    for key, meta in DEMO_PROFILES.items():
        text = extract_cv_text(meta['path'].name, meta['path'].read_bytes())
        profile, _signals = build_profile_from_cv(text)
        profiles.append({
            'key': key,
            'label': meta['label'],
            'description': meta['description'],
            'filename': meta['path'].name,
            'profile': profile,
        })
        scored[key] = {}
        for dataset_key, dataset_meta in DEMO_DATASETS.items():
            csv_text = dataset_meta['path'].read_text(encoding='utf-8')
            with tempfile.TemporaryDirectory() as tmp:
                db_path = Path(tmp) / 'jobs.sqlite'
                init_db(db_path)
                stats = import_jobs_csv_text(csv_text, profile, db_path)
                rows = list_jobs(db_path)
            scored[key][dataset_key] = {'stats': stats, 'jobs': rows}
    for key, meta in DEMO_DATASETS.items():
        # Count rows without depending on CSV module just for concise metadata.
        row_count = max(0, len(meta['path'].read_text(encoding='utf-8').splitlines()) - 1)
        datasets.append({
            'key': key,
            'label': meta['label'],
            'description': meta['description'],
            'filename': meta['path'].name,
            'row_count': row_count,
        })
    return {
        'version': 'v51',
        'notice': 'Recherche-Snapshots wurden am 2026-06-21 KI-gestützt aus öffentlicher Websuche und sichtbaren Trefferseiten strukturiert. Große Jobplattformen werden nicht automatisiert gecrawlt. Links können veralten und dienen nur Demo-Zwecken.',
        'profiles': profiles,
        'datasets': datasets,
        'scored': scored,
    }


if __name__ == '__main__':
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2), encoding='utf-8')
    print(OUT)
