from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import List

from .model import JobAd

DATA_DIR = Path("data")
JOBS_PATH = DATA_DIR / "jobs.jsonl"


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _hash_text(text: str) -> str:
    """
    Compute a stable hash for the raw job text.
    Used to detect duplicates.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_existing_hashes() -> set[str]:
    """
    Load hashes of raw_text for all stored jobs.
    """
    if not JOBS_PATH.exists():
        return set()

    hashes: set[str] = set()
    with JOBS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            raw = data.get("raw_text", "")
            if raw:
                hashes.add(_hash_text(raw))
    return hashes


def append_job(job: JobAd) -> bool:
    """
    Append a JobAd as a JSON line to jobs.jsonl.

    Returns:
        True if the job was saved, False if it was detected as duplicate.
    """
    ensure_data_dir()

    existing_hashes = _load_existing_hashes()
    new_hash = _hash_text(job.raw_text)

    if new_hash in existing_hashes:
        # Already stored – skip
        return False

    with JOBS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(job.model_dump(), default=str) + "\n")

    return True


def load_jobs() -> List[JobAd]:
    """
    Load all JobAd entries from jobs.jsonl.
    """
    if not JOBS_PATH.exists():
        return []

    jobs: List[JobAd] = []
    with JOBS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            jobs.append(JobAd(**data))
    return jobs
# storage.py
def save_fit_result(job_id: str, result: dict):
    ...

def load_fit_result(job_id: str) -> dict | None:
    ...
