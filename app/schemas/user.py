from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

from app.schemas.profile import ProfileResponse

# === USER ===

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    profile: ProfileResponse

    model_config = {
        "from_attributes": True
    }