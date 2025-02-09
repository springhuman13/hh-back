from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.parsers import parse_hackathons
from app.models import Hackathon  # Модель SQLAlchemy
from app.schemas import HackathonOut  # Pydantic-схема

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/parse/")
def parse_hackathon_endpoint(url: str, db: Session = Depends(get_db)):
    return parse_hackathons(url, db)

@router.get("/hackathons/", response_model=list[HackathonOut])
def get_hackathons(db: Session = Depends(get_db)):
    hackathons = db.query(Hackathon).all() 
    return [HackathonOut.model_validate(hackathon) for hackathon in hackathons]
