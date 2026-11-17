import uuid
from datetime import datetime
from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    doc_type: str
    file_name: str
    file_hash: str
    file_size: int | None
    parse_status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True