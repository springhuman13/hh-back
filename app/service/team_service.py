from fastapi import Depends
from sqlalchemy.orm import Session, selectinload
from typing import Annotated, Optional, List

from app.models import User, Team, TeamMember, CheckListToTeamMember, Hackathon
from app.schemas.team import TeamCreate, TeamResponse, TeamMemberInfo, TeamFilter
from app.service.relevance_service import RelevanceServiceDep, RelevanceService
from app.schemas.team import UserProfile

class TeamService:
    def __init__(self, relevance_service: RelevanceService = Depends(RelevanceServiceDep)):
        self.relevance_service = relevance_service

    def create_team(self, data: TeamCreate, db: Session, user: User):
        team = Team(
            name=data.name,
            hackathon_id=data.hackathon_id,
            city_id=data.city_id,
            leader_id=user.id,
            description=data.description,
        )
        db.add(team)
        db.flush()

        for role_data in data.roles:
            tm = TeamMember(team_id=team.id, role_id=role_data.role_id)
            db.add(tm)
            db.flush()

            for skill in role_data.checklist:
                db.add(CheckListToTeamMember(
                    clp_id=skill.checklist_point_id,
                    tm_id=tm.id,
                    weight=skill.weight
                ))

        db.commit()
        return {"status": "ok", "team_id": team.id}

    def get_all_teams(self, db: Session):
        teams = db.query(Team).options(
            selectinload(Team.city),
            selectinload(Team.hackathon),
            selectinload(Team.members).selectinload(TeamMember.user),
            selectinload(Team.members).selectinload(TeamMember.role),
        ).all()

        return [
            TeamResponse(
                id=team.id,
                name=team.name,
                description=team.description,
                city_name=team.city.name,
                hackathon_name=team.hackathon.name,
                hackathon_website=team.hackathon.website,
                members=[
                    TeamMemberInfo(
                        id=member.id,  
                        role_id=member.role_id,
                        role_name=member.role.name,
                        user_id=member.user_id,
                    )
                    for member in team.members
                ]
            )
            for team in teams
        ]
    def get_user_led_teams(self, user: User, db: Session) -> List[TeamResponse]:
        teams = db.query(Team).options(
            selectinload(Team.city),
            selectinload(Team.hackathon),
            selectinload(Team.members).selectinload(TeamMember.user),
            selectinload(Team.members).selectinload(TeamMember.role),
        ).filter(Team.leader_id == user.id).all()

        return [
            TeamResponse(
                id=team.id,
                name=team.name,
                description=team.description,
                city_name=team.city.name,
                city_id=team.city_id,
                hackathon_name=team.hackathon.name,
                hackathon_id=team.hackathon_id,
                hackathon_website=team.hackathon.website,
                members=[
                    TeamMemberInfo(
                        id=member.id,
                        role_id=member.role_id,
                        role_name=member.role.name,
                        user_id=member.user_id,
                    )
                    for member in team.members
                ]
            )
            for team in teams
        ]

    def get_filtered_team(self, filters: TeamFilter, db: Session, user: Optional[User] = None) -> List[TeamResponse]:
        query = db.query(Team).options(
            selectinload(Team.city),
            selectinload(Team.hackathon),
            selectinload(Team.members).selectinload(TeamMember.user),
            selectinload(Team.members).selectinload(TeamMember.role),
        )

        if filters.name:
            query = query.filter(Team.name.ilike(f"%{filters.name}%"))

        if filters.city:
            query = query.filter(Team.city_id.in_(filters.city))

        if filters.hackathon:
            query = query.filter(Team.hackathon_id.in_(filters.hackathon))

        if filters.role:
            query = query.join(Team.members).filter(
                TeamMember.user_id == None,
                TeamMember.role_id.in_(filters.role)
            ).distinct()

        teams = query.all()

        team_responses = [
            TeamResponse(
                id=team.id,
                name=team.name,
                description=team.description,
                city_id=team.city_id,
                city_name=team.city.name,
                hackathon_id=team.hackathon_id,
                hackathon_name=team.hackathon.name,
                hackathon_website=team.hackathon.website,
                members=[
                    TeamMemberInfo(
                        id=member.id,  
                        role_id=member.role_id,
                        role_name=member.role.name,
                        user_id=member.user_id,
                    )
                    for member in team.members
                ]
            )
            for team in teams
        ]

        # Конвертация User -> UserProfile
        user_profile = None
        if user:
            if not user.profile:
                raise ValueError("User must have a profile to use relevance sort.")
            user_profile = UserProfile(
                user_id=user.id,
                role_id=user.profile.role_id,
                selected_subskills=[checklist.clp_id for checklist in user.checklist_to_user],
                tech_focuses=[focus.id for focus in user.tech_focuses]
            )

        return self.relevance_service.sort_teams_by_relevance(
            user_profile=user_profile,
            teams=team_responses,
            filters_sort=filters.sort
        )

TeamServiceDep = Annotated[TeamService, Depends()]
