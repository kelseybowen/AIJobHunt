"""
Arbeitnow API → MongoDB ingestion.

Fetches job postings from the Arbeitnow API, normalizes them,
and appends to a MongoDB collection. Uses shared mongo_ingestion_utils.

Env: MONGODB_CONNECT_STRING, PROD_DB, MONGO_JOBS_COLLECTION (optional).
Data source label: "Arbeitnow".

Run from backend: python app/api/arbeitnow/arbeitnow_to_mongo.py
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
load_dotenv(dotenv_path=_env_path)

try:
    from backend.app.api.mongo_ingestion_utils import get_mongo_collection, insert_jobs_into_mongo
except ImportError:
    import sys
    _api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _api_dir not in sys.path:
        sys.path.insert(0, _api_dir)
    from mongo_ingestion_utils import get_mongo_collection, insert_jobs_into_mongo

try:
    from backend.app.api.arbeitnow.test_arbeitnow_api import test_arbeitnow_api, normalize_arbeitnow_job
except ImportError:
    from test_arbeitnow_api import test_arbeitnow_api, normalize_arbeitnow_job


def run(
    page: Optional[int] = None,
    remote_only: bool = True,
    keywords: Optional[str] = "Software Engineer",
    salary_min: Optional[int] = 50000,
    salary_max: Optional[int] = 150000,
) -> int:
    """Fetch jobs from Arbeitnow and insert into MongoDB. Returns count inserted."""
    print("Arbeitnow → MongoDB")
    print("=" * 50)
    data = test_arbeitnow_api(
        page=page,
        remote_only=remote_only,
        keywords=keywords,
        salary_min=salary_min,
        salary_max=salary_max,
    )
    jobs = data.get("data", [])
    print(f"Retrieved {len(jobs)} job postings from Arbeitnow.")
    if not jobs:
        print("No jobs to insert.")
        return 0
    collection = get_mongo_collection()
    count = insert_jobs_into_mongo(
        jobs, collection, source="Arbeitnow", normalizer=normalize_arbeitnow_job
    )
    print(f"Inserted {count} documents into MongoDB.")
    return count


if __name__ == "__main__":
    try:
        run()
        print("Done.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        raise
