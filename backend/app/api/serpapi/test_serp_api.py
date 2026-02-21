"""
Test API Call for SerpAPI (Google Jobs)
Endpoint: GET https://serpapi.com/search.json?engine=google_jobs

This file demonstrates how to make a test API call to SerpAPI for Google Jobs search.
Type: Job search API (aggregates Google Jobs results)
Auth: API key required
Coverage: Google Jobs search results from various sources

Note: Requires the google-search-results package
Install with: pip install google-search-results
"""

import os
import sys

# This file lives under a folder named 'serpapi', which shadows the pip package.
# Prefer site-packages so "from serpapi import GoogleSearch" gets the real package.
_this_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_this_dir)
_n = lambda p: os.path.normcase(os.path.abspath(p))
_removed = []
for path in (_parent_dir, _this_dir):
    path_n = _n(path)
    for i, p in enumerate(sys.path):
        if _n(p) == path_n:
            sys.path.pop(i)
            _removed.append(path)
            break
# Ensure site-packages is searched before any remaining path that could shadow
_site_packages = getattr(sys, "path", [])
_site_packages = [p for p in sys.path if "site-packages" in _n(p)]
if _site_packages:
    for p in _site_packages:
        if p in sys.path:
            sys.path.remove(p)
    for p in reversed(_site_packages):
        sys.path.insert(0, p)
try:
    from serpapi import GoogleSearch
except ImportError:
    for p in reversed(_removed):
        sys.path.insert(0, p)
    print("Error: serpapi library not found.")
    print("Install in this environment with:")
    print("  .\\venv\\Scripts\\python.exe -m pip install google-search-results")
    raise
for p in reversed(_removed):
    sys.path.insert(0, p)

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

# SerpAPI Credentials
# Loaded from environment variables
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

try:
    from backend.app.api.job_schema import export_canonical_to_csv
    from backend.app.api.top_jobs import TOP_JOBS
    from backend.app.api.serpapi.serpapi_fetch_top_jobs import fetch_all_top_jobs
except ImportError:
    import sys
    _api = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _api not in sys.path:
        sys.path.insert(0, _api)
    from job_schema import export_canonical_to_csv
    from top_jobs import TOP_JOBS
    from serpapi_fetch_top_jobs import fetch_all_top_jobs


