from sqlalchemy.orm import Session
from app.models import Hackathon

def create_hackathon(db: Session, title: str, description: str, link: str, img: str,
                    place: str = None, dates: str = None, 
                    organizers: str = None, tech_focus: str = None):
    db_hackathon = Hackathon(
        title=title,
        description=description,
        link=link,
        place=place,
        dates=dates,
        organizers=organizers,
        tech_focus=tech_focus,
        img = img
    )
    db.add(db_hackathon)
    db.commit()
    db.refresh(db_hackathon)
    return db_hackathon