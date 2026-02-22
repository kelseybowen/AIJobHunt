from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class JobMatchBase(BaseModel):
    user_id: str
    job_id: str
    score: float = Field(..., ge=0.0, le=1.0)
    match_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    missing_skills: List[str] = []


class JobMatchCreate(JobMatchBase):
    pass


class JobMatchUpdate(BaseModel):
    score: Optional[float] = Field(None, ge=0.0, le=1.0)


class JobMatchInDB(JobMatchBase):
    id: str


def jobmatch_helper(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "user_id": str(doc["user_id"]),
        "job_id": str(doc["job_id"]),
        "score": doc["score"],
        "match_date": doc["match_date"],
        "missing_skills": doc["missing_skills"]
    }
