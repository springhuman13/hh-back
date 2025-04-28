from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

from app.schemas.tech_focus import TechFocusOut
from app.schemas.certificate import CertificateOut

# === PROFILE ===

class ProfileBase(BaseModel):
    id: int

class ProfileResponse(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_link: Optional[str] = None
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

class InterestsResponse(BaseModel):
    interests: List[int]

class SkillResponse(BaseModel):
    id: int
    description: str

class SkillsUpdateRequest(BaseModel):
    skills: List[int]

class SkillPoint(BaseModel):
    id: int
    description: str

class SkillChecklistGrouped(BaseModel):
    checklist_id: int
    name: str
    points: List[SkillPoint]

class OtherUserProfileResponse(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    photo_url: Optional[str]
    git: Optional[GitResponse]
    role_name: Optional[str]
    interests: List[TechFocusOut]
    skills: List[SkillPoint]
    certificates: List[CertificateOut]