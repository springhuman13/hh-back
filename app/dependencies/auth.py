from fastapi import Depends, HTTPException, Request
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_optional_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None

    scheme, _, param = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return None

    payload = decode_access_token(param)
    if payload is None:
        return None

    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    return user
