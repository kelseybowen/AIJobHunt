"""
Adzuna API → MongoDB ingestion (single keyword).

Fetches job postings from the Adzuna API for a given keyword (e.g. "Software Engineer"),
normalizes them, and inserts into a MongoDB collection.

Uses MONGODB_CONNECT_STRING and PROD_DB from environment (.env).
Collection name defaults to data-ingestion-api (override with MONGO_JOBS_COLLECTION).

Run from project root:
  python -m backend.app.api.adzuna.adzuna_to_mongo
Or from backend/app/api/adzuna:
  python adzuna_to_mongo.py
"""

import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from backend/.env
_env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path=_env_path)

# Import existing Adzuna fetch and normalize logic
try:
    from backend.app.api.adzuna.test_adzuna_api import test_adzuna_api, normalize_adzuna_job
except ImportError:
    from test_adzuna_api import test_adzuna_api, normalize_adzuna_job


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
    source: str = "adzuna",
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
    keywords: Optional[str] = "Software Engineer",
    page: int = 1,
    results_per_page: int = 50,
) -> int:
    """
    Fetch jobs from Adzuna for the given keyword, then insert into MongoDB.
    Returns the number of documents inserted.
    """
    print("Adzuna → MongoDB (single keyword)")
    print("=" * 50)

    result = test_adzuna_api(
        page=page,
        keywords=keywords,
        results_per_page=results_per_page,
    )
    jobs = result.get("results", [])
    print(f"Retrieved {len(jobs)} job postings from Adzuna.")

    if not jobs:
        print("No jobs to insert.")
        return 0

    collection = get_mongo_collection()
    count = insert_jobs_into_mongo(jobs, collection, source="adzuna")
    print(f"Inserted {count} documents into MongoDB.")
    return count


if __name__ == "__main__":
    try:
        run(
            keywords="Software Engineer",
            page=1,
            results_per_page=50,
        )
        print("Done.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        raise
