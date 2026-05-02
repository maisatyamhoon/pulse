def categorize_transaction(description: str) -> str:
    desc = description.lower()

    if any(word in desc for word in ["swiggy", "zomato", "amul", "restaurant", "cafe", "food"]):
        return "Food"

    if any(word in desc for word in ["spotify", "netflix", "youtube", "prime"]):
        return "Entertainment"

    if any(word in desc for word in ["electricity", "recharge", "bill", "broadband"]):
        return "Bills"

    if any(word in desc for word in ["rent", "transfer", "sent", "upi"]):
        return "Transfer"

    return "Other"


def enrich_transactions(records):
    enriched = []

    for row in records:
        row["category"] = categorize_transaction(row["description"])
        enriched.append(row)

    return enriched