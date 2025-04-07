from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === CITY ===

class CityBase(BaseModel):
    name: str

class CityCreate(CityBase):
    pass

class CityRead(CityBase):
    id: int