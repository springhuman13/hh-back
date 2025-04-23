from fastapi import HTTPException
import requests
from typing import List
from sqlalchemy.orm import Session

from app.models import Profile
from app.schemas.profile import ProfileUpdate, ProfileUpdateGit, GitResponse, InterestsResponse
from app.schemas.tech_focus import TechFocusOut
from app.models import User, TechFocusToUser, TechFocus


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, user_id: int) -> Profile:
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()

    def update(self, user: User, **fields) -> Profile:
        profile = self.get_profile(user.id)

        if not profile:
            profile = Profile(user_id=user.id)

        for key, value in fields.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_git(self, user: User):
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
        
    def update_interests(self, user: User, tf_ids: list[int]):
        self.db.query(TechFocusToUser).filter(TechFocusToUser.user_id == user.id).delete()
        for tf_id in tf_ids:
            self.db.add(TechFocusToUser(user_id=user.id, tf_id=tf_id))
        self.db.commit()

    def get_interests(self, user: User) -> List[TechFocusOut]:
        links = self.db.query(TechFocusToUser).filter(TechFocusToUser.user_id == user.id).all()
    
        interests = []
        for link in links:
            tech_focus = self.db.query(TechFocus).filter(TechFocus.id == link.tf_id).first()
            if tech_focus:
                interests.append(TechFocusOut(id=tech_focus.id, name=tech_focus.name))
    
        return interests