from fastapi import HTTPException
import requests

from sqlalchemy.orm import Session
from app.models import Profile
from app.schemas.profile import ProfileUpdate, ProfileUpdateGit, GitResponse
from app.models import User


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
