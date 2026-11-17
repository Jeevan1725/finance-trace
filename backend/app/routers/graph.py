import uuid
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.account import Account
from app.models.transaction import Transaction

router = APIRouter(prefix="/cases/{case_id}/graph", tags=["graph"])


@router.get("")
def get_graph(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    nodes = [
        {
            "id": str(a.id),
            "label": "*" + (a.account_last4 or "????"),
            "account_type": a.account_type,
            "bank": a.bank_name or "?",
        }
        for a in accounts
    ]

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