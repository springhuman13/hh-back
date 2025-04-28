from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.models import TeamMember, Application, User, Notification
from app.schemas.application import ApplicationSubmitRequest, ApplicationDecisionRequest
from pydantic import BaseModel

class ApplicationService:
    def create_notification(self, user_id: int, message: str,  db: Session, application_id: int, link: str = None, type: str = "info"):
        notification = Notification(
            user_id=user_id,
            message=message,
            link=link,
            type=type,
            application_id=application_id
        )
        db.add(notification)
    def submit_application(self, data: ApplicationSubmitRequest, user: User, db: Session):
        team_member = db.query(TeamMember).filter(
            TeamMember.id == data.team_member_id,
            TeamMember.user_id == None
        ).first()

        if not team_member:
            raise ValueError("Эта роль уже занята или не существует")

        existing_application = db.query(Application).filter(
            Application.team_member_id == team_member.id,
            Application.user_id == user.id,
            Application.status_id == 1 
        ).first()

        if existing_application:
            raise ValueError("Вы уже подали заявку на эту роль в команде")

        application = Application(
            team_id=team_member.team_id,
            team_member_id=team_member.id,
            user_id=user.id,
            status_id=1, 
        )

        db.add(application)
        db.flush()
        self.create_notification(
            user_id=team_member.team.leader_id,
            message=f"Новая заявка в команду {team_member.team.name}",
            db=db,
            link=f"https://hahackathon.ru.tuna.am/view_profile.html?id={user.id}", #ДОДЕЛАТЬ
            type="application",
            application_id=application.id
        )
        db.commit()

        return {"status": "ok", "message": "Заявка отправлена"}

    def accept_application(self, data: ApplicationDecisionRequest, user: User, db: Session):
        application = db.query(Application).filter(
            Application.id == data.application_id,
            Application.status_id == 1
        ).first()

        if not application:
            raise ValueError("Заявка не найдена или уже обработана")

        team = application.team

        if team.leader_id != user.id:
            raise ValueError("Вы не являетесь капитаном этой команды")

        team_member = db.query(TeamMember).filter(
            TeamMember.id == application.team_member_id,
            TeamMember.user_id == None
        ).first()

        if not team_member:
            raise ValueError("Роль уже занята другим пользователем")

        application.status_id = 2
        team_member.user_id = application.user_id
        captain_profile = user.profile

        self.create_notification(
            user_id=application.user_id,
            message=f"Вас приняли в команду {team.name} на роль {team_member.role.name}",
            db=db,
            link=captain_profile.tg_link,
            application_id=application.id
        )

        self.create_notification(
            user_id=user.id,
            message=f"Вы приняли участника в команду {team.name} на роль {team_member.role.name}",
            db=db,
            link=application.user.profile.tg_link,
            application_id=application.id
        )

        db.commit()

        return {"status": "ok", "message": "Заявка принята"}

    def decline_application(self, data: ApplicationDecisionRequest, user: User, db: Session):
        application = db.query(Application).filter(
            Application.id == data.application_id,
            Application.status_id == 1
        ).first()

        if not application:
            raise ValueError("Заявка не найдена или уже обработана")

        team = application.team

        if team.leader_id != user.id:
            raise ValueError("Вы не являетесь капитаном этой команды")

        application.status_id = 3 

        self.create_notification(
            user_id=application.user_id,
            message=f"Вам отказали во вступлении в команду {team.name}",
            db=db,
            link=None,
            type="decline",
            application_id=application.id
        )

        db.commit()

        return {"status": "ok", "message": "Заявка отклонена"}


ApplicationServiceDep = Annotated[ApplicationService, Depends()]