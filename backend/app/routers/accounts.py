import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.account import Account

router = APIRouter(prefix="/cases/{case_id}/accounts", tags=["accounts"])


@router.get("")
def list_accounts(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    return [
        {
            "id": str(a.id),
            "account_last4": a.account_last4,
            "bank_name": a.bank_name,
            "account_type": a.account_type,
            "entity_type": a.entity_type,
            "entity_id": str(a.entity_id),
        }
        for a in accounts
    ]