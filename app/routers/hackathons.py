from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.parsers import parse_hackathon

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/parse/")
def parse_hackathon_endpoint(url: str, db: Session = Depends(get_db)):
    return parse_hackathon(url, db)
