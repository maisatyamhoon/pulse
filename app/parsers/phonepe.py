from app.parsers.extract import extract_pdf_text


def parse_phonepe_pdf(file, password=None):
    text = extract_pdf_text(file, password=password)

    print("\n===== PHONEPE OCR TEXT START =====\n")
    print(text[:5000])
    print("\n===== PHONEPE OCR TEXT END =====\n")

    return []