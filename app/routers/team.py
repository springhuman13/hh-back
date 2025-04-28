from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import User
from app.schemas.team import TeamCreate, TeamResponse, TeamFilter, UserProfile
from app.service.team_service import TeamServiceDep
from app.dependencies.auth import get_current_user, get_optional_current_user

router = APIRouter()

@router.post("/create_team")
def create_team(
    team_service: TeamServiceDep,
    team_data: TeamCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return team_service.create_team(
        data=team_data,
        db=db,
        user=user,
    )

@router.get("/get_all", response_model=list[TeamResponse])
def get_all_teams(
    team_service: TeamServiceDep,
    db: Session = Depends(get_db),
):
    return team_service.get_all_teams(db=db)

@router.post("/get_filtered", response_model=list[TeamResponse])
async def get_filtered_teams(
    team_service: TeamServiceDep,
    filters: TeamFilter,
    user: Optional[UserProfile] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    return team_service.get_filtered_team(user=user, filters=filters, db=db)
