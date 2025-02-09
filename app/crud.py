from sqlalchemy.orm import Session
from app.models import Hackathon, TechFocus

def create_hackathon(db: Session, title: str, description: str, link: str):
    hackathon = Hackathon(title=title, description=description, link=link)
    db.add(hackathon)
    db.commit()
    db.refresh(hackathon)
    return hackathon