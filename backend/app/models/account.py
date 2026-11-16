import uuid
from sqlalchemy import String, CHAR, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Account(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "accounts"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    bank_name: Mapped[str | None] = mapped_column(String(100), index=True)
    branch: Mapped[str | None] = mapped_column(String(100))
    ifsc: Mapped[str | None] = mapped_column(String(11))
    account_number_encrypted: Mapped[bytes | None] = mapped_column(LargeBinary)
    account_last4: Mapped[str | None] = mapped_column(CHAR(4))
    account_type: Mapped[str | None] = mapped_column(String(50))
    district: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(100), default="India")
