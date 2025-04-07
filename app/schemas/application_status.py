from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === APPLICATION STATUS ===

class ApplicationStatusBase(BaseModel):
    name: str

class ApplicationStatusCreate(ApplicationStatusBase):
    pass

class ApplicationStatusRead(ApplicationStatusBase):
    id: int