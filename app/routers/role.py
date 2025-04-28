from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Role, CheckList, CheckListToRole
from app.schemas.role import RoleOut


router = APIRouter()

@router.get("/get_all/", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role)
    return roles

@router.get("/get_checklist_for_role/{role_id}")
def get_checklist_for_role(role_id: int, db: Session = Depends(get_db)):
    checklists = (
        db.query(CheckList)
        .join(CheckListToRole)
        .filter(CheckListToRole.role_id == role_id)
        .all()
    )

    return [
        {
            "checklist_id": cl.id,
            "name": cl.name,
            "points": [{"id": p.id, "description": p.description} for p in cl.checklist_points],
        }
        for cl in checklists
    ]
