from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# === CHECK LIST TO ROLE ===

class CheckListToRoleBase(BaseModel):
    cl_id: int
    role_id: int

class CheckListToRoleCreate(CheckListToRoleBase):
    pass

class CheckListToRoleRead(CheckListToRoleBase):
    id: int