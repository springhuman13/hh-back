from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
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
    created_at = Column(DateTime, default=func.now())

    organizers = relationship("Organizer", secondary="organizer_to_hackathon", back_populates="hackathons")
    tech_focuses = relationship("TechFocus", secondary="tech_focus_to_hackathon", back_populates="hackathons")
    teams = relationship("Team", back_populates="hackathon")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String)
    created_at = Column(DateTime, default=func.now())

    profile = relationship("Profile", back_populates="user", uselist=False)
    tech_focuses = relationship("TechFocus", secondary="tech_focus_to_user", back_populates="users")
    teams_led = relationship("Team", back_populates="leader")
    team_memberships = relationship("TeamMember", back_populates="user")
    applications = relationship("Application", back_populates="user")
    checklist_to_user = relationship("CheckListToUser", back_populates="user")

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
    photo_url = Column(String)

    user = relationship("User", back_populates="profile")
    role = relationship("Role", back_populates="profiles")

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    profiles = relationship("Profile", back_populates="role")
    team_members = relationship("TeamMember", back_populates="role")
    checklists = relationship("CheckListToRole", back_populates="role")

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    teams = relationship("Team", back_populates="city")

class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    hackathon_id = Column(Integer, ForeignKey("hackathon.id"))
    leader_id = Column(Integer, ForeignKey("user.id"))
    description = Column(String)
    city_id = Column(Integer, ForeignKey("city.id"))

    hackathon = relationship("Hackathon", back_populates="teams")
    leader = relationship("User", back_populates="teams_led")
    city = relationship("City", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")
    applications = relationship("Application", back_populates="team")

class TeamMember(Base):
    __tablename__ = "team_member"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    team_id = Column(Integer, ForeignKey("team.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
    joined_at = Column(DateTime, default=func.now())

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")
    role = relationship("Role", back_populates="team_members")
    checklist_to_tm = relationship("CheckListToTeamMember", back_populates="team_member")

class ApplicationStatus(Base):
    __tablename__ = "application_status"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    applications = relationship("Application", back_populates="status")

class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    team_id = Column(Integer, ForeignKey("team.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    status_id = Column(Integer, ForeignKey("application_status.id"))
    message = Column(String)
    created_at = Column(DateTime, default=func.now())

    team = relationship("Team", back_populates="applications")
    user = relationship("User", back_populates="applications")
    status = relationship("ApplicationStatus", back_populates="applications")

class TechFocus(Base):
    __tablename__ = "tech_focus"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    hackathons = relationship("Hackathon", secondary="tech_focus_to_hackathon", back_populates="tech_focuses")
    users = relationship("User", secondary="tech_focus_to_user", back_populates="tech_focuses")

class Organizer(Base):
    __tablename__ = "organizer"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)

    hackathons = relationship("Hackathon", secondary="organizer_to_hackathon", back_populates="organizers")

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

    checklist_to_role = relationship("CheckListToRole", back_populates="checklist")
    checklist_points = relationship("CheckListPoint", back_populates="checklist")
    checklist_to_user = relationship("CheckListToUser", back_populates="checklist")
    checklist_to_tm = relationship("CheckListToTeamMember", back_populates="checklist")

class CheckListToRole(Base):
    __tablename__ = "check_list_to_role"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cl_id = Column(Integer, ForeignKey("check_list.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

    checklist = relationship("CheckList", back_populates="checklist_to_role")
    role = relationship("Role", back_populates="checklists")

class CheckListPoint(Base):
    __tablename__ = "check_list_point"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    description = Column(String)
    cl_id = Column(Integer, ForeignKey("check_list.id"))

    checklist = relationship("CheckList", back_populates="checklist_points")

class CheckListToUser(Base):
    __tablename__ = "check_list_to_user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cl_id = Column(Integer, ForeignKey("check_list.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    grade = Column(Integer)

    checklist = relationship("CheckList", back_populates="checklist_to_user")
    user = relationship("User", back_populates="checklist_to_user")

class CheckListToTeamMember(Base):
    __tablename__ = "check_list_to_team_member"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cl_id = Column(Integer, ForeignKey("check_list.id"))
    tm_id = Column(Integer, ForeignKey("team_member.id"))
    grade = Column(Integer)

    checklist = relationship("CheckList", back_populates="checklist_to_tm")
    team_member = relationship("TeamMember", back_populates="checklist_to_tm")
