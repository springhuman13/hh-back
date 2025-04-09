from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === PROFILE ===

class ProfileBase(BaseModel):
    id: int

class ProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_link: str
    photo_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ProfileOut(BaseModel):
    role_id: Optional[int]
    bio: Optional[str]
    git_link: Optional[str]

    model_config = {
        "from_attributes": True
    }