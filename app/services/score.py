import pandas as pd


def generate_financial_score(records):
    df = pd.DataFrame(records)

    if df.empty:
        return {
            "spending_discipline": 0,
            "savings_health": 0,
            "risk_score": 0,
            "overall_score": 0
        }

    debit_df = df[df["type"] == "debit"].copy()
    credit_df = df[df["type"] == "credit"].copy()

    total_debit = abs(debit_df["amount"].sum()) if not debit_df.empty else 0
    total_credit = credit_df["amount"].sum() if not credit_df.empty else 0
    net = total_credit - total_debit

    # ---------------- Spending Discipline ----------------
    spending_discipline = 100

    if total_debit > 0:
        top_merchant_spend = (
            debit_df.groupby("description")["amount"].sum().abs().max()
            if not debit_df.empty else 0
        )
        merchant_concentration = top_merchant_spend / total_debit if total_debit else 0

        if merchant_concentration > 0.25:
            spending_discipline -= 20
        elif merchant_concentration > 0.15:
            spending_discipline -= 10

        txn_count = len(debit_df)
        if txn_count > 80:
            spending_discipline -= 15
        elif txn_count > 50:
            spending_discipline -= 8

    spending_discipline = max(0, min(100, spending_discipline))

    # ---------------- Savings Health ----------------
    savings_health = 50

    if total_credit > 0:
        savings_ratio = net / total_credit

        if savings_ratio > 0.4:
            savings_health = 90
        elif savings_ratio > 0.25:
            savings_health = 75
        elif savings_ratio > 0.1:
            savings_health = 60
        elif savings_ratio > 0:
            savings_health = 45
        else:
            savings_health = 20

    savings_health = max(0, min(100, savings_health))

    # ---------------- Risk Score ----------------
    risk_score = 100

    if not debit_df.empty and total_debit > 0:
        largest_txn = abs(debit_df["amount"].min())
        largest_ratio = largest_txn / total_debit

        if largest_ratio > 0.25:
            risk_score -= 30
        elif largest_ratio > 0.15:
            risk_score -= 15

        if len(debit_df) > 0 and debit_df["amount"].std() > abs(debit_df["amount"].mean()) * 2:
            risk_score -= 15

    risk_score = max(0, min(100, risk_score))

    # ---------------- Overall ----------------
    overall_score = round(
        (spending_discipline * 0.35) +
        (savings_health * 0.40) +
        (risk_score * 0.25)
    )

    return {
        "spending_discipline": round(spending_discipline),
        "savings_health": round(savings_health),
        "risk_score": round(risk_score),
        "overall_score": overall_score
    }