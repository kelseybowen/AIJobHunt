from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserProfile(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )
    updated_at: Optional[datetime] = None  # Set default to None


class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )


class UserInDB(UserProfile):
    id: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "updated_at": user.get("updated_at"),
    }
