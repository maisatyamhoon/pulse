import pandas as pd


def compare_statements(records_a, records_b):
    df_a = pd.DataFrame(records_a)
    df_b = pd.DataFrame(records_b)

    if df_a.empty or df_b.empty:
        return {"summary": "Not enough data to compare statements."}

    spend_a = abs(df_a[df_a["type"] == "debit"]["amount"].sum())
    spend_b = abs(df_b[df_b["type"] == "debit"]["amount"].sum())

    income_a = df_a[df_a["type"] == "credit"]["amount"].sum()
    income_b = df_b[df_b["type"] == "credit"]["amount"].sum()

    net_a = income_a - spend_a
    net_b = income_b - spend_b

    category_a = (
        df_a[df_a["type"] == "debit"]
        .groupby("category")["amount"]
        .sum()
        .abs()
    )

    category_b = (
        df_b[df_b["type"] == "debit"]
        .groupby("category")["amount"]
        .sum()
        .abs()
    )

    categories = sorted(set(category_a.index).union(set(category_b.index)))

    category_changes = []
    for cat in categories:
        a = category_a.get(cat, 0)
        b = category_b.get(cat, 0)
        diff = b - a

        category_changes.append({
            "category": cat,
            "previous": round(a, 2),
            "current": round(b, 2),
            "change": round(diff, 2)
        })

    return {
        "summary": {
            "previous_spend": round(spend_a, 2),
            "current_spend": round(spend_b, 2),
            "spend_change": round(spend_b - spend_a, 2),
            "previous_income": round(income_a, 2),
            "current_income": round(income_b, 2),
            "income_change": round(income_b - income_a, 2),
            "previous_net": round(net_a, 2),
            "current_net": round(net_b, 2),
            "net_change": round(net_b - net_a, 2),
        },
        "category_changes": category_changes
    }