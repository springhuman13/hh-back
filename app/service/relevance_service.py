from typing import List, Optional, Annotated

from app.schemas.team import UserProfile, TeamResponse, TeamMemberInfo
from app.schemas.hackathon import HackathonOut
from app.models import CheckListToTeamMember, CheckListPoint, TeamMember, Hackathon
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from app.database import get_db

# Утилита для подсчета Жаккара между двумя списками
def jaccard_similarity(set1: List[int], set2: List[int]) -> float:
    if not set1 and not set2:
        return 1.0
    union = set(set1) | set(set2)
    intersection = set(set1) & set(set2)
    return len(intersection) / len(union) if union else 0.0

class RelevanceService:
    def __init__(self, session: Session):
        self.session = session

    def calculate_relevance(self, user_profile: UserProfile, team: TeamResponse, hackathon: HackathonOut) -> float:
        matching_role_id = None
        for member in team.members:
            if member.user_id is None and member.role_id == user_profile.role_id:
                matching_role_id = member.role_id
                break

        role_match = 1.0 if matching_role_id else 0.0

        skill_score = 0.0
        if matching_role_id:
            stmt = select(TeamMember).where(
                TeamMember.team_id == team.id,
                TeamMember.role_id == matching_role_id,
                TeamMember.user_id == None
            )
            result = self.session.execute(stmt)
            team_member = result.scalar_one_or_none()

            if team_member:
                stmt = select(CheckListToTeamMember).where(
                    CheckListToTeamMember.tm_id == team_member.id
                )
                result = self.session.execute(stmt)
                checklist_weights = result.scalars().all()

                total_weight = sum(c.weight for c in checklist_weights)
                matched_weight = sum(
                    c.weight for c in checklist_weights
                    if c.clp_id in user_profile.selected_subskills
                )
                skill_score = matched_weight / total_weight if total_weight else 0.0

        hackathon_focus_ids = [tf.id for tf in hackathon.tech_focuses]
        tech_focus_score = jaccard_similarity(user_profile.tech_focuses, hackathon_focus_ids)

        total_score = 0.4 * role_match + 0.4 * skill_score + 0.2 * tech_focus_score
        return total_score

    def sort_teams_by_relevance(self, user_profile: Optional[UserProfile], teams: List[TeamResponse], filters_sort: int) -> List[TeamResponse]:
        if filters_sort != 0:
            if filters_sort == 1:
                teams.sort(key=lambda t: t.id, reverse=True)
            elif filters_sort == 2:
                teams.sort(key=lambda t: t.name)
            return teams

        if not user_profile:
            teams.sort(key=lambda t: t.id, reverse=True)
            return teams

        hackathon_ids = [team.hackathon_id for team in teams]
        stmt = select(Hackathon).where(Hackathon.id.in_(hackathon_ids))
        result = self.session.execute(stmt)
        hackathons = result.scalars().all()
        hackathon_by_id = {h.id: h for h in hackathons}

        scored_teams = []
        for team in teams:
            hackathon = hackathon_by_id.get(team.hackathon_id)
            if not hackathon:
                continue
            score = self.calculate_relevance(user_profile, team, hackathon)
            scored_teams.append({
                "team": team,
                "score": score
            })

        scored_teams.sort(key=lambda x: x["score"], reverse=True)
        return [
            TeamResponse(
                **{k: v for k, v in team_data["team"].dict().items() if k != "score"},
                score=team_data["score"]
            )
            for team_data in scored_teams
        ]


def RelevanceServiceDep(session: Session = Depends(get_db)) -> RelevanceService:
    return RelevanceService(session)
