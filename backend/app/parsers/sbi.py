import re
from datetime import datetime
from decimal import Decimal
from app.parsers.base import BaseParser, ParsedTxn

class SBIParser(BaseParser):
    def detect(self, text: str) -> bool:
        t = text.upper()
        return 'STATE BANK OF INDIA' in t or 'SBIN' in t

    def parse(self, pages: list[str]) -> list[ParsedTxn]:
        transactions = []
        previous_balance = Decimal(0)
        row_no = 0

        for page_idx, page_text in enumerate(pages, start=1):
            if not page_text:
                continue
            
            lines = page_text.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                # Match: 05/04/23 05/04/23 DEP TFR 1100000.00 1100001.00Cr
                # Or: 05/04/23 05/04/23 WDL TFR 1100000.00 1.00Cr
                m = re.match(r'^(?P<pdate>\d{2}/\d{2}/\d{2})\s+(?P<vdate>\d{2}/\d{2}/\d{2})\s+(?P<type>DEP|WDL|BY)\s+(?P<desc>.*?)\s+(?P<amt>[\d,]+\.\d{2})\s+(?P<bal>[\d,]+\.\d{2})?(?:Cr|Dr)?$', line)
                if not m:
                    continue
                
                try:
                    vdate = datetime.strptime(m.group('vdate'), '%d/%m/%y').date()
                except ValueError:
                    continue
                
                amount = self.clean_number(m.group('amt'))
                direction = 'CREDIT' if m.group('type') == 'DEP' else 'DEBIT'
                desc = m.group('desc').strip()
                
                # Look ahead in the next 1-2 lines for the counterparty account number
                counterparty = None
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    m_acc = re.search(r'\b(\d{10,16})\b', next_line)
                    if m_acc:
                        counterparty = m_acc.group(1)
                        desc += " " + next_line
                
                row_no += 1
                transactions.append(ParsedTxn(
                    value_date=vdate,
                    narration=desc,
                    amount=amount,
                    direction=direction,
                    balance=None,
                    mode=self.detect_mode(desc),
                    page_no=page_idx,
                    row_no=row_no,
                    counterparty_account=counterparty
                ))

        return transactions