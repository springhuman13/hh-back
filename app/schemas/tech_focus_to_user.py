from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TECH FOCUS TO USER ===

class TechFocusToUserBase(BaseModel):
    tf_id: int
    user_id: int

class TechFocusToUserCreate(TechFocusToUserBase):
    pass

class TechFocusToUserRead(TechFocusToUserBase):
    id: int
