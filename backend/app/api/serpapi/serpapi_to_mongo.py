"""
SerpAPI (Google Jobs) → MongoDB ingestion.

Fetches job postings from SerpAPI Google Jobs for the same TOP_JOBS list as Adzuna,
normalizes them, and appends to a MongoDB collection. Uses shared mongo_ingestion_utils.

Env: MONGODB_CONNECT_STRING, PROD_DB, MONGO_JOBS_COLLECTION (optional), SERPAPI_API_KEY.
Data source label: "SerpAPI".

Run from backend dir (use venv Python so dotenv/packages are available):
  .\\venv\\Scripts\\python.exe app\\api\\serpapi\\serpapi_to_mongo.py
Or activate venv first, then:  python app\\api\\serpapi\\serpapi_to_mongo.py
Run from project root:  python backend\\app\\api\\serpapi\\serpapi_to_mongo.py  (use backend venv)
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
    from backend.app.api.serpapi.test_serp_api import test_serpapi_google_jobs, normalize_serpapi_job
except ImportError:
    from test_serp_api import test_serpapi_google_jobs, normalize_serpapi_job

try:
    from backend.app.api.top_jobs import TOP_JOBS
except ImportError:
    import sys
    _api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _api_dir not in sys.path:
        sys.path.insert(0, _api_dir)
    from top_jobs import TOP_JOBS


def run(
    job_titles: Optional[List[str]] = None,
    location: str = "United States",
    num: int = 100,
) -> int:
    """Fetch jobs from SerpAPI for each title in TOP_JOBS (or given list), dedupe, and insert into MongoDB."""
    titles = job_titles or TOP_JOBS
    print("SerpAPI (Google Jobs) → MongoDB (Top Jobs)")
    print("=" * 50)
    all_jobs: List[Dict[str, Any]] = []
    seen_ids = set()
    total = len(titles)
    for idx, query in enumerate(titles, 1):
        print(f"[{idx}/{total}] Searching for: {query}")
        try:
            result = test_serpapi_google_jobs(query=query, location=location, num=num)
            jobs = result.get("jobs_results", [])
            for job in jobs:
                job_id = job.get("job_id") or job.get("title", "") + "|" + job.get("company_name", "")
                if job_id not in seen_ids:
                    seen_ids.add(job_id)
                    all_jobs.append(job)
            print(f"  ✓ Got {len(jobs)} results (total unique: {len(all_jobs)})")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    print("=" * 50)
    print(f"Retrieved {len(all_jobs)} unique job postings from SerpAPI.")
    if not all_jobs:
        print("No jobs to insert.")
        return 0
    collection = get_mongo_collection()
    count = insert_jobs_into_mongo(
        all_jobs, collection, source="SerpAPI", normalizer=normalize_serpapi_job
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
