from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TEAM ===

class UserProfile(BaseModel):
    user_id: int
    selected_subskills: Optional[list[int]]
    tech_focuses: Optional[list[int]]       
    role_id: Optional[int]      

class ChecklistPointInput(BaseModel):
    checklist_point_id: int
    weight: int

class RoleInput(BaseModel):
    role_id: int
    checklist: List[ChecklistPointInput]

class TeamCreate(BaseModel):
    name: str
    hackathon_id: int
    city_id: int
    description: str
    roles: List[RoleInput]

class CityOut(BaseModel):
    id: int
    name: str

class TeamMemberInfo(BaseModel):
    id: int
    role_id: int
    role_name: str
    user_id: Optional[int]
    user_tg: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class TeamResponse(BaseModel):
    id: int
    name: str
    description: str
    city_name: str
    city_id: int
    hackathon_name: str
    hackathon_website: str
    hackathon_id: int
    members: List[TeamMemberInfo]
    score: Optional[float] = None

    model_config = {
        "from_attributes": True
    }

class TeamFilter(BaseModel):
    sort: int
    name: Optional[str] = None
    city: Optional[List[int]] = None
    hackathon: Optional[List[int]] = None
    role: Optional[List[int]] = None