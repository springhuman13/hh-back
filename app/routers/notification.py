# app/routers/notification.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models import Notification, User
from app.schemas.notification import NotificationOut
from typing import List

router = APIRouter()

@router.get("/get_all", response_model=List[NotificationOut])
def get_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()
    return notifications
