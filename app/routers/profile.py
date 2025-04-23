from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import uuid4
import boto3
from botocore.config import Config

from app.auth.jwt import decode_access_token
from app.database import get_db
from app.models import User, Certificate
from app.schemas.user import UserResponse
from app.schemas.profile import ProfileUpdate, ProfileUpdateGit, GitResponse, InterestsResponse
from app.service.profile_service import ProfileService
from app.service.s3_service import S3ServiceDep
from app.core.config import settings
from app.dependencies.auth import get_current_user

router = APIRouter()

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

@router.get("/get_interests")
async def get_interests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = ProfileService(db)
    return service.get_interests(current_user)

@router.post("/update_interests")
async def update_interests(
    data: InterestsResponse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ProfileService(db)
    return service.update_interests(current_user, data.interests)

@router.post("/upload_certificate")
async def upload_certificate(
    s3: S3ServiceDep,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    s3.upload_file(file, user.id, db)
    return {"status": "success"}

@router.get("/get_certificates")
async def get_certificates(
    s3: S3ServiceDep,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return s3.get_all(user, db)