import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from abc import ABC, abstractmethod


@dataclass
class ParsedTxn:
    value_date: datetime
    narration: str
    amount: Decimal
    direction: str
    balance: Decimal | None
    mode: str | None
    page_no: int
    row_no: int
    counterparty_account: str | None = None    # NEW


class BaseParser(ABC):
    @abstractmethod
    def detect(self, text: str) -> bool: ...

    @abstractmethod
    def parse(self, pages: list[str]) -> list[ParsedTxn]: ...

    @staticmethod
    def clean_number(s: str) -> Decimal:
        s = re.sub(r'[^\d.\-]', '', s)
        return Decimal(s) if s else Decimal(0)

    @staticmethod
    def detect_mode(narration: str) -> str:
        n = narration.upper()
        if 'UPI' in n: return 'UPI'
        if 'NEFT' in n: return 'NEFT'
        if 'RTGS' in n: return 'RTGS'
        if 'IMPS' in n: return 'IMPS'
        if 'TRF' in n or 'TRANSFER' in n: return 'INTERNAL'
        if 'ATM' in n or 'CASH' in n: return 'CASH'
        if 'CHQ' in n or 'CHEQUE' in n: return 'CHEQUE'
        if 'DD' in n: return 'DD'
        return 'OTHER'

    @staticmethod
    def extract_counterparty_account(narration: str) -> str | None:
        """Extract account number from narration like 'TRF FROM 478105000013' or 'TRFR TO:478105000012'."""
        # Patterns: TRF FROM 478105000013, TRFR TO:478105000012, TRF FROM478105000013
        m = re.search(r'(?:TRF|TRFR|TRANSFER|NEFT|RTGS|IMPS)[\s:\-]*(?:FROM|TO)?[\s:]*(\d{10,16})', narration.upper())
        if m:
            return m.group(1)
        # Fallback: any 10-16 digit number at start (common in UPI like 478105000013@icici)
        m = re.search(r'\b(\d{10,16})\b', narration)
        if m:
            return m.group(1)
        return None