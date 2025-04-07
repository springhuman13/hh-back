from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TEAM MEMBER ===

class TeamMemberBase(BaseModel):
    team_id: int
    user_id: int
    role_id: int

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberRead(TeamMemberBase):
    id: int
    joined_at: datetime