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
    direction: str          # DEBIT or CREDIT
    balance: Decimal | None
    mode: str | None
    page_no: int
    row_no: int


class BaseParser(ABC):
    @abstractmethod
    def detect(self, text: str) -> bool:
        ...

    @abstractmethod
    def parse(self, pages: list[str]) -> list[ParsedTxn]:
        ...

    @staticmethod
    def clean_number(s: str) -> Decimal:
        # Remove commas and Cr/Dr suffix
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