from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas.user import UserResponse
from app.schemas.profile import ProfileUpdate, ProfileUpdateGit, GitResponse, InterestsResponse, SkillsUpdateRequest, SkillChecklistGrouped, ProfileResponse, OtherUserProfileResponse
from app.service.profile_service import ProfileServiceDep
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
        profile=ProfileResponse.model_validate(current_user.profile)
    )

@router.post("/update_profile")
def update_profile(
    profile_service: ProfileServiceDep,
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile_service.update(user, db, **data.model_dump(exclude_unset=True))
    return {"status": "success"}

@router.post("/update_git")
def update_git(
    profile_service: ProfileServiceDep,
    data: ProfileUpdateGit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile_service.update(user, db, **data.model_dump(exclude_unset=True))
    return {"status": "success"}

@router.get("/get_git", response_model=GitResponse)
async def get_git(profile_service: ProfileServiceDep, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return profile_service.get_git(current_user, db)

@router.get("/get_interests")
async def get_interests(profile_service: ProfileServiceDep, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return profile_service.get_interests(current_user, db)

@router.post("/update_interests")
async def update_interests(
    profile_service: ProfileServiceDep,
    data: InterestsResponse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return profile_service.update_interests(current_user, data.interests, db)

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

@router.get("/get_skills", response_model=List[SkillChecklistGrouped])
async def get_skills(
    profile_service: ProfileServiceDep,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return profile_service.get_skills_grouped(user, db)

@router.post("/update_skills")
async def update_skills(
    profile_service: ProfileServiceDep,
    skills: SkillsUpdateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    profile_service.update_skills(user, skills.skills, db)
    return {"status": "success"}

@router.get("/{user_id}", response_model=OtherUserProfileResponse)
async def get_other_user_profile(
    profile_service: ProfileServiceDep,
    user_id: int,
    db: Session = Depends(get_db),
):
    return profile_service.get_other_user_profile(user_id=user_id, db=db)
    
