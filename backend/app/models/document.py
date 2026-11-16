import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, CHAR, BigInteger, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDMixin


class Document(Base, UUIDMixin):
    __tablename__ = "documents"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_hash: Mapped[str] = mapped_column(CHAR(64), nullable=False)
    file_size: Mapped[int | None] = mapped_column(BigInteger)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    parse_status: Mapped[str] = mapped_column(String(20), default="PENDING", index=True)
    parse_confidence: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    linked_entities: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)))
