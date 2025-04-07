from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === CHECK LIST POINT ===

class CheckListPointBase(BaseModel):
    description: str
    cl_id: int

class CheckListPointCreate(CheckListPointBase):
    pass

class CheckListPointRead(CheckListPointBase):
    id: int