from sqlalchemy.orm import Session
from app.models import Hackathon, TechFocus, TechFocusToHackathon, Organizer, OrganizerToHackathon
from typing import Optional


class HackathonService:
    def __init__(self, db: Session):
        self.db = db

    def process_hackathon(
        self,
        title: str,
        link: str,
        img: str,
        online: bool,
        place: Optional[str] = None,
        dates: Optional[str] = None,
        organizers: Optional[str] = None,
        tech_focus: Optional[str] = None
    ) -> str:
        
        hackathon = self._create_hackathon(
            name=title,
            website=link,
            image=img,
            online=online,
            place=place,
            dates=dates
        )

        if tech_focus:
            tf_ids = self._create_tech_focuses(tech_focus)
            self._create_tech_focuses_to_hackathon(tf_ids, hackathon.id)

        if organizers:
            organizer_ids = self._create_organizers(organizers)
            self._create_organizers_to_hackathon(organizer_ids, hackathon.id)
            

        return "success"

    def _create_hackathon(
        self,
        name: str,
        website: str,
        image: str,
        online: bool,
        place: Optional[str],
        dates: Optional[str]
    ) -> Hackathon:
        hackathon = Hackathon(
            name=name,
            website=website,
            image=image,
            online=online,
            place=place,
            dates=dates,
        )
        self.db.add(hackathon)
        self.db.commit()
        self.db.refresh(hackathon)
        return hackathon

    def _create_tech_focuses(self, tech_focus_str: str) -> list[int]:
        tf_ids = []
        tech_focuses = [p.strip() for p in tech_focus_str.split(',') if p.strip()]
        for tf_name in tech_focuses:
            existing = self.db.query(TechFocus).filter_by(name=tf_name).first()
            if existing:
                tf_ids.append(existing.id)
                continue

            tf = TechFocus(name=tf_name)
            self.db.add(tf)
            self.db.commit()
            self.db.refresh(tf)
            tf_ids.append(tf.id)
        return tf_ids

    def _create_tech_focuses_to_hackathon(self, tf_ids: list[int], hackathon_id: int):
        for tf_id in tf_ids:
            exists = self.db.query(TechFocusToHackathon).filter_by(
                tf_id=tf_id, hachathon_id=hackathon_id
            ).first()
            if exists:
                continue

            link = TechFocusToHackathon(tf_id=tf_id, hachathon_id=hackathon_id)
            self.db.add(link)
        self.db.commit()

    def _create_organizers(self, organizers_str: str) -> Organizer:
        organizers_ids = []
        organizers = [p.strip() for p in organizers_str.split(',') if p.strip()]
        for organizer_name in organizers:
            existing = self.db.query(Organizer).filter_by(name=organizer_name).first()
            if existing:
                organizers_ids.append(existing.id)
                continue

            org = Organizer(name=organizer_name)
            self.db.add(org)
            self.db.commit()
            self.db.refresh(org)
            organizers_ids.append(org.id)
        return organizers_ids

    def _create_organizers_to_hackathon(self, organizer_ids: list[int], hackathon_id: int):
        for organizer_id in organizer_ids:
            exists = self.db.query(OrganizerToHackathon).filter_by(
                organizer_id=organizer_id, hachathon_id=hackathon_id
            ).first()
            if exists:
                continue

            link = OrganizerToHackathon(organizer_id=organizer_id, hachathon_id=hackathon_id)
            self.db.add(link)
        self.db.commit()
