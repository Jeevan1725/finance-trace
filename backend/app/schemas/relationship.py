from datetime import date
from pydantic import BaseModel, Field


class RelationshipCreate(BaseModel):
    source_type: str = Field(..., description="PERSON | COMPANY")
    source_id: str
    target_type: str = Field(..., description="PERSON | COMPANY")
    target_id: str
    rel_type: str = Field(..., description="FAMILY | ASSOCIATE | BENAMI | FRIEND | DIRECTOR_OF | SHAREHOLDER_OF | TRANSACTED_WITH")
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    valid_from: date | None = None
    valid_to: date | None = None
    evidence_doc_ids: list[str] | None = None


class RelationshipOut(BaseModel):
    id: str
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    rel_type: str
    confidence: float
    asserted_by: str

    class Config:
        from_attributes = True