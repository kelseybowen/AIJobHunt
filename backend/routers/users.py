from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from backend.db.mongo import get_db
from backend.models.user import (
    UserProfile,
    UserProfileUpdate,
    UserInDB,
    user_helper,
)
from datetime import datetime, timezone

router = APIRouter()


@router.post("/", response_model=UserInDB, status_code=201)
async def create_user(user: UserProfile):
    db = get_db()
    result = await db.users.insert_one(user.model_dump())

    new_user = await db.users.find_one(
        {"_id": result.inserted_id}
    )

    return user_helper(new_user)


@router.get("/", response_model=List[UserInDB])
async def get_users():
    db = get_db()
    users = []

    async for user in db.users.find():
        users.append(user_helper(user))

    return users


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str):
    db = get_db()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = await db.users.find_one(
        {"_id": ObjectId(user_id)}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user_helper(user)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, updates: UserProfileUpdate):
    db = get_db()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    update_data = {
        k: v for k, v in updates.model_dump().items()
        if v is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    update_data["updated_at"] = datetime.now(timezone.utc)

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await db.users.find_one(
        {"_id": ObjectId(user_id)}
    )

    return user_helper(updated_user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    db = get_db()

    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    result = await db.users.delete_one(
        {"_id": ObjectId(user_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
