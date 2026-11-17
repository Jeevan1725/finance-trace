import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.account import Account
from app.models.entity import Person, Company
from app.services.audit import log_action

router = APIRouter(prefix="/cases/{case_id}/accounts", tags=["accounts"])


class AccountLinkPayload(BaseModel):
    entity_type: str          # PERSON | COMPANY
    entity_id: uuid.UUID
    bank_name: str | None = None


@router.get("")
def list_accounts(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    accounts = db.query(Account).filter(Account.case_id == case_id).all()

    # Look up entity names
    persons = {str(p.id): p.full_name for p in db.query(Person).filter(Person.case_id == case_id).all()}
    companies = {str(c.id): c.name for c in db.query(Company).filter(Company.case_id == case_id).all()}

    out = []
    for a in accounts:
        entity_name = None
        if a.entity_type == "PERSON":
            entity_name = persons.get(str(a.entity_id))
        elif a.entity_type == "COMPANY":
            entity_name = companies.get(str(a.entity_id))
        out.append({
            "id": str(a.id),
            "account_last4": a.account_last4,
            "bank_name": a.bank_name,
            "account_type": a.account_type,
            "entity_type": a.entity_type,
            "entity_id": str(a.entity_id),
            "entity_name": entity_name,
        })
    return out


@router.post("/{account_id}/link")
def link_account(
    case_id: uuid.UUID, account_id: uuid.UUID,
    payload: AccountLinkPayload, db: Session = Depends(get_db),
):
    acc = db.query(Account).filter(Account.id == account_id, Account.case_id == case_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    # Verify entity exists in this case
    if payload.entity_type == "PERSON":
        entity = db.query(Person).filter(Person.id == payload.entity_id, Person.case_id == case_id).first()
    elif payload.entity_type == "COMPANY":
        entity = db.query(Company).filter(Company.id == payload.entity_id, Company.case_id == case_id).first()
    else:
        raise HTTPException(status_code=400, detail="entity_type must be PERSON or COMPANY")

    if not entity:
        raise HTTPException(status_code=404, detail=f"{payload.entity_type} not found in this case")

    acc.entity_type = payload.entity_type
    acc.entity_id = payload.entity_id
    if payload.bank_name:
        acc.bank_name = payload.bank_name
    db.commit()

    log_action(db, case_id, entity.id, "LINK_ACCOUNT", "ACCOUNT", acc.id,
               {"account_last4": acc.account_last4, "entity_type": payload.entity_type})
    return {"status": "ok", "account_last4": acc.account_last4, "linked_to": payload.entity_type}