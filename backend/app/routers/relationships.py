import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.relationship import Relationship
from app.schemas.relationship import RelationshipCreate, RelationshipOut
from app.services.audit import log_action

router = APIRouter(prefix="/cases/{case_id}/relationships", tags=["relationships"])


@router.post("", response_model=RelationshipOut)
def create_relationship(case_id: uuid.UUID, payload: RelationshipCreate, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    rel = Relationship(
        case_id=case_id,
        source_type=payload.source_type,
        source_id=uuid.UUID(payload.source_id),
        target_type=payload.target_type,
        target_id=uuid.UUID(payload.target_id),
        rel_type=payload.rel_type,
        confidence=payload.confidence,
        valid_from=payload.valid_from,
        valid_to=payload.valid_to,
        evidence_doc_ids=[uuid.UUID(x) for x in payload.evidence_doc_ids] if payload.evidence_doc_ids else None,
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)

    log_action(db, case_id, case.created_by, "CREATE_RELATIONSHIP", "RELATIONSHIP", rel.id,
               {"rel_type": rel.rel_type})
    return rel


@router.get("", response_model=list[RelationshipOut])
def list_relationships(case_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(Relationship).filter(Relationship.case_id == case_id).all()