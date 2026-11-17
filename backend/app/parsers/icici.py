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

        P3_RE = re.compile(
            r'^(?P<date>\d{2}-\d{2}-\d{4})\s+(?P<narration>.+?)\s+(?P<wd>[\d,]+\.\d{2})\s+(?P<dep>[\d,]+\.\d{2})\s+(?P<bal>[\d,]+\.\d{2})\s*(?P<drcr>Cr|Dr)?$'
        )
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
                if not re.match(r'^\d{2}-\d{2}-\d{4}\s', line):
                    continue
                if 'B/F' in line.upper():
                    m_bf = re.search(r'([\d,]+\.\d{2})\s*(Cr|Dr)?$', line)
                    if m_bf and previous_balance is None:
                        previous_balance = self.clean_number(m_bf.group(1))
                    continue

                m3 = P3_RE.match(line)
                if m3:
                    try:
                        vdate = datetime.strptime(m3.group('date'), '%d-%m-%Y').date()
                    except ValueError:
                        continue
                    wd = self.clean_number(m3.group('wd'))
                    dep = self.clean_number(m3.group('dep'))
                    bal = self.clean_number(m3.group('bal'))
                    if wd > 0:
                        direction, amount = 'DEBIT', wd
                    else:
                        direction, amount = 'CREDIT', dep
                    narration = m3.group('narration')
                    row_no += 1
                    transactions.append(ParsedTxn(
                        value_date=vdate, narration=narration, amount=amount,
                        direction=direction, balance=bal, mode=self.detect_mode(narration),
                        page_no=page_idx, row_no=row_no,
                        counterparty_account=self.extract_counterparty_account(narration),
                    ))
                    previous_balance = bal
                    continue

                m1 = P1_RE.match(line)
                if m1:
                    try:
                        vdate = datetime.strptime(m1.group('date'), '%d-%m-%Y').date()
                    except ValueError:
                        continue
                    amount = self.clean_number(m1.group('amt'))
                    bal = self.clean_number(m1.group('bal'))
                    if previous_balance is not None:
                        if bal > previous_balance:
                            direction = 'CREDIT'
                        elif bal < previous_balance:
                            direction = 'DEBIT'
                        else:
                            direction = 'CREDIT'
                    else:
                        direction = 'CREDIT' if m1.group('drcr') == 'Cr' else 'DEBIT'
                    narration = m1.group('rest')
                    row_no += 1
                    transactions.append(ParsedTxn(
                        value_date=vdate, narration=narration, amount=amount,
                        direction=direction, balance=bal, mode=self.detect_mode(narration),
                        page_no=page_idx, row_no=row_no,
                        counterparty_account=self.extract_counterparty_account(narration),
                    ))
                    previous_balance = bal

        return transactions