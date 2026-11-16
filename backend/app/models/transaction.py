import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy import String, Date, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Transaction(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "transactions"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), index=True)
    value_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    posting_date: Mapped[date | None] = mapped_column(Date)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False, index=True)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    mode: Mapped[str | None] = mapped_column(String(20), index=True)
    counterparty_name_raw: Mapped[str | None] = mapped_column(String(255))
    counterparty_entity_type: Mapped[str | None] = mapped_column(String(20))
    counterparty_entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), index=True)
    counterparty_account_masked: Mapped[str | None] = mapped_column(String(50))
    upi_id: Mapped[str | None] = mapped_column(String(100))
    narration_raw: Mapped[str | None] = mapped_column(Text)
    source_doc_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    page_no: Mapped[int | None] = mapped_column(Integer)
    row_no: Mapped[int | None] = mapped_column(Integer)
    district: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(100), default="India")
