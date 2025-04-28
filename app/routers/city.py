from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import City
from app.schemas.team import CityOut

router = APIRouter()

@router.get("/get_all/", response_model=list[CityOut])
def get_city(db: Session = Depends(get_db)):
    cities = db.query(City)
    return cities