from bson import ObjectId
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError

from backend.db.mongo import get_db
from backend.models.userjobinteraction import (
    UserJobInteractionCreate,
    UserJobInteractionUpdate,
    UserJobInteractionInDB,
    userjobinteraction_helper,
)

router = APIRouter()


@router.post("/", response_model=UserJobInteractionInDB, status_code=201)
async def create_interaction(payload: UserJobInteractionCreate):

    db = get_db()

    if not ObjectId.is_valid(payload.user_id):
        raise HTTPException(400, "Invalid user_id")

    if not ObjectId.is_valid(payload.job_id):
        raise HTTPException(400, "Invalid job_id")

    user_oid = ObjectId(payload.user_id)
    job_oid = ObjectId(payload.job_id)

    if not await db.users.find_one({"_id": user_oid}):
        raise HTTPException(404, "User not found")

    if not await db.jobs.find_one({"_id": job_oid}):
        raise HTTPException(404, "Job not found")

    doc = payload.model_dump()

    doc["user_id"] = user_oid
    doc["job_id"] = job_oid
    doc["timestamp"] = datetime.now(timezone.utc)

    try:
        result = await db.user_job_interactions.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Interaction already exists",
        )

    created = await db.user_job_interactions.find_one(
        {"_id": result.inserted_id}
    )

    return userjobinteraction_helper(created)


@router.get("/user/{user_id}")
async def get_user_interactions(user_id: str):

    if not ObjectId.is_valid(user_id):
        raise HTTPException(400, "Invalid user ID")

    db = get_db()

    cursor = db.user_job_interactions.find(
        {"user_id": ObjectId(user_id)}
    )

    return [
        userjobinteraction_helper(doc)
        async for doc in cursor
    ]


@router.get("/job/{job_id}")
async def get_job_interactions(job_id: str):

    if not ObjectId.is_valid(job_id):
        raise HTTPException(400, "Invalid job ID")

    db = get_db()

    cursor = db.user_job_interactions.find(
        {"job_id": ObjectId(job_id)}
    )

    return [
        userjobinteraction_helper(doc)
        async for doc in cursor
    ]


@router.patch("/{interaction_id}")
async def update_interaction(
    interaction_id: str,
    payload: UserJobInteractionUpdate,
):

    if not ObjectId.is_valid(interaction_id):
        raise HTTPException(400, "Invalid interaction ID")

    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(400, "No fields provided")

    db = get_db()

    result = await db.user_job_interactions.update_one(
        {"_id": ObjectId(interaction_id)},
        {"$set": updates},
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Interaction not found")

    updated = await db.user_job_interactions.find_one(
        {"_id": ObjectId(interaction_id)}
    )

    return userjobinteraction_helper(updated)


@router.delete("/{interaction_id}", status_code=204)
async def delete_interaction(interaction_id: str):

    if not ObjectId.is_valid(interaction_id):
        raise HTTPException(400, "Invalid interaction ID")

    db = get_db()

    result = await db.user_job_interactions.delete_one(
        {"_id": ObjectId(interaction_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(404, "Interaction not found")
