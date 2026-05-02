from app.parsers.extract import extract_pdf_text


def detect_provider(file_bytes: bytes, password=None):
    text = extract_pdf_text(file_bytes).lower()

    if "paytm" in text:
        return "paytm"
    elif "google pay" in text or "gpay" in text:
        return "gpay"
    else:
        return "unknown"