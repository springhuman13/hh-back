from fastapi import HTTPException, Depends
import requests
from typing import List, Annotated
from sqlalchemy.orm import Session

from app.models import Profile
from app.schemas.profile import GitResponse, SkillChecklistGrouped, SkillPoint, OtherUserProfileResponse
from app.schemas.tech_focus import TechFocusOut
from app.schemas.certificate import CertificateOut
from app.models import User, TechFocusToUser, TechFocus, CheckListToUser, CheckListPoint, CheckList, Certificate
from app.service.s3_service import S3Service

class ProfileService:
    def get_profile(self, user_id: int, db: Session) -> Profile:
        return db.query(Profile).filter(Profile.user_id == user_id).first()

    def update(self, user: User, db: Session, **fields) -> Profile:
        profile = self.get_profile(user.id, db)

        if not profile:
            profile = Profile(user_id=user.id)

        for key, value in fields.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile

    def get_git(self, user: User, db: Session):
        url = f"https://api.github.com/users/{user.profile.git_link}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return GitResponse(
                username=data.get("login"),
                public_repos=data.get("public_repos"),
                followers=data.get("followers"),
                following=data.get("following")
            )
        else:
            raise HTTPException(status_code=404, detail=f"GitHub user {user.profile.git_link} not found")

    def update_interests(self, user: User, tf_ids: List[int], db: Session):
        db.query(TechFocusToUser).filter(TechFocusToUser.user_id == user.id).delete()
        for tf_id in tf_ids:
            db.add(TechFocusToUser(user_id=user.id, tf_id=tf_id))
        db.commit()

    def get_interests(self, user: User, db: Session) -> List[TechFocusOut]:
        links = db.query(TechFocusToUser).filter(TechFocusToUser.user_id == user.id).all()

        interests = []
        for link in links:
            tech_focus = db.query(TechFocus).filter(TechFocus.id == link.tf_id).first()
            if tech_focus:
                interests.append(TechFocusOut(id=tech_focus.id, name=tech_focus.name))
        return interests

    def update_skills(self, user: User, skill_ids: List[int], db: Session):
        db.query(CheckListToUser).filter(CheckListToUser.user_id == user.id).delete()
        for skill_id in skill_ids:
            db.add(CheckListToUser(user_id=user.id, clp_id=skill_id))
        db.commit()

    def get_skills_grouped(self, user: User, db: Session) -> List[SkillChecklistGrouped]:
        links = db.query(CheckListToUser).filter(CheckListToUser.user_id == user.id).all()

        grouped = {}
        for link in links:
            point = db.query(CheckListPoint).filter(CheckListPoint.id == link.clp_id).first()
            if not point:
                continue

            checklist = db.query(CheckList).filter(CheckList.id == point.cl_id).first()
            if not checklist:
                continue

            if checklist.id not in grouped:
                grouped[checklist.id] = SkillChecklistGrouped(
                    checklist_id=checklist.id,
                    name=checklist.name,
                    points=[]
                )

            grouped[checklist.id].points.append(
                SkillPoint(
                    id=point.id,
                    description=point.description
                )
            )

        return list(grouped.values())
    
    def get_other_user_profile(self, user_id: int, db: Session) -> OtherUserProfileResponse:
        profile = self.get_profile(user_id=user_id, db=db)
        if not profile:
            raise HTTPException(status_code=404, detail="Профиль не найден")

        links = db.query(TechFocusToUser).filter(TechFocusToUser.user_id == user_id).all()
        interests = []
        for link in links:
            tech_focus = db.query(TechFocus).filter(TechFocus.id == link.tf_id).first()
            if tech_focus:
                interests.append(TechFocusOut(id=tech_focus.id, name=tech_focus.name))

        skill_links = db.query(CheckListToUser).filter(CheckListToUser.user_id == user_id).all()
        skills_set = set()
        skills = []

        for link in skill_links:
            point = db.query(CheckListPoint).filter(CheckListPoint.id == link.clp_id).first()
            if point and point.checklist:
                skill_id = point.checklist.id
                skill_description = point.checklist.name
                if (skill_id, skill_description) not in skills_set:
                    skills_set.add((skill_id, skill_description))
                    skills.append(SkillPoint(id=skill_id, description=skill_description))

        s3_service = S3Service()
        files = db.query(Certificate).filter(Certificate.user_id == user_id).all()
        certificates = []
        for file in files:
            download_url = s3_service._generate_presigned_url(s3_service.bucket, file.s3_key)
            certificates.append(CertificateOut(id=file.id, original_filename=file.original_filename, download_url=download_url))

        git_info = None
        if profile.git_link:
            url = f"https://api.github.com/users/{profile.git_link}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                git_info = GitResponse(
                    username=data.get("login"),
                    public_repos=data.get("public_repos"),
                    followers=data.get("followers"),
                    following=data.get("following")
                )

        return OtherUserProfileResponse(
            first_name=profile.first_name,
            last_name=profile.last_name,
            bio=profile.bio,
            photo_url=profile.photo_url,
            git=git_info,
            role_name=profile.role.name,
            interests=interests,
            skills=skills,
            certificates=certificates
        )
    

ProfileServiceDep = Annotated[ProfileService, Depends()]