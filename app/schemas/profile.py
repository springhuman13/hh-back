from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

from app.schemas.team import TeamOut
from app.schemas.tech_focus import TechFocusOut

# === PROFILE ===

class ProfileBase(BaseModel):
    id: int

class ProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_link: str
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    role_id: Optional[int] = None
    git_link: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ProfileUpdate(BaseModel):
    role_id: Optional[int] = None
    bio: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ProfileUpdateGit(BaseModel):
    git_link: str

    model_config = {
        "from_attributes": True
    }

class GitResponse(BaseModel):
    username: Optional[str] = None
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None

    model_config = {
        "from_attributes": True
    }