import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.services.forensics import analyze_case

router = APIRouter(prefix="/cases/{case_id}/alerts", tags=["alerts"])

@router.get("")
def get_alerts(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return analyze_case(db, case_id)