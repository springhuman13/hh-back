from sqlalchemy.orm import Session
from app.models import Hackathon, TechFocus

def create_hackathon(db: Session, title: str, description: str, link: str, focuses: list):
    hackathon = Hackathon(title=title, description=description, link=link)

    for focus_name in focuses:
        focus = db.query(TechFocus).filter_by(name=focus_name).first()
        if not focus:
            focus = TechFocus(name=focus_name)
            db.add(focus)
        hackathon.focuses.append(focus)

    db.add(hackathon)
    db.commit()
    db.refresh(hackathon)
    return hackathon