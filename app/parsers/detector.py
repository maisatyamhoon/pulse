from app.parsers.extract import extract_pdf_text


def detect_parser(file):
    text = extract_pdf_text(file).lower()

    if "google pay" in text or "transaction statement" in text:
        return "gpay"

    if "paytm statement" in text or "passbook payments history" in text:
        return "paytm"

    if "phonepe" in text:
        return "phonepe"

    return "unknown"