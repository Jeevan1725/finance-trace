import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class CaseCreate(BaseModel):
    case_number: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    created_by: str = Field(..., description="UUID string of the user")


class CaseOut(BaseModel):
    id: uuid.UUID
    case_number: str
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True