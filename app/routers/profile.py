from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import decode_access_token
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.user import UserResponse
from app.schemas.profile import ProfileUpdate, ProfileUpdateGit, GitResponse
from app.service.profile_service import ProfileService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me")
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        created_at=current_user.created_at,
        profile={
            "id": current_user.profile.id,
            "first_name": current_user.profile.first_name,
            "last_name": current_user.profile.last_name,
            "tg_link": current_user.profile.tg_link,
            "photo_url": current_user.profile.photo_url,
            "bio": current_user.profile.bio,
            "role_id": current_user.profile.role_id,
            "git_link": current_user.profile.git_link,
        }
    )

@router.post("/update_profile")
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ProfileService(db)
    profile = service.update(user, **data.model_dump(exclude_unset=True))
    return {"status": "success"}

@router.post("/update_git")
def update_git(
    data: ProfileUpdateGit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ProfileService(db)
    profileGit = service.update(user, **data.model_dump(exclude_unset=True))
    return {"status": "success"}

@router.get("/get_git", response_model=GitResponse)
async def get_git(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ProfileService(db)
    return service.get_git(current_user)
