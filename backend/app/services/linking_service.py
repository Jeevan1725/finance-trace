import re
import uuid
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.account import Account
from app.models.transaction import Transaction


def extract_self_account_number(document: Document, pages: list[str]) -> str | None:
    """Try to extract the account number that the statement belongs to."""
    combined = "\n".join(pages[:2])  # usually on first page
    # ICICI pattern: Current XXXXXXXX0014 or Current 478105000014
    for pattern in [
        r'Current\s+(?:XXXX+)?(\d{4,16})',
        r'Statement of Transactions in Current Account\s+(?:XXXX+)?(\d{4,16})',
        r'Current\s+Account\s+(?:XXXX+)?(\d{4,16})',
        r'account number:\s*(\d{8,16})',
    ]:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            return m.group(1)
    # Fallback: any 12-16 digit account like 478105000014
    m = re.search(r'\b(4781\d{10,12})\b', combined)
    return m.group(1) if m else None


def get_or_create_account(
    db: Session,
    case_id: uuid.UUID,
    account_number: str,
    bank_name: str | None = None,
    is_self: bool = False,
) -> Account:
    """Find existing account in this case or create a placeholder."""
    # Match by last 4 digits
    last4 = account_number[-4:] if len(account_number) >= 4 else account_number
    existing = db.query(Account).filter(
        Account.case_id == case_id,
        Account.account_last4 == last4,
    ).first()
    if existing:
        return existing

    acc = Account(
        case_id=case_id,
        entity_type="UNKNOWN",
        entity_id=uuid.UUID(int=0),  # placeholder until linked to a person/company
        bank_name=bank_name,
        account_last4=last4,
        account_type="CURRENT" if is_self else "COUNTERPARTY",
    )
    db.add(acc)
    db.flush()
    return acc


def link_document_accounts(db: Session, document: Document, pages: list[str]) -> dict:
    """
    After parsing, link all transactions to their source account and counterparty account.
    Returns a summary.
    """
    # 1. Detect the statement's own account number
    self_account_num = extract_self_account_number(document, pages)
    if not self_account_num:
        return {"status": "skipped", "reason": "could not detect self account number"}

    self_account = get_or_create_account(db, document.case_id, self_account_num, is_self=True)

    # 2. Link all transactions from this document to the self_account
    txns = db.query(Transaction).filter(Transaction.source_doc_id == document.id).all()
    linked = 0
    counterparty_accounts_created = 0
    for txn in txns:
        txn.account_id = self_account.id
        # 3. Extract counterparty account number from narration
        counterparty_num = _extract_counterparty(txn.narration_raw or "")
        if counterparty_num:
            cp = get_or_create_account(db, document.case_id, counterparty_num, is_self=False)
            txn.counterparty_account_masked = cp.account_last4
            txn.counterparty_entity_type = "ACCOUNT"
            txn.counterparty_entity_id = cp.id
            counterparty_accounts_created += 1
        linked += 1

    db.commit()
    return {
        "status": "success",
        "self_account_last4": self_account.account_last4,
        "transactions_linked": linked,
        "counterparty_account_links": counterparty_accounts_created,
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