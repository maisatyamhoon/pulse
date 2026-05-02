import re
from datetime import datetime


def parse_gpay(text: str):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    records = []

    i = 0
    while i < len(lines) - 2:
        line1 = lines[i]
        line2 = lines[i + 1]
        line3 = lines[i + 2]

        m1 = re.match(r"(\d{2}\w{3},\d{4})\s+(.+?)\s+₹([\d,]+(?:\.\d+)?)", line1)
        m2 = re.match(r"(\d{2}:\d{2}(?:AM|PM))\s+UPITransactionID:\d+", line2)

        if m1 and m2 and line3.startswith("Paidby"):
            raw_date, desc, amount = m1.groups()

            try:
                date = datetime.strptime(raw_date, "%d%b,%Y").strftime("%Y-%m-%d")
                amount = float(amount.replace(",", ""))

                tx_type = "credit"
                if desc.lower().startswith("paidto") or desc.lower().startswith("selftransfer"):
                    tx_type = "debit"
                    amount = -amount

                desc = (
                    desc.replace("Paidto", "Paid to ")
                        .replace("Receivedfrom", "Received from ")
                        .replace("Selftransfer", "Self transfer ")
                        .strip()
                )

                records.append({
                    "date": date,
                    "description": desc,
                    "amount": amount,
                    "type": tx_type
                })

                i += 3
                continue

            except Exception:
                pass

        i += 1

    return records