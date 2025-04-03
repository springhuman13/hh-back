from sqlalchemy import Column, String, Integer
from app.database import Base

class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    img = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    place = Column(String, nullable=True)
    dates = Column(String, nullable=True)
    organizers = Column(String, nullable=True)
    tech_focus = Column(String, nullable=True)
