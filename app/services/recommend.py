import pandas as pd


def generate_recommendations(records):
    df = pd.DataFrame(records)

    if df.empty:
        return ["No spending data available for recommendations."]

    recs = []

    debit_df = df[df["type"] == "debit"].copy()
    total_spent = debit_df["amount"].abs().sum()

    if total_spent == 0:
        return ["No debit transactions found to analyze."]

    # normalize categories
    debit_df["category"] = debit_df["category"].fillna("Other").str.strip().str.title()

    category_spend = debit_df.groupby("category")["amount"].sum().abs()

    # Food recommendation
    food = category_spend.get("Food", 0)
    if food > 0:
        food_pct = food / total_spent
        if food_pct > 0.15:
            recs.append(
                f"Food spending is {food_pct:.0%} of total spend. "
                f"Reducing it by 15% could save about ₹{food * 0.15:,.0f}/month."
            )

    # Transfer recommendation
    transfer = category_spend.get("Transfer", 0)
    if transfer > 0:
        transfer_pct = transfer / total_spent
        if transfer_pct > 0.25:
            recs.append(
                f"Transfers make up {transfer_pct:.0%} of your spending. "
                "Review non-essential peer-to-peer transfers to improve savings."
            )

    # Bills
    bills = category_spend.get("Bills", 0)
    if bills > 0:
        recs.append("Your bill payments look stable and predictable.")

    # Merchant concentration
    merchant_spend = (
        debit_df.groupby("description")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    if not merchant_spend.empty:
        top_merchant = merchant_spend.index[0]
        top_amt = merchant_spend.iloc[0]
        top_pct = top_amt / total_spent

        recs.append(
            f"Your highest spend merchant is '{top_merchant}' (₹{top_amt:,.0f}, {top_pct:.0%} of total spend)."
        )

    # Large expense warning
    largest_txn = debit_df["amount"].min()
    if abs(largest_txn) > total_spent * 0.08:
        recs.append(
            "A few high-value transactions contribute heavily to your monthly outflow. Review large expenses carefully."
        )

    # fallback
    if not recs:
        recs.append("Your spending looks balanced overall. Keep monitoring monthly trends.")

    return recs