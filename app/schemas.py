from pydantic import BaseModel
from typing import List, Optional

class TechFocusSchema(BaseModel):
    name: str

class HackathonSchema(BaseModel):
    title: str
    description: Optional[str] = None
    link: str
    focuses: List[TechFocusSchema] = []

class HackathonOut(BaseModel):
    title: str
    description: str
    link: str

    class Config:
        from_attributes = True