def test_serpapi_google_jobs(query: str = "Software Engineer",
                             location: str = "United States",
                             api_key: Optional[str] = None,
                             num: int = 100,
                             next_page_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Make a test API call to SerpAPI Google Jobs endpoint.
    
    Args:
        query: Search query (job title/keywords) (default: "Software Engineer")
        location: Location filter (default: "United States")
        api_key: SerpAPI API key (defaults to SERPAPI_API_KEY)
        num: Number of results to return (default: 100, max typically 100)
        next_page_token: Token for pagination (from previous response)
    
    Returns:
        Dictionary containing job postings from SerpAPI Google Jobs
        Structure: {"jobs_results": [list of jobs], "next_page_token": token for next page}
    
    Raises:
        ValueError: If api_key is not provided
    """
    try:
        # Use provided API key or default
        api_key_value = api_key or SERPAPI_API_KEY
        
        if not api_key_value:
            raise ValueError(
                "SerpAPI requires an API key. "
                "Please provide an api_key parameter or set SERPAPI_API_KEY in the .env file."
            )
        
        # Build search parameters
        # Note: Google Jobs API no longer supports 'start' parameter, use 'next_page_token' instead
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "google_domain": "google.com",
            "hl": "en",
            "gl": "us",
            "api_key": api_key_value,
            "num": num
        }
        
        # Add next_page_token if provided (for pagination)
        if next_page_token:
            params["next_page_token"] = next_page_token
        
        # Perform the search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Debug: Check what we got back
        if "error" in results:
            error_msg = results.get("error", "Unknown error")
            print(f"SerpAPI Error: {error_msg}")
            if "Invalid API key" in error_msg:
                raise ValueError("Invalid SerpAPI API key. Please check your API key.")
            raise Exception(f"SerpAPI API error: {error_msg}")
        
        # Extract jobs results
        jobs_results = results.get("jobs_results", [])
        
        # Extract pagination token - check multiple possible locations
        next_page_token = None
        if "pagination" in results:
            pagination = results.get("pagination", {})
            next_page_token = pagination.get("next_page_token") or pagination.get("next")
        elif "serpapi_pagination" in results:
            next_page_token = results.get("serpapi_pagination", {}).get("next_page_token")
        
        # Debug output
        if not jobs_results:
            print(f"Warning: No jobs_results found in response.")
            print(f"Response keys: {list(results.keys())}")
            if "search_information" in results:
                print(f"Search info: {results.get('search_information', {})}")
        
        return {
            "jobs_results": jobs_results,
            "search_metadata": results.get("search_metadata", {}),
            "search_parameters": results.get("search_parameters", {}),
            "next_page_token": next_page_token,
            "raw_response": results  # Include full response for debugging
        }
    except Exception as error:
        print(f'Error calling SerpAPI: {error}')
        import traceback
        traceback.print_exc()
        raise


def normalize_serpapi_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize SerpAPI Google Jobs data to include all mapped fields.
    
    Args:
        job: Raw job data from SerpAPI Google Jobs API
    
    Returns:
        Normalized job data with all required fields
    """
    # Extract job title
    job_title = job.get('title', 'N/A')
    
    # Extract company name
    company = job.get('company_name', 'N/A')
    
    # Extract location
    location = job.get('location', 'N/A')
    
    # Extract description
    description = job.get('description', '')
    if not description:
        # Try alternative description fields
        description = job.get('snippet', '') or job.get('job_highlights', {}).get('description', '')
    
    # Clean description - remove HTML tags and normalize whitespace
    if isinstance(description, str):
        clean_description = re.sub(r'<[^>]+>', '', description)
        clean_description = ' '.join(clean_description.split())
    elif isinstance(description, list):
        # If description is a list, join it
        clean_description = ' '.join([str(d) for d in description])
    else:
        clean_description = str(description) if description else ''
    
    # Extract URL
    url = job.get('apply_options', [{}])[0].get('link', '') if job.get('apply_options') else ''
    if not url:
        url = job.get('related_links', [{}])[0].get('link', '') if job.get('related_links') else ''
    if not url:
        url = job.get('link', 'N/A')
    
    # Extract salary/pay information
    salary_min = ''
    salary_max = ''
    
    # Try multiple sources for salary information
    salary_sources = [
        job.get('detected_extensions', {}).get('salary'),
        job.get('salary'),
        job.get('compensation', {}).get('base_salary', {}).get('value', {}).get('min_value'),
    ]
    
    for salary_data in salary_sources:
        if salary_data:
            salary_str = str(salary_data)
            # Try to parse salary range (e.g., "$100,000 - $150,000", "$100k - $150k")
            # Pattern 1: Full numbers with commas
            salary_range = re.findall(r'\$?([\d,]+)', salary_str)
            if len(salary_range) >= 2:
                salary_min = salary_range[0].replace(',', '')
                salary_max = salary_range[1].replace(',', '')
                break
            elif len(salary_range) == 1:
                salary_min = salary_range[0].replace(',', '')
                salary_max = salary_min
                break
            # Pattern 2: Numbers with 'k' suffix (e.g., "$100k - $150k")
            k_range = re.findall(r'\$?(\d+)k', salary_str, re.IGNORECASE)
            if len(k_range) >= 2:
                salary_min = str(int(k_range[0]) * 1000)
                salary_max = str(int(k_range[1]) * 1000)
                break
            elif len(k_range) == 1:
                salary_min = str(int(k_range[0]) * 1000)
                salary_max = salary_min
                break
    
    # Extract job highlights/tags
    job_highlights = job.get('job_highlights', [])
    tags = []
    if isinstance(job_highlights, list):
        for highlight in job_highlights:
            if isinstance(highlight, dict):
                tags.append(highlight.get('title', ''))
            else:
                tags.append(str(highlight))
    tags_str = '; '.join([tag for tag in tags if tag]) if tags else ''
    
    # Extract date (if available)
    date = job.get('posted_at', job.get('schedule_type', 'N/A'))
    
    # Extract job ID
    job_id = job.get('job_id', job.get('title', 'N/A'))
    
    return {
        'Company': company,
        'Position': job_title,
        'Location': location,
        'Tags': tags_str,
        'Description': clean_description,
        'URL': url,
        'Salary_Min': salary_min,
        'Salary_Max': salary_max,
        'Date': date,
        'ID': job_id
    }


def export_to_csv(jobs: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
    """Export job postings to CSV using the canonical schema (same as MongoDB)."""
    if not jobs:
        print("No jobs to export")
        return ""
    csv_dir = os.path.join(os.path.dirname(__file__), "csv")
    filepath = export_canonical_to_csv(
        jobs, source="SerpAPI", normalizer=normalize_serpapi_job,
        csv_dir=csv_dir, filename=filename, file_prefix="serpapi",
    )
    print(f"Exported {len(jobs)} job postings to {filepath}")
    return filepath


if __name__ == "__main__":
    # Same flow as serpapi_to_mongo: TOP_JOBS, fetch_all_top_jobs, then export to CSV
    try:
        print("SerpAPI Google Jobs - TOP_JOBS (same as serpapi_to_mongo)")
        print("=" * 60)
        jobs = fetch_all_top_jobs(job_titles=TOP_JOBS, location="United States", num=100)
        print(f"Retrieved {len(jobs)} unique job postings")
        if jobs:
            csv_file = export_to_csv(jobs)
            if csv_file:
                print(f"\nCSV file created: {csv_file}")
            print("\nSample jobs (first 2):")
            print(json.dumps(jobs[:2], indent=2))
        else:
            print("\nNo jobs found. This might indicate:")
            print("  - API key issue (check if key is valid)")
            print("  - Rate limit reached")
            print("  - No jobs match the search criteria")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
