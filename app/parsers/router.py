from app.parsers.paytm import parse_paytm
from app.parsers.extract import extract_pdf_text


def parse_file(file_bytes: bytes, password: str = None):
    raw_text = extract_pdf_text(file_bytes)
    return parse_paytm(raw_text)