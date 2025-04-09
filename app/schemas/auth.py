from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserResponse


class TelegramLoginRequest(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse