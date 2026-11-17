import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseOut
from app.services.audit import log_action

router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("", response_model=CaseOut)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    existing = db.query(Case).filter(Case.case_number == payload.case_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Case number already exists")

    case = Case(
        case_number=payload.case_number,
        title=payload.title,
        description=payload.description,
        created_by=uuid.UUID(payload.created_by),
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    log_action(db, case.id, case.created_by, "CREATE_CASE", "CASE", case.id,
               {"case_number": case.case_number, "title": case.title})
    return case


@router.get("", response_model=list[CaseOut])
def list_cases(db: Session = Depends(get_db)):
    return db.query(Case).order_by(Case.created_at.desc()).all()


@router.get("/{case_id}", response_model=CaseOut)
def get_case(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case