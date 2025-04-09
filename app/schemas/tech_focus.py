from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TECH FOCUS ===

class TechFocusBase(BaseModel):
    name: str

class TechFocusCreate(TechFocusBase):
    pass

class TechFocusRead(TechFocusBase):
    id: int

class TechFocusOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }