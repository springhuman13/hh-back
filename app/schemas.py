from pydantic import BaseModel
from typing import List, Optional

class HackathonSchema(BaseModel):
    id: int
    title: str
    img: str
    description: str 
    link: str
    place: Optional[str] = None
    dates: Optional[str] = None
    organizers: Optional[str] = None
    tech_focus: Optional[str] = None

class HackathonOut(BaseModel):
    title: str
    link: str
    img: str
    place: Optional[str] = None
    dates: Optional[str] = None
    organizers: Optional[str] = None
    tech_focus: Optional[str] = None

    class Config:
        from_attributes = True