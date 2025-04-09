from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserResponse
from app.schemas.auth import AuthResponse
from app.service.auth_service import TelegramAuthService

router = APIRouter()

auth_service = TelegramAuthService()

@router.get("/login-telegram", response_model=AuthResponse)
def login_with_telegram(request: Request, db: Session = Depends(get_db)):
    return auth_service.login_with_telegram_from_query(request, db)