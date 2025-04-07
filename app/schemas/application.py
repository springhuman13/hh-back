from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === APPLICATION ===

class ApplicationBase(BaseModel):
    team_id: int
    user_id: int
    status_id: int
    message: Optional[str]

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationRead(ApplicationBase):
    id: int
    created_at: datetime