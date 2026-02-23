"""
Test API Call for Adzuna - Top Jobs
Endpoint: GET https://api.adzuna.com/v1/api/jobs/us/search/{page}

This file searches for a configurable list of job titles (TOP_JOBS).
Type: Job aggregator API
Auth: API key required
"""

import requests
import json
import csv
import os
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file in backend directory
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

# Adzuna API Credentials
# Note: Adzuna requires BOTH app_id and app_key for authentication
# Loaded from environment variables
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")

# Top job titles and normalizer (shared with adzuna_top_jobs_to_mongo)
try:
    from backend.app.api.top_jobs import TOP_JOBS
    from backend.app.api.job_schema import export_canonical_to_csv
    from backend.app.api.adzuna.test_adzuna_api import normalize_adzuna_job
except ImportError:
    import sys
    _api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _api_dir not in sys.path:
        sys.path.insert(0, _api_dir)
    from top_jobs import TOP_JOBS
    from job_schema import export_canonical_to_csv
    from test_adzuna_api import normalize_adzuna_job


def search_adzuna_jobs(keywords: str, page: int = 1,
                       app_id: Optional[str] = None,
                       app_key: Optional[str] = None,
                       results_per_page: int = 50) -> Dict[str, Any]:
    """
    Make a single API call to Adzuna endpoint for a specific job title.
    """
    try:
        url = f'https://api.adzuna.com/v1/api/jobs/us/search/{page}'
        api_key = app_key or ADZUNA_API_KEY
        api_app_id = app_id or ADZUNA_APP_ID
        if not api_app_id:
            raise ValueError(
                "Adzuna API requires both app_id and app_key. "
                "Please provide an app_id parameter or set ADZUNA_APP_ID in the .env file."
            )
        if not api_key:
            raise ValueError(
                "Adzuna API requires both app_id and app_key. "
                "Please provide an app_key parameter or set ADZUNA_API_KEY in the .env file."
            )
        params = {
            'app_id': api_app_id,
            'app_key': api_key,
            'results_per_page': results_per_page,
            'what': keywords
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f'Error calling Adzuna API for "{keywords}": {error}')
        if error.response is not None:
            print(f'Response: {error.response.text}')
        return {'results': []}


def filter_jobs_by_top_titles(jobs: List[Dict[str, Any]], job_titles: List[str]) -> List[Dict[str, Any]]:
    """Filter jobs to only include those matching the top job titles."""
    filtered = []
    title_keywords = [title.upper() for title in job_titles]
    for job in jobs:
        job_title = job.get('title', '').upper()
        for keyword in title_keywords:
            keyword_parts = keyword.split()
            if len(keyword_parts) > 1:
                if all(part in job_title for part in keyword_parts if len(part) > 2):
                    filtered.append(job)
                    break
            else:
                if keyword in job_title:
                    filtered.append(job)
                    break
    return filtered


def fetch_all_top_jobs(job_titles: List[str] = None,
                       app_id: Optional[str] = None,
                       app_key: Optional[str] = None,
                       results_per_page: int = 50,
                       max_pages_per_job: int = 1) -> List[Dict[str, Any]]:
    """Fetch jobs for all top job titles. Dedupes by job id (same key as adzuna_fetch_top_jobs)."""
    if job_titles is None:
        job_titles = TOP_JOBS
    all_jobs = []
    seen_ids = set()
    total_jobs = len(job_titles)
    print(f"Searching for {total_jobs} top job titles...")
    print("=" * 60)
    for idx, job_title in enumerate(job_titles, 1):
        print(f"[{idx}/{total_jobs}] Searching for: {job_title}")
        try:
            for page in range(1, max_pages_per_job + 1):
                result = search_adzuna_jobs(
                    keywords=job_title,
                    page=page,
                    app_id=app_id,
                    app_key=app_key,
                    results_per_page=results_per_page
                )
                jobs = result.get('results', [])
                if jobs:
                    filtered = filter_jobs_by_top_titles(jobs, [job_title])
                    new_count = 0
                    for job in filtered:
                        job_id = job.get("id")
                        if job_id is not None and job_id not in seen_ids:
                            seen_ids.add(job_id)
                            all_jobs.append(job)
                            new_count += 1
                    print(f"  ✓ Found {len(filtered)} jobs (page {page}), {new_count} new unique")
                else:
                    if page == 1:
                        print(f"  ✗ No jobs found")
                    break
                if len(jobs) < results_per_page:
                    break
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    print("=" * 60)
    print(f"Total unique jobs retrieved: {len(all_jobs)}")
    return all_jobs


def export_to_csv(jobs: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
    """Export job postings to CSV using the canonical schema (same as MongoDB)."""
    if not jobs:
        print("No jobs to export")
        return ""
    csv_dir = os.path.join(os.path.dirname(__file__), "csv")
    filepath = export_canonical_to_csv(
        jobs, source="Adzuna", normalizer=normalize_adzuna_job,
        csv_dir=csv_dir, filename=filename, file_prefix="adzuna_top_jobs",
    )
    print(f"✓ Exported {len(jobs)} job postings to {filepath}")
    return filepath


def print_statistics(jobs: List[Dict[str, Any]]):
    """Print statistics about the retrieved jobs by job title."""
    if not jobs:
        return
    print("\n" + "=" * 60)
    print("JOB STATISTICS BY TITLE")
    print("=" * 60)
    title_counts = {}
    for job in jobs:
        title = job.get('title', 'Unknown')
        for top_title in TOP_JOBS:
            if top_title.upper() in title.upper():
                title_counts[top_title] = title_counts.get(top_title, 0) + 1
                break
        else:
            title_counts['Other'] = title_counts.get('Other', 0) + 1
    sorted_titles = sorted(title_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTotal jobs: {len(jobs)}")
    print(f"\nJobs by title category:")
    for title, count in sorted_titles[:15]:
        print(f"  {title}: {count}")
    jobs_with_salary = sum(1 for job in jobs if job.get('salary_min') or job.get('salary_max'))
    print(f"\nJobs with salary info: {jobs_with_salary} ({jobs_with_salary/len(jobs)*100:.1f}%)")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        print("Adzuna API - Top Jobs Search")
        print("=" * 60)
        all_jobs = fetch_all_top_jobs(
            job_titles=TOP_JOBS,
            results_per_page=50,
            max_pages_per_job=1
        )
        print_statistics(all_jobs)
        if all_jobs:
            csv_file = export_to_csv(all_jobs)
            if csv_file:
                print(f"\n✓ CSV file created: {csv_file}")
        print("\nSample jobs (first 3):")
        print(json.dumps(all_jobs[:3], indent=2))
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
