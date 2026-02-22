"""
HTTP endpoints to trigger top-jobs data pull (Adzuna, Jobicy, SerpAPI).
"""
import asyncio
from fastapi import APIRouter, HTTPException

router = APIRouter()


def _run_adzuna_top_jobs():
    from backend.app.api.adzuna.adzuna_top_jobs_to_mongo import run
    return run(results_per_page=50, max_pages_per_job=1)


def _run_jobicy_top_jobs():
    from backend.app.api.jobicy.jobicy_to_mongo import run
    return run(count_per_tag=100)


def _run_serpapi_top_jobs():
    from backend.app.api.serpapi.serpapi_to_mongo import run
    return run(location="United States", num=100)


@router.post("/adzuna/top-jobs")
async def trigger_adzuna_top_jobs():
    """Trigger Adzuna top-jobs ingestion. Returns count inserted."""
    try:
        loop = asyncio.get_event_loop()
        count = await loop.run_in_executor(None, _run_adzuna_top_jobs)
        return {"source": "Adzuna", "inserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobicy/top-jobs")
async def trigger_jobicy_top_jobs():
    """Trigger Jobicy top-jobs ingestion. Returns count inserted."""
    try:
        loop = asyncio.get_event_loop()
        count = await loop.run_in_executor(None, _run_jobicy_top_jobs)
        return {"source": "Jobicy", "inserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/serpapi/top-jobs")
async def trigger_serpapi_top_jobs():
    """Trigger SerpAPI top-jobs ingestion. Returns count inserted."""
    try:
        loop = asyncio.get_event_loop()
        count = await loop.run_in_executor(None, _run_serpapi_top_jobs)
        return {"source": "SerpAPI", "inserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
