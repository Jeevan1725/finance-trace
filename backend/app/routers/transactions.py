import uuid
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.transaction import Transaction

router = APIRouter(prefix="/cases/{case_id}/transactions", tags=["transactions"])


@router.get("")
def list_transactions(
    case_id: uuid.UUID,
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    min_amount: Decimal | None = Query(None),
    max_amount: Decimal | None = Query(None),
    direction: str | None = Query(None, description="DEBIT | CREDIT"),
    mode: str | None = Query(None, description="NEFT | RTGS | UPI | CASH | ..."),
    db: Session = Depends(get_db),
):
    q = db.query(Transaction).filter(Transaction.case_id == case_id)
    if from_date: q = q.filter(Transaction.value_date >= from_date)
    if to_date: q = q.filter(Transaction.value_date <= to_date)
    if min_amount is not None: q = q.filter(Transaction.amount >= min_amount)
    if max_amount is not None: q = q.filter(Transaction.amount <= max_amount)
    if direction: q = q.filter(Transaction.direction == direction)
    if mode: q = q.filter(Transaction.mode == mode)
    rows = q.order_by(Transaction.value_date.desc(), Transaction.id.desc()).limit(1000).all()

    return [
        {
            "id": str(r.id),
            "value_date": r.value_date.isoformat(),
            "amount": str(r.amount),
            "direction": r.direction,
            "mode": r.mode,
            "narration": r.narration_raw,
            "source_doc_id": str(r.source_doc_id) if r.source_doc_id else None,
            "page_no": r.page_no,
            "row_no": r.row_no,
        }
        for r in rows
    ]