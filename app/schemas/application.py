from pydantic import BaseModel

class ApplicationSubmitRequest(BaseModel):
    team_member_id: int

class ApplicationDecisionRequest(BaseModel):
    application_id: int