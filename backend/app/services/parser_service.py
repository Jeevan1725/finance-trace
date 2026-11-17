import uuid
import pdfplumber
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.transaction import Transaction
from app.parsers.registry import parse_pdf_pages


def parse_document(db: Session, document: Document) -> dict:
    """
    Opens the PDF, detects the bank, extracts transactions, inserts them.
    Returns a summary dict.
    """
    with pdfplumber.open(document.storage_path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]

    if not any(pages):
        document.parse_status = "FAILED"
        document.parse_confidence = 0
        db.commit()
        return {"status": "failed", "reason": "no extractable text (likely scanned PDF)", "transactions": 0}

    parser, txns = parse_pdf_pages(pages)

    if not parser:
        document.parse_status = "REVIEW"
        document.parse_confidence = 0
        db.commit()
        return {"status": "unsupported", "reason": "no matching bank parser", "transactions": 0}

    # Insert transactions
    inserted = 0
    for t in txns:
        txn = Transaction(
            case_id=document.case_id,
            account_id=None,  # account linking is a later commit
            value_date=t.value_date,
            amount=t.amount,
            direction=t.direction,
            mode=t.mode,
            counterparty_name_raw=None,
            narration_raw=t.narration,
            source_doc_id=document.id,
            page_no=t.page_no,
            row_no=t.row_no,
        )
        db.add(txn)
        inserted += 1

    document.parse_status = "PARSED"
    document.parse_confidence = 1.0 if inserted > 0 else 0
    db.commit()

    return {
        "status": "success",
        "parser": parser.__class__.__name__,
        "transactions": inserted,
    }