import re
import uuid
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.account import Account
from app.models.transaction import Transaction


def extract_self_account_number(document: Document, pages: list[str]) -> str | None:
    combined = "\n".join(pages[:2])
    for pattern in [
        # SBI: Account No.:40595612144
        r'Account\s*No\.?\s*:\s*(\d{8,16})',
        # ICICI: Current XXXXXXXX0014 / Current 478105000014
        r'Current\s+(?:XXXX+)?(\d{4,16})',
        # ICICI: Statement of Transactions in Current Account XXXXXXXX0014
        r'Statement of Transactions in Current Account\s+(?:XXXX+)?(\d{4,16})',
        # ICICI: account number: 478105000014
        r'account number:\s*(\d{8,16})',
        # HDFC: A/c No. XXXXXXXX1234
        r'A/c\s*No\.?\s*:?\s*(?:X+)?(\d{4,16})',
        # Axis: Account No: XXXXXXXX1234
        r'Account\s*Number\s*:?\s*(?:X+)?(\d{4,16})',
    ]:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            return m.group(1)
    # Fallback
    m = re.search(r'\b(\d{11,16})\b', combined)
    return m.group(1) if m else None


def get_or_create_account(
    db: Session, case_id: uuid.UUID, account_number: str,
    bank_name: str | None = None, is_self: bool = False,
) -> Account:
    last4 = account_number[-4:] if len(account_number) >= 4 else account_number
    existing = db.query(Account).filter(
        Account.case_id == case_id, Account.account_last4 == last4,
    ).first()
    if existing:
        return existing
    acc = Account(
        case_id=case_id,
        entity_type="UNKNOWN",
        entity_id=uuid.UUID(int=0),
        bank_name=bank_name,
        account_last4=last4,
        account_type="CURRENT" if is_self else "COUNTERPARTY",
    )
    db.add(acc)
    db.flush()
    return acc


def link_document_accounts(db: Session, document: Document, pages: list[str]) -> dict:
    self_account_num = extract_self_account_number(document, pages)
    if not self_account_num:
        return {"status": "skipped", "reason": "could not detect self account number"}

    self_account = get_or_create_account(db, document.case_id, self_account_num, is_self=True)

    txns = db.query(Transaction).filter(Transaction.source_doc_id == document.id).all()
    linked = 0
    cp_links = 0
    for txn in txns:
        txn.account_id = self_account.id
        counterparty_num = _extract_counterparty(txn.narration_raw or "")
        if counterparty_num:
            cp = get_or_create_account(db, document.case_id, counterparty_num, is_self=False)
            txn.counterparty_account_masked = cp.account_last4
            txn.counterparty_entity_type = "ACCOUNT"
            txn.counterparty_entity_id = cp.id
            cp_links += 1
        linked += 1

    db.commit()
    return {
        "status": "success",
        "self_account_last4": self_account.account_last4,
        "transactions_linked": linked,
        "counterparty_account_links": cp_links,
    }


def _extract_counterparty(narration: str) -> str | None:
    n = narration.upper()
    m = re.search(r'(?:TRF|TRFR|TRANSFER|NEFT|RTGS|IMPS)[\s:\-]*(?:FROM|TO)?[\s:]*(\d{10,16})', n)
    if m:
        return m.group(1)
    m = re.search(r'\b(\d{10,16})\b', n)
    if m:
        return m.group(1)
    return None