import re
from datetime import datetime
from decimal import Decimal
from app.parsers.base import BaseParser, ParsedTxn


class ICICIParser(BaseParser):
    def detect(self, text: str) -> bool:
        t = text.upper()
        return ('ICICI' in t) and ('STATEMENT OF TRANSACTIONS' in t or 'STATEMENT OF TRANSACTIONS IN CURRENT ACCOUNT' in t)

    def parse(self, pages: list[str]) -> list[ParsedTxn]:
        transactions: list[ParsedTxn] = []
        previous_balance: Decimal | None = None
        row_no = 0

        # Regex for Page 3 layout: Withdrawals, Deposits, Balance
        # Format: 02-04-2024 TRF FROM 478105000013 0.00 20,44,806.40 20,51,174.20 Cr
        P3_RE = re.compile(
            r'^(?P<date>\d{2}-\d{2}-\d{4})\s+(?P<narration>.+?)\s+(?P<wd>[\d,]+\.\d{2})\s+(?P<dep>[\d,]+\.\d{2})\s+(?P<bal>[\d,]+\.\d{2})\s*(?P<drcr>Cr|Dr)?$'
        )

        # Regex for Page 1 layout: Amount, Balance
        # Format: 12-06-2024 12-06-2024TRF FROM 478105000013 RAIPUR - LABHANDI 4,00,190.00 5,07,777.20 Cr
        P1_RE = re.compile(
            r'^(?P<date>\d{2}-\d{2}-\d{4})\s+(?P<rest>.+?)\s+(?P<amt>[\d,]+\.\d{2})\s+(?P<bal>[\d,]+\.\d{2})\s*(?P<drcr>Cr|Dr)?$'
        )

        for page_idx, page_text in enumerate(pages, start=1):
            if not page_text:
                continue

            for raw_line in page_text.split('\n'):
                line = raw_line.strip()
                if not line:
                    continue

                # Skip header/footer
                if not re.match(r'^\d{2}-\d{2}-\d{4}\s', line):
                    continue
                
                # Skip B/F (opening balance)
                if ' B/F ' in line.upper() or 'B/F' in line.upper():
                    m_bf = re.search(r'([\d,]+\.\d{2})\s*(Cr|Dr)?$', line)
                    if m_bf and previous_balance is None:
                        previous_balance = self.clean_number(m_bf.group(1))
                    continue

                # Try Page 3 format first (has withdrawals AND deposits)
                m3 = P3_RE.match(line)
                if m3:
                    try:
                        vdate = datetime.strptime(m3.group('date'), '%d-%m-%Y').date()
                    except ValueError:
                        continue
                    
                    wd = self.clean_number(m3.group('wd'))
                    dep = self.clean_number(m3.group('dep'))
                    bal = self.clean_number(m3.group('bal'))
                    
                    # If withdrawal > 0, it's DEBIT. Else DEPOSIT > 0 is CREDIT.
                    if wd > 0:
                        direction = 'DEBIT'
                        amount = wd
                    else:
                        direction = 'CREDIT'
                        amount = dep
                    
                    row_no += 1
                    transactions.append(ParsedTxn(
                        value_date=vdate,
                        narration=m3.group('narration'),
                        amount=amount,
                        direction=direction,
                        balance=bal,
                        mode=self.detect_mode(m3.group('narration')),
                        page_no=page_idx,
                        row_no=row_no,
                    ))
                    previous_balance = bal
                    continue

                # Try Page 1 format (single amount column)
                m1 = P1_RE.match(line)
                if m1:
                    try:
                        vdate = datetime.strptime(m1.group('date'), '%d-%m-%Y').date()
                    except ValueError:
                        continue
                    
                    amount = self.clean_number(m1.group('amt'))
                    bal = self.clean_number(m1.group('bal'))
                    
                    # Infer direction from balance change
                    if previous_balance is not None:
                        if bal > previous_balance:
                            direction = 'CREDIT'
                        elif bal < previous_balance:
                            direction = 'DEBIT'
                        else:
                            direction = 'CREDIT'
                    else:
                        direction = 'CREDIT' if m1.group('drcr') == 'Cr' else 'DEBIT'
                    
                    row_no += 1
                    transactions.append(ParsedTxn(
                        value_date=vdate,
                        narration=m1.group('rest'),
                        amount=amount,
                        direction=direction,
                        balance=bal,
                        mode=self.detect_mode(m1.group('rest')),
                        page_no=page_idx,
                        row_no=row_no,
                    ))
                    previous_balance = bal

        return transactions