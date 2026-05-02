from app.parsers.detector import detect_provider
from app.parsers.extract import extract_pdf_text
from app.parsers.gpay import parse_gpay
from app.parsers.paytm import parse_paytm
from app.parsers.phonepe import parse_phonepe


def parse_file(file_bytes: bytes, password: str = None):
    provider = detect_provider(file_bytes, password=password)
    raw_text = extract_pdf_text(file_bytes)

    if provider == "gpay":
        return parse_gpay(raw_text)
    elif provider == "paytm":
        return parse_paytm(raw_text)
    elif provider == "phonepe":
        return parse_phonepe(raw_text)

    return []