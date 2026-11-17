import uuid
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.models.account import Account
from app.models.entity import Person, Company
from app.models.relationship import Relationship
from app.models.transaction import Transaction

router = APIRouter(prefix="/cases/{case_id}/graph", tags=["graph"])

@router.get("")
def get_graph(case_id: uuid.UUID, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    persons = db.query(Person).filter(Person.case_id == case_id).all()
    companies = db.query(Company).filter(Company.case_id == case_id).all()
    rels = db.query(Relationship).filter(Relationship.case_id == case_id).all()

    nodes = []
    edges = []

    # 1. Add Persons and Companies as nodes
    for p in persons:
        nodes.append({"id": str(p.id), "label": p.full_name, "type": "PERSON", "role": p.role})
    for c in companies:
        nodes.append({"id": str(c.id), "label": c.name, "type": "COMPANY"})

    # 2. Add Accounts as nodes
    for a in accounts:
        label = f"*{a.account_last4}"
        nodes.append({"id": str(a.id), "label": label, "type": "ACCOUNT", "account_type": a.account_type})

    # 3. Add Relationship edges
    for r in rels:
        edges.append({
            "id": str(r.id),
            "source": str(r.source_id),
            "target": str(r.target_id),
            "label": r.rel_type,
            "type": "RELATIONSHIP"
        })

    # 4. Add Transaction edges (aggregated)
    txn_map = defaultdict(lambda: {"total": 0, "count": 0})
    for t in db.query(Transaction).filter(Transaction.case_id == case_id).all():
        if not t.account_id or not t.counterparty_entity_id: continue
        src, dst = (t.account_id, t.counterparty_entity_id) if t.direction == "DEBIT" else (t.counterparty_entity_id, t.account_id)
        txn_map[(str(src), str(dst))]["total"] += float(t.amount)
        txn_map[(str(src), str(dst))]["count"] += 1

    for (s, d), data in txn_map.items():
        edges.append({
            "id": f"txn_{s}_{d}",
            "source": s, "target": d,
            "label": f"Rs. {data['total']:,.2f}",
            "type": "TRANSACTION",
            "total": data["total"]
        })

    return {"nodes": nodes, "edges": edges}