"""
Remotive API → MongoDB ingestion.

Fetches job postings from the Remotive API, normalizes them,
and appends to a MongoDB collection. Uses shared mongo_ingestion_utils.

Env: MONGODB_CONNECT_STRING, PROD_DB, MONGO_JOBS_COLLECTION (optional).
Data source label: "Remotive".

Run from backend: python app/api/remotive/remotive_to_mongo.py
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
    from backend.app.api.remotive.test_remotive_api import test_remotive_api, normalize_remotive_job
except ImportError:
    from test_remotive_api import test_remotive_api, normalize_remotive_job


def run(
    category: Optional[str] = "software-dev",
    search: Optional[str] = "Software Engineer",
    limit: Optional[int] = None,
) -> int:
    """Fetch jobs from Remotive and insert into MongoDB. Returns count inserted."""
    print("Remotive → MongoDB")
    print("=" * 50)
    data = test_remotive_api(category=category, search=search, limit=limit)
    jobs = data.get("jobs", [])
    print(f"Retrieved {len(jobs)} job postings from Remotive.")
    if not jobs:
        print("No jobs to insert.")
        return 0
    collection = get_mongo_collection()
    count = insert_jobs_into_mongo(
        jobs, collection, source="Remotive", normalizer=normalize_remotive_job
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
