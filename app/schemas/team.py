from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TEAM ===

class TeamBase(BaseModel):
    name: str
    hackathon_id: int
    leader_id: int
    description: Optional[str]
    city_id: Optional[int]

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int