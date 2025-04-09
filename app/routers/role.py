from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List

from app.database import get_db

from app.models import Role
from app.schemas.role import RoleOut


router = APIRouter()

@router.get("/get_all/", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role)
    return roles
