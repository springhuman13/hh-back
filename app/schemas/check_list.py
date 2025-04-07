from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === CHECK LIST ===

class CheckListBase(BaseModel):
    name: str

class CheckListCreate(CheckListBase):
    pass

class CheckListRead(CheckListBase):
    id: int