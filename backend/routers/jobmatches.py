from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError

from backend.db.mongo import get_db
from backend.models.jobmatch import (
    JobMatchCreate,
    JobMatchUpdate,
    JobMatchInDB,
    jobmatch_helper,
)

router = APIRouter()


@router.post("/", response_model=JobMatchInDB, status_code=201)
async def create_job_match(payload: JobMatchCreate):

    db = get_db()

    if not ObjectId.is_valid(payload.user_id):
        raise HTTPException(400, "Invalid user ID")

    if not ObjectId.is_valid(payload.job_id):
        raise HTTPException(400, "Invalid job ID")

    if not await db.users.find_one({"_id": ObjectId(payload.user_id)}):
        raise HTTPException(404, "User not found")

    if not await db.jobs.find_one({"_id": ObjectId(payload.job_id)}):
        raise HTTPException(404, "Job not found")

    doc = payload.model_dump()
    doc["user_id"] = ObjectId(payload.user_id)
    doc["job_id"] = ObjectId(payload.job_id)

    try:
        result = await db.job_matches.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Job match already exists for this user and job",
        )

    doc["matched_at"] = datetime.now(timezone.utc)
    created = await db.job_matches.find_one(
        {"_id": result.inserted_id}
    )

    return jobmatch_helper(created)


@router.get("/user/{user_id}", response_model=List[JobMatchInDB])
async def get_matches_for_user(user_id: str):

    db = get_db()

    if not ObjectId.is_valid(user_id):
        raise HTTPException(400, "Invalid user ID")

    matches = []

    async for doc in db.job_matches.find(
        {"user_id": ObjectId(user_id)}
    ):
        matches.append(jobmatch_helper(doc))

    return matches


@router.patch("/{match_id}", response_model=JobMatchInDB)
async def update_job_match(match_id: str, updates: JobMatchUpdate):

    db = get_db()

    if not ObjectId.is_valid(match_id):
        raise HTTPException(400, "Invalid match ID")

    update_data = {
        k: v for k, v in updates.model_dump(exclude_unset=True).items()
    }

    if not update_data:
        raise HTTPException(400, "No fields provided for update")

    result = await db.job_matches.update_one(
        {"_id": ObjectId(match_id)},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Match not found")

    updated = await db.job_matches.find_one(
        {"_id": ObjectId(match_id)}
    )

    return jobmatch_helper(updated)


@router.delete("/{match_id}", status_code=204)
async def delete_job_match(match_id: str):

    db = get_db()

    if not ObjectId.is_valid(match_id):
        raise HTTPException(400, "Invalid match ID")

    result = await db.job_matches.delete_one(
        {"_id": ObjectId(match_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(404, "Match not found")
