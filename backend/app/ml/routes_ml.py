from fastapi import APIRouter, HTTPException, Body
from jinja2.filters import async_select_or_reject
from pydantic import BaseModel, Field
from typing import List, Optional
from logic import JobMatcher

router = APIRouter()

# Initialize ML Engine
try:
    matcher = JobMatcher()
    print("ML Model loaded successfully.")
except Exception as e:
    print(f"Failed to load ML Model: {e}")
    matcher = None

# --- Pydantic Models
class UserPreferences(BaseModel):
    desired_locations: List[str] = []
    target_roles: List[str] = []
    skills: List[str] = []
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None

class RecommendationRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user requesting matches")
    preferences: UserPreferences

# --- API Endpoints ---

@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    """
    Generates job recommendations based on user preferences.
    Args:
        request: dict

    Returns:
    """

    if matcher is None:
        raise HTTPException(status_code=503, detail="ML Service unavailable")

    try:
        # Run logic
        # Convert Pydantic model to dict for the logic handler
        matches = matcher.recommend(request.preferences.model_dump(), top_n=10)

        return {
            "status": "success",
            "count": len(matches),
            "matches": matches
        }

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=503, detail="Internal processing error")