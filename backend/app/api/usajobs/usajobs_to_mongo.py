"""
USAJobs API → MongoDB ingestion.

Fetches job postings from the USAJobs API, normalizes them,
and appends to a MongoDB collection. Uses shared mongo_ingestion_utils.

Env: MONGODB_CONNECT_STRING, PROD_DB, MONGO_JOBS_COLLECTION (optional), USAJOBS_API_KEY.
Data source label: "USAJobs".

Run from backend: python app/api/usajobs/usajobs_to_mongo.py
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
    from backend.app.api.usajobs.test_usajobs_api import test_usajobs_api, normalize_usajobs_job
except ImportError:
    from test_usajobs_api import test_usajobs_api, normalize_usajobs_job


def run(
    keywords: Optional[str] = "Software Engineer",
    page: Optional[int] = None,
) -> int:
    """Fetch jobs from USAJobs and insert into MongoDB. Returns count inserted."""
    print("USAJobs → MongoDB")
    print("=" * 50)
    data = test_usajobs_api(keywords=keywords, page=page)
    items = data.get("SearchResult", {}).get("SearchResultItems", [])
    print(f"Retrieved {len(items)} job postings from USAJobs.")
    if not items:
        print("No jobs to insert.")
        return 0
    collection = get_mongo_collection()
    count = insert_jobs_into_mongo(
        items, collection, source="USAJobs", normalizer=normalize_usajobs_job
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
