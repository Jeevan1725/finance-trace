import uuid
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.account import Account
from app.models.entity import Person, Company
from app.models.transaction import Transaction

router = APIRouter(prefix="/cases/{case_id}/graph", tags=["graph"])


@router.get("")
def get_graph(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    persons = {str(p.id): p.full_name for p in db.query(Person).filter(Person.case_id == case_id).all()}
    companies = {str(c.id): c.name for c in db.query(Company).filter(Company.case_id == case_id).all()}

    nodes = []
    for a in accounts:
        entity_name = None
        if a.entity_type == "PERSON":
            entity_name = persons.get(str(a.entity_id))
        elif a.entity_type == "COMPANY":
            entity_name = companies.get(str(a.entity_id))

        # Label: if entity known, use name + *last4, else *last4
        if entity_name:
            label = entity_name[:18] + " *" + (a.account_last4 or "????")
        else:
            label = "*" + (a.account_last4 or "????")

        nodes.append({
            "id": str(a.id),
            "label": label,
            "account_last4": a.account_last4,
            "account_type": a.account_type,
            "bank": a.bank_name or "?",
            "entity_type": a.entity_type,
            "entity_name": entity_name,
        })

    txns = db.query(Transaction).filter(Transaction.case_id == case_id).all()
    edge_map = defaultdict(lambda: {"count": 0, "total": 0.0, "min_date": None, "max_date": None})

    for t in txns:
        if not t.account_id or not t.counterparty_entity_id:
            continue
        if t.direction == "DEBIT":
            src, dst = t.account_id, t.counterparty_entity_id
        else:
            src, dst = t.counterparty_entity_id, t.account_id
        key = (str(src), str(dst))
        e = edge_map[key]
        e["count"] += 1
        e["total"] += float(t.amount)
        vd = t.value_date.isoformat()
        if not e["min_date"] or vd < e["min_date"]: e["min_date"] = vd
        if not e["max_date"] or vd > e["max_date"]: e["max_date"] = vd

    edges = [
        {
            "id": s + "__" + d,
            "source": s, "target": d,
            "count": e["count"], "total": e["total"],
            "min_date": e["min_date"], "max_date": e["max_date"],
        }
        for (s, d), e in edge_map.items()
    ]

    return {"nodes": nodes, "edges": edges}