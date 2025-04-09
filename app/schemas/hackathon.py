from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime
from app.schemas.organizer import OrganizerOut
from app.schemas.tech_focus import TechFocusOut


# === HACKATHON ===

class HackathonBase(BaseModel):
    name: str
    online: bool
    website: Optional[HttpUrl]
    image: Optional[str]
    dates: Optional[str]
    place: Optional[str]

class HackathonOut(HackathonBase):
    id: int
    organizers: list[OrganizerOut]
    tech_focuses: list[TechFocusOut]

    model_config = {
        "from_attributes": True
    }

class HackathonCreate(HackathonBase):
    pass

class HackathonRead(HackathonBase):
    id: int
    created_at: datetime

class HackathonFilter(BaseModel):
    name: Optional[str] = None
    organizers: Optional[List[str]] = None
    tech_focuses: Optional[List[str]] = None
    online: Optional[bool] = None