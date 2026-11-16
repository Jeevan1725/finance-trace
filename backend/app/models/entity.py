import uuid
from datetime import date
from sqlalchemy import String, Date, CHAR
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Person(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "persons"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    pan: Mapped[str | None] = mapped_column(String(10), index=True)
    aadhaar_last4: Mapped[str | None] = mapped_column(CHAR(4))
    din: Mapped[str | None] = mapped_column(CHAR(8), index=True)
    dob: Mapped[date | None] = mapped_column(Date)
    phones: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    emails: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    upi_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    address: Mapped[str | None] = mapped_column(String)
    district: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(100), default="India")


class Company(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "companies"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    pan: Mapped[str | None] = mapped_column(String(10), index=True)
    tan: Mapped[str | None] = mapped_column(String(10))
    cin: Mapped[str | None] = mapped_column(CHAR(21), index=True)
    gstin: Mapped[str | None] = mapped_column(CHAR(15), index=True)
    district: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(100), default="India")
