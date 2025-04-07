from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TECH FOCUS TO HACKATHON ===

class TechFocusToHackathonBase(BaseModel):
    tf_id: int
    hachathon_id: int

class TechFocusToHackathonCreate(TechFocusToHackathonBase):
    pass

class TechFocusToHackathonRead(TechFocusToHackathonBase):
    id: int