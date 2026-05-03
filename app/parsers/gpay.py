from app.parsers.extract import extract_pdf_text


def parse_gpay(file_bytes):
    text = extract_pdf_text(file_bytes)

    return [{
        "date": "DEBUG",
        "description": text[:1200],
        "amount": 0,
        "type": "debug"
    }]