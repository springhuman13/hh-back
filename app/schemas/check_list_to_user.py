from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === CHECK LIST TO USER ===

class CheckListToUserBase(BaseModel):
    cl_id: int
    user_id: int
    grade: int

class CheckListToUserCreate(CheckListToUserBase):
    pass

class CheckListToUserRead(CheckListToUserBase):
    id: int