from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === CHECK LIST TO TEAM MEMBER ===

class CheckListToTeamMemberBase(BaseModel):
    cl_id: int
    tm_id: int
    grade: int

class CheckListToTeamMemberCreate(CheckListToTeamMemberBase):
    pass

class CheckListToTeamMemberRead(CheckListToTeamMemberBase):
    id: int