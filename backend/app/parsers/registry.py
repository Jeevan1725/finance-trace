from app.parsers.icici import ICICIParser
from app.parsers.sbi import SBIParser
from app.parsers.generic_bank import GenericBankParser
from app.parsers.sale_deed import SaleDeedParser
from app.parsers.base import BaseParser, ParsedTxn

PARSERS: list[BaseParser] = [
    ICICIParser(),
    SBIParser(),
    GenericBankParser(),
    SaleDeedParser(),
]

def pick_parser(text: str) -> BaseParser | None:
    for parser in PARSERS:
        if parser.detect(text):
            return parser
    return None

def parse_pdf_pages(pages: list[str]) -> tuple[BaseParser | None, list[ParsedTxn]]:
    if not pages: return None, []
    sample = "\n".join(pages[:2])
    parser = pick_parser(sample)
    if not parser: return None, []
    return parser, parser.parse(pages)