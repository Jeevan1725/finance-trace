import uuid
from datetime import date
from pydantic import BaseModel, Field


class PersonCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., description="POI | ASSOCIATE | FAMILY | DIRECTOR | SHAREHOLDER | BENAMI | FRIEND")
    pan: str | None = Field(None, min_length=10, max_length=10)
    aadhaar_last4: str | None = Field(None, min_length=4, max_length=4)
    din: str | None = Field(None, min_length=8, max_length=8)
    dob: date | None = None
    phones: list[str] | None = None
    emails: list[str] | None = None
    upi_ids: list[str] | None = None
    address: str | None = None
    district: str | None = None
    state: str | None = None
    country: str | None = "India"


class PersonOut(BaseModel):
    id: uuid.UUID
    full_name: str
    role: str
    pan: str | None
    aadhaar_last4: str | None
    din: str | None

    class Config:
        from_attributes = True


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    pan: str | None = None
    tan: str | None = None
    cin: str | None = Field(None, min_length=21, max_length=21)
    gstin: str | None = Field(None, min_length=15, max_length=15)
    district: str | None = None
    state: str | None = None
    country: str | None = "India"


class CompanyOut(BaseModel):
    id: uuid.UUID
    name: str
    pan: str | None
    tan: str | None
    cin: str | None
    gstin: str | None

    class Config:
        from_attributes = True