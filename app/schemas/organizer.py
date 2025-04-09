from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

class OrganizerOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }