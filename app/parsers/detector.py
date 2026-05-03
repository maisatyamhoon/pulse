from app.parsers.extract import extract_pdf_text


def detect_provider(file_bytes: bytes, password=None):
    text = extract_pdf_text(file_bytes)
    text_lower = text.lower()

    # Paytm
    if "paytm" in text_lower:
        return "paytm"

    # GPay (strong signals from actual statement)
    if (
        "google pay app" in text_lower
        or ("transaction statement" in text_lower and "upi transaction id" in text_lower)
        or "paid by " in text_lower
    ):
        return "gpay"

    # PhonePe
    if "phonepe" in text_lower or "phone pe" in text_lower:
        return "phonepe"

    return "unknown"