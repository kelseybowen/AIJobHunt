"""
Adzuna API → MongoDB ingestion (Top 25 Computer Science Jobs).

Fetches job postings from the Adzuna API for the top 25 CS job titles,
normalizes them, and inserts into a MongoDB collection.

Uses MONGODB_CONNECT_STRING and PROD_DB from environment (.env).
Collection name defaults to data-ingestion-api (override with MONGO_JOBS_COLLECTION).

Run from project root:
  python -m backend.app.api.adzuna.adzuna_top25_to_mongo
Or from backend/app/api/adzuna:
  python adzuna_top25_to_mongo.py
"""

import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from backend/.env
_env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path=_env_path)

# Import existing Adzuna top-25 fetch and normalize logic
try:
    from backend.app.api.adzuna.test_adzuna_api_top25 import (
        fetch_all_top_jobs,
        normalize_adzuna_job,
        TOP_25_JOBS,
    )
except ImportError:
    from test_adzuna_api_top25 import (
        fetch_all_top_jobs,
        normalize_adzuna_job,
        TOP_25_JOBS,
    )


def get_mongo_collection():
    """Build MongoDB client and return the jobs collection (sync)."""
    uri = os.getenv("MONGODB_CONNECT_STRING")
    if not uri:
        raise ValueError(
            "MONGODB_CONNECT_STRING is not set. Add it to your .env file."
        )
    db_name = os.getenv("PROD_DB", "aijobhunt_db_test")
    collection_name = os.getenv("MONGO_JOBS_COLLECTION", "data-ingestion-api_adzuna")

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection


def insert_jobs_into_mongo(
    jobs: List[Dict[str, Any]],
    collection,
    source: str = "adzuna_top25",
) -> int:
    """
    Normalize job records and insert them into MongoDB.
    Adds source and ingested_at to each document.
    Returns the number of documents inserted.
    """
    if not jobs:
        return 0

    normalized = [normalize_adzuna_job(job) for job in jobs]
    now = datetime.now(timezone.utc)

    docs = []
    for doc in normalized:
        doc["source"] = source
        doc["ingested_at"] = now
        docs.append(doc)

    result = collection.insert_many(docs)
    return len(result.inserted_ids)


def run(
    job_titles: Optional[List[str]] = None,
    results_per_page: int = 50,
    max_pages_per_job: int = 1,
) -> int:
    """
    Fetch jobs from Adzuna for the top 25 (or given) job titles, then insert into MongoDB.
    Returns the number of documents inserted.
    """
    print("Adzuna → MongoDB (Top 25 Computer Science Jobs)")
    print("=" * 50)

    all_jobs = fetch_all_top_jobs(
        job_titles=job_titles or TOP_25_JOBS,
        results_per_page=results_per_page,
        max_pages_per_job=max_pages_per_job,
    )
    print(f"Retrieved {len(all_jobs)} job postings from Adzuna.")

    if not all_jobs:
        print("No jobs to insert.")
        return 0

    collection = get_mongo_collection()
    count = insert_jobs_into_mongo(all_jobs, collection, source="adzuna_top25")
    print(f"Inserted {count} documents into MongoDB.")
    return count


if __name__ == "__main__":
    try:
        run(
            job_titles=TOP_25_JOBS,
            results_per_page=50,
            max_pages_per_job=1,
        )
        print("Done.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        raise
