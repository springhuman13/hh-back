from pydantic import BaseModel

# === ROLE ===

class RoleBase(BaseModel):
    name: str

class RoleOut(RoleBase):
    id: int