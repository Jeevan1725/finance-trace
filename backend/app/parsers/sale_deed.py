import re
from app.parsers.base import BaseParser

class SaleDeedParser(BaseParser):
    def detect(self, text: str) -> bool:
        t = text.upper()
        return 'SALE DEED' in t or 'DEED OF SALE' in t

    def parse(self, pages: list[str]) -> dict:
        # We won't return ParsedTxn here; we'll return a dictionary of extracted facts
        full_text = "\n".join(pages)
        
        # Extract Vendor (Seller)
        vendor_match = re.search(r'Sri/\s*Smt\./\s*Kum\.\s*(.+?)\s*S/o', full_text, re.IGNORECASE | re.DOTALL)
        vendor = vendor_match.group(1).replace('\n', ' ').strip() if vendor_match else "Unknown"
        
        # Extract Vendee (Buyer)
        vendee_match = re.search(r'In Favour of\s*Sri/\s*Smt\.\s*(.+?)\s*S/o', full_text, re.IGNORECASE | re.DOTALL)
        vendee = vendee_match.group(1).replace('\n', ' ').strip() if vendee_match else "Unknown"
        
        # Extract Sale Consideration
        amount_match = re.search(r'total sale consideration of Rs\.\s*([\d,]+)', full_text, re.IGNORECASE)
        amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0.0
        
        # Extract Property Details
        prop_match = re.search(r'Plot bearing plot no\./\s*House No\.\s*(.+?),', full_text, re.IGNORECASE)
        prop = prop_match.group(1).strip() if prop_match else "Unknown"
        
        return {
            "vendor": vendor,
            "vendee": vendee,
            "amount": amount,
            "property": prop,
            "raw_text": full_text[:500] # For debugging
        }