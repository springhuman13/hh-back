from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

hackathon_focus_association = Table(
    "hackathon_focus",
    Base.metadata,
    Column("hackathon_id", Integer, ForeignKey("hackathons.id")),
    Column("focus_id", Integer, ForeignKey("tech_focus.id")),
)

class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    description = Column(String)
    link = Column(String, unique=True)

    focuses = relationship("TechFocus", secondary=hackathon_focus_association, back_populates="hackathons")

class TechFocus(Base):
    __tablename__ = "tech_focus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    hackathons = relationship("Hackathon", secondary=hackathon_focus_association, back_populates="focuses")