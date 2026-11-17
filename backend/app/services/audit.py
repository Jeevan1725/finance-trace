import uuid
from sqlalchemy.orm import Session
from app.models.audit import AuditLog


def log_action(
    db: Session,
    case_id: uuid.UUID | None,
    actor_id: uuid.UUID,
    action: str,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    payload: dict | None = None,
) -> None:
    entry = AuditLog(
        case_id=case_id,
        actor_id=actor_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        payload=payload,
    )
    db.add(entry)
    db.commit()