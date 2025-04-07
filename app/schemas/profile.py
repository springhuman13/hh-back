from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === PROFILE ===

class ProfileBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: Optional[int]
    bio: Optional[str]
    git_link: Optional[str]
    tg_link: Optional[str]

class ProfileCreate(ProfileBase):
    user_id: int

class ProfileRead(ProfileBase):
    id: int