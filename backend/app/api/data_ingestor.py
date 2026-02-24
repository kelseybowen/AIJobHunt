"""
Shared ingestion orchestration for API → MongoDB scripts.

Provides run_ingestion(source, normalizer, fetch_jobs) so each *_to_mongo.py script
can avoid duplicating .env loading and the "fetch → get collection → insert" flow.
Mongo-only logic (get_mongo_collection, insert_jobs_into_mongo) stays in mongo_ingestion_utils.

Only *_to_mongo.py scripts use this module; test_*.py do not.
"""

from typing import List, Dict, Any, Callable

import os

try:
    from backend.app.api.mongo_ingestion_utils import get_mongo_collection, insert_jobs_into_mongo
except ImportError:
    _api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    import sys
    if _api_dir not in sys.path:
        sys.path.insert(0, _api_dir)
    from mongo_ingestion_utils import get_mongo_collection, insert_jobs_into_mongo


def run_ingestion(
    source: str,
    normalizer: Callable[[Dict[str, Any]], Dict[str, Any]],
    fetch_jobs: Callable[[], List[Dict[str, Any]]],
) -> int:
    """
    Load jobs via fetch_jobs(), then insert into MongoDB using mongo_ingestion_utils.

    .env is loaded by get_mongo_collection() when needed. Data key names (e.g. "results",
    "data", "jobs", "jobs_results") are handled inside the fetch_jobs callable; this
    function only receives a list of raw job dicts.

    Args:
        source: Source label (e.g. "Adzuna", "Jobicy", "Arbeitnow").
        normalizer: Function that takes one raw job dict and returns a normalized dict
                    for job_schema.to_canonical_document.
        fetch_jobs: No-arg callable that returns the list of raw job dicts.

    Returns:
        Number of documents inserted, or 0 if no jobs.
    """
    try:
        jobs = fetch_jobs()
    except Exception as e:
        raise RuntimeError(f"{source} ingestion failed during fetch") from e
    if not jobs:
        return 0
    collection = get_mongo_collection()
    return insert_jobs_into_mongo(jobs, collection, source=source, normalizer=normalizer)
