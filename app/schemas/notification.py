from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationOut(BaseModel):
    id: int
    message: str
    link: Optional[str] = None
    type: str
    is_read: bool
    created_at: datetime
    application_id: int
    model_config = {
        "from_attributes": True
    }
