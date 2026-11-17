import re
from datetime import datetime
from decimal import Decimal
from app.parsers.base import BaseParser, ParsedTxn

class GenericBankParser(BaseParser):
    def detect(self, text: str) -> bool:
        t = text.upper()
        # Fallback for HDFC, Axis, Kotak, etc.
        return ('HDFC' in t or 'AXIS' in t or 'KOTAK' in t or 'BANK' in t) and ('STATEMENT' in t)

    def parse(self, pages: list[str]) -> list[ParsedTxn]:
        transactions = []
        row_no = 0
        for page_idx, page_text in enumerate(pages, start=1):
            if not page_text: continue
            for line in page_text.split('\n'):
                # Generic match: 01/04/2023 NEFT-SOMETHING 1,000.00 5,000.00
                m = re.match(r'^(?P<date>\d{2}[/-]\d{2}[/-]\d{2,4})\s+(?P<desc>.+?)\s+(?P<amt>[\d,]+\.\d{2})\s+(?P<bal>[\d,]+\.\d{2})', line)
                if not m: continue
                try:
                    vdate = datetime.strptime(m.group('date'), '%d/%m/%Y').date()
                except:
                    try: vdate = datetime.strptime(m.group('date'), '%d-%m-%Y').date()
                    except: continue
                
                desc = m.group('desc').strip()
                amount = self.clean_number(m.group('amt'))
                
                # Can't always infer direction from balance here, default to DEBIT for now
                direction = 'DEBIT' if 'DR' in line.upper() else 'CREDIT'
                
                row_no += 1
                transactions.append(ParsedTxn(
                    value_date=vdate, narration=desc, amount=amount,
                    direction=direction, balance=None, mode=self.detect_mode(desc),
                    page_no=page_idx, row_no=row_no,
                    counterparty_account=self.extract_counterparty_account(desc)
                ))
        return transactions