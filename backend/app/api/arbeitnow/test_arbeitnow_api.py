"""
Test API Call for Arbeitnow
Endpoint: GET https://www.arbeitnow.com/api/job-board-api

This file demonstrates how to make a test API call to Arbeitnow
and includes sample response data with all required fields.
Type: Job aggregator API
Auth: None
Coverage: European companies and remote roles
"""

import requests
import json
import csv
import os
import re
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from backend.app.api.job_schema import export_canonical_to_csv
except ImportError:
    import sys
    _api = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if _api not in sys.path:
        sys.path.insert(0, _api)
    from job_schema import export_canonical_to_csv


def test_arbeitnow_api(page: Optional[int] = None, 
                       remote_only: bool = True,
                       keywords: Optional[str] = None,
                       salary_min: Optional[int] = None,
                       salary_max: Optional[int] = None) -> Dict[str, Any]:
    """
    Make a test API call to Arbeitnow endpoint.
    
    Args:
        page: Optional page number for pagination
        remote_only: Filter to only return remote jobs (default: True)
        keywords: Optional search keywords (default: "Software Engineer")
        salary_min: Optional minimum salary filter; no filter when None
        salary_max: Optional maximum salary filter; no filter when None
    
    Returns:
        Dictionary containing job postings from Arbeitnow API (filtered to remote only if requested)
    """
    try:
        url = 'https://www.arbeitnow.com/api/job-board-api'
        params = {}
        if page:
            params['page'] = page
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Filter for remote jobs, keywords, and optional salary range
        if 'data' in data:
            filtered_jobs = []
            search_term = (keywords or "Software Engineer").lower()
            min_salary = salary_min
            max_salary = salary_max
            
            for job in data['data']:
                # Filter by remote
                if remote_only and not job.get('remote', False):
                    continue
                
                # Filter by keywords in title
                title = job.get('title', '').lower()
                if search_term not in title and 'software engineer' not in title:
                    continue
                
                # Filter by salary only when both min and max are set (Arbeitnow may not have salary in all jobs)
                if min_salary is not None and max_salary is not None:
                    job_salary = job.get('salary_min') or job.get('salary_max')
                    if job_salary is not None and (job_salary < min_salary or job_salary > max_salary):
                        continue
                
                filtered_jobs.append(job)
            
            data['data'] = filtered_jobs
        
        return data
    except requests.exceptions.RequestException as error:
        print(f'Error calling Arbeitnow API: {error}')
        raise


def normalize_arbeitnow_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize Arbeitnow job data to include all mapped fields.
    
    Args:
        job: Raw job data from Arbeitnow API
    
    Returns:
        Normalized job data with all required fields
    """
    # Normalize tags
    tags = job.get('tags', [])
    tags_str = '; '.join(tags) if isinstance(tags, list) else str(tags)
    
    # Clean description
    description = job.get('description', '')
    clean_description = re.sub(r'<[^>]+>', '', description)
    clean_description = ' '.join(clean_description.split())
    
    return {
        'Company': job.get('company_name', 'N/A'),
        'Position': job.get('title', 'N/A'),
        'Location': job.get('location', 'Remote'),
        'Tags': tags_str,
        'Description': clean_description,
        'URL': job.get('url', 'N/A'),
        'Salary_Min': job.get('salary_min', ''),
        'Salary_Max': job.get('salary_max', ''),
        'Date': job.get('published_at', 'N/A'),
        'ID': job.get('id', 'N/A')
    }


def export_to_csv(jobs: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
    """Export job postings to CSV using the canonical schema (same as MongoDB)."""
    if not jobs:
        print("No jobs to export")
        return ""
    csv_dir = os.path.join(os.path.dirname(__file__), "csv")
    filepath = export_canonical_to_csv(
        jobs, source="Arbeitnow", normalizer=normalize_arbeitnow_job,
        csv_dir=csv_dir, filename=filename, file_prefix="arbeitnow",
    )
    print(f"Exported {len(jobs)} job postings to {filepath}")
    return filepath


# Response shape: data array of jobs with id, title, company_name, location, remote, tags, description, url, salary_min, salary_max.


if __name__ == "__main__":
    # Example usage: Software Engineer, Remote (no salary range filter)
    try:
        result = test_arbeitnow_api(
            page=1,
            remote_only=True,
            keywords="Software Engineer",
            salary_min=None,
            salary_max=None
        )
        jobs = result.get("data", [])
        print(f"Retrieved {len(jobs)} Software Engineer remote job postings")
        
        # Export to CSV
        if jobs:
            csv_file = export_to_csv(jobs)
            if csv_file:
                print(f"\nCSV file created: {csv_file}")
        
        print(json.dumps(jobs[:2], indent=2))  # Print first 2 jobs
    except Exception as e:
        print(f"Test failed: {e}")

