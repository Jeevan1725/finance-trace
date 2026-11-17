from app.parsers.icici import ICICIParser
from app.parsers.base import BaseParser, ParsedTxn


PARSERS: list[BaseParser] = [
    ICICIParser(),
]


def pick_parser(text: str) -> BaseParser | None:
    for parser in PARSERS:
        if parser.detect(text):
            return parser
    return None


def parse_pdf_pages(pages: list[str]) -> tuple[BaseParser | None, list[ParsedTxn]]:
    if not pages:
        return None, []
    # Detect on first page (or concat of first few)
    sample = "\n".join(pages[:2])
    parser = pick_parser(sample)
    if not parser:
        return None, []
    return parser, parser.parse(pages)