from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List

from app.database import get_db

from app.models import Hackathon, Organizer, TechFocus  # Модель SQLAlchemy

from app.schemas.hackathon import HackathonOut, HackathonFilter  # Pydantic-схема
from app.schemas.organizer import OrganizerOut
from app.schemas.tech_focus import TechFocusOut

from app.service.parsers import HackathonParser


router = APIRouter()

@router.post("/parse/")
def parse_hackathon_endpoint(db: Session = Depends(get_db)):
    parser = HackathonParser(db)
    parser.parse()

@router.post("/get-filtered/", response_model=List[HackathonOut])
def get_filtered_hackathons(filters: HackathonFilter, db: Session = Depends(get_db)):
    query = db.query(Hackathon).options(
        selectinload(Hackathon.organizers),
        selectinload(Hackathon.tech_focuses)
    )

    if filters.name is not None:
        query = query.filter(Hackathon.name.ilike(f"%{filters.name}%"))

    if filters.online is not None:
        query = query.filter(Hackathon.online == filters.online)

    if filters.organizers:
        query = query.filter(
            Hackathon.organizers.any(Organizer.id.in_(filters.organizers))
        )

    if filters.tech_focuses:
        query = query.filter(
            Hackathon.tech_focuses.any(TechFocus.id.in_(filters.tech_focuses))
        )

    return query.all()

@router.get("/hackathons/", response_model=list[HackathonOut])
def get_hackathons(db: Session = Depends(get_db)):
    hackathons = db.query(Hackathon)\
        .options(
            selectinload(Hackathon.organizers),
            selectinload(Hackathon.tech_focuses)
        ).all()
    return hackathons

@router.get("/organizers/", response_model=list[OrganizerOut])
def get_organizers(db: Session = Depends(get_db)):
    organizers = db.query(Organizer)
    return organizers

@router.get("/tech_focuses/", response_model=list[TechFocusOut])
def get_tech_focuses(db: Session = Depends(get_db)):
    tech_focuses = db.query(TechFocus).order_by(TechFocus.name).all()
    return tech_focuses
