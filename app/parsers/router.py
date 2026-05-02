from app.parsers.detector import detect_parser
from app.parsers.paytm import parse_paytm_pdf
from app.parsers.gpay import parse_gpay_pdf


def parse_file(file):
    parser = detect_parser(file)
    print("DETECTED PARSER:", parser)

    file.file.seek(0)

    if parser == "paytm":
        return parse_paytm_pdf(file)

    elif parser == "gpay":
        return parse_gpay_pdf(file)

    else:
        return []