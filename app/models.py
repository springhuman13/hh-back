from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP, func
from app.database import Base, relationship

class Hackathon(Base):
    __tablename__ = "hackathon"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    online = Column(Boolean)
    website = Column(String)
    image = Column(String)
    dates = Column(String)
    place = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    organizers = relationship(
        "Organizer",
        secondary="organizer_to_hackathon",
        back_populates="hackathons"
    )

    tech_focuses = relationship(
        "TechFocus",
        secondary="tech_focus_to_hackathon",
        back_populates="hackathons"
    )

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    first_name = Column(String)
    last_name = Column(String)
    role_id = Column(Integer, ForeignKey("role.id"))
    bio = Column(String)
    git_link = Column(String)
    tg_link = Column(String)

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    hackathon_id = Column(Integer, ForeignKey("hackathon.id"))
    leader_id = Column(Integer, ForeignKey("user.id"))
    description = Column(String)
    city_id = Column(Integer, ForeignKey("city.id"))

class TeamMember(Base):
    __tablename__ = "team_member"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    team_id = Column(Integer, ForeignKey("team.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
    joined_at = Column(TIMESTAMP, server_default=func.now())

class ApplicationStatus(Base):
    __tablename__ = "application_status"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    team_id = Column(Integer, ForeignKey("team.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    status_id = Column(Integer, ForeignKey("application_status.id"))
    message = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class TechFocus(Base):
    __tablename__ = "tech_focus"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    hackathons = relationship(
        "Hackathon",
        secondary="tech_focus_to_hackathon",
        back_populates="tech_focuses"
    )

class Organizer(Base):
    __tablename__ = "organizer"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    
    hackathons = relationship(
        "Hackathon",
        secondary="organizer_to_hackathon",
        back_populates="organizers"
    )

class OrganizerToHackathon(Base):
    __tablename__ = "organizer_to_hackathon"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    organizer_id = Column(Integer, ForeignKey("organizer.id"))
    hachathon_id = Column(Integer, ForeignKey("hackathon.id"))

class TechFocusToHackathon(Base):
    __tablename__ = "tech_focus_to_hackathon"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    tf_id = Column(Integer, ForeignKey("tech_focus.id"))
    hachathon_id = Column(Integer, ForeignKey("hackathon.id"))

class TechFocusToUser(Base):
    __tablename__ = "tech_focus_to_user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    tf_id = Column(Integer, ForeignKey("tech_focus.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

class CheckList(Base):
    __tablename__ = "check_list"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

class CheckListToRole(Base):
    __tablename__ = "check_list_to_role"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cl_id = Column(Integer, ForeignKey("check_list.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

class CheckListPoint(Base):
    __tablename__ = "check_list_point"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    description = Column(String)
    cl_id = Column(Integer, ForeignKey("check_list.id"))

class CheckListToUser(Base):
    __tablename__ = "check_list_to_user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cl_id = Column(Integer, ForeignKey("check_list.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    grade = Column(Integer)

class CheckListToTeamMember(Base):
    __tablename__ = "check_list_to_team_member"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cl_id = Column(Integer, ForeignKey("check_list.id"))
    tm_id = Column(Integer, ForeignKey("team_member.id"))
    grade = Column(Integer)