from app.parsers.detector import detect_parser
from app.parsers.gpay import parse_gpay
from app.parsers.paytm import parse_paytm
from app.parsers.phonepe import parse_phonepe


def parse_file(file_bytes: bytes, password: str = None):
    text = detect_parser(file_bytes, password=password)

    parser = text["parser"]
    raw_text = text["text"]

    if parser == "gpay":
        return parse_gpay(raw_text)
    elif parser == "paytm":
        return parse_paytm(raw_text)
    elif parser == "phonepe":
        return parse_phonepe(raw_text)

    return []