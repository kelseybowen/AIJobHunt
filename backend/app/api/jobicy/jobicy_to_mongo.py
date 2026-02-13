"""
Jobicy API → MongoDB ingestion.

Fetches job postings from the Jobicy API, normalizes them,
and appends to a MongoDB collection. Uses shared mongo_ingestion_utils.

Env: MONGODB_CONNECT_STRING, PROD_DB, MONGO_JOBS_COLLECTION (optional).
Data source label: "Jobicy".

Run from backend: python app/api/jobicy/jobicy_to_mongo.py
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
    from backend.app.api.jobicy.test_jobicy_api import test_jobicy_api, normalize_jobicy_job
except ImportError:
    from test_jobicy_api import test_jobicy_api, normalize_jobicy_job


def run(
    tag: Optional[str] = "Software Engineer",
    industry: Optional[str] = None,
    geo: Optional[str] = None,
    count: Optional[int] = 100,
) -> int:
    """Fetch jobs from Jobicy and insert into MongoDB. Returns count inserted."""
    print("Jobicy → MongoDB")
    print("=" * 50)
    data = test_jobicy_api(tag=tag, industry=industry, geo=geo, count=count)
    jobs = data.get("jobs", [])
    print(f"Retrieved {len(jobs)} job postings from Jobicy.")
    if not jobs:
        print("No jobs to insert.")
        return 0
    collection = get_mongo_collection()
    count_inserted = insert_jobs_into_mongo(
        jobs, collection, source="Jobicy", normalizer=normalize_jobicy_job
    )
    print(f"Inserted {count_inserted} documents into MongoDB.")
    return count_inserted


if __name__ == "__main__":
    try:
        run()
        print("Done.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        raise
