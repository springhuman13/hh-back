# app/routers/application.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.models import User
from app.database import get_db
from app.service.application_service import ApplicationServiceDep
from app.schemas.application import ApplicationSubmitRequest, ApplicationDecisionRequest 


router = APIRouter(
    
)

@router.post("/submit")
def submit_application(
    data: ApplicationSubmitRequest,
    application_service: ApplicationServiceDep,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return application_service.submit_application(data, user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/accept")
def accept_application(
    data: ApplicationDecisionRequest,
    application_service: ApplicationServiceDep,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return application_service.accept_application(data, user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decline")
def decline_application(
    data: ApplicationDecisionRequest,
    application_service: ApplicationServiceDep,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return application_service.decline_application(data, user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))