import re
from datetime import datetime
from app.parsers.extract import extract_pdf_text


def parse_paytm_pdf(file):
    text = extract_pdf_text(file)
    records = []

    pattern = re.findall(
        r"(\d{1,2} \w{3})\s+(Paid to .*?|Received from .*?|Money sent to .*?|Money received from .*?)\s+.*?Rs\.?([0-9,]+(?:\.\d{2})?)",
        text,
        re.IGNORECASE
    )

    for date_str, desc, amount in pattern:
        try:
            date = datetime.strptime(date_str + " 2026", "%d %b %Y").strftime("%Y-%m-%d")
        except:
            continue

        amount = float(amount.replace(",", ""))
        tx_type = "credit" if "received" in desc.lower() else "debit"

        records.append({
            "date": date,
            "description": desc.strip(),
            "amount": amount if tx_type == "credit" else -amount,
            "type": tx_type
        })

    return records