from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User, Profile
from app.schemas.user import UserResponse
from app.utils import verify_telegram_auth
from app.auth.jwt import create_access_token

class TelegramAuthService:
    def login_with_telegram_from_query(self, request, db: Session) -> UserResponse:
        params = dict(request.query_params)

        # Проверка Telegram-подписи
        if not verify_telegram_auth(params):
            raise HTTPException(status_code=400, detail="Invalid Telegram authentication")

        username = params.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        # Поиск пользователя по username
        user = db.query(User).filter(User.username == username).first()

        if not user:
            # Если пользователь не найден, создаем нового
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)

            # Создаем профиль для нового пользователя
            profile = Profile(
                user_id=user.id,
                first_name=params.get("first_name"),
                last_name=params.get("last_name"),
                tg_link=f"https://t.me/{username}",
                photo_url=params.get("photo_url")
            )
            db.add(profile)
            db.commit()

        access_token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
            profile={
                "id": user.profile.id,
                "first_name": user.profile.first_name,
                "last_name": user.profile.last_name,
                "tg_link": user.profile.tg_link,
                "photo_url": user.profile.photo_url
            }
        )
        }
