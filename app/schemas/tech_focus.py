from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === TECH FOCUS ===
class TechFocusOut(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }