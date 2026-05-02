from collections import Counter
import pandas as pd


def generate_insights(records):
    if not records:
        return [
            "No transactions found.",
        ]

    df = pd.DataFrame(records)

    debit_df = df[df["type"] == "debit"].copy()
    credit_df = df[df["type"] == "credit"].copy()

    insights = []

    # Top spending category
    if "category" in debit_df.columns and not debit_df.empty:
        top_category = (
            debit_df.groupby("category")["amount"]
            .sum()
            .abs()
            .sort_values(ascending=False)
        )

        if not top_category.empty:
            category = top_category.index[0]
            amount = top_category.iloc[0]
            insights.append(
                f"Top spending category was {category} at ₹{amount:,.2f}."
            )

    # Biggest expense
    if not debit_df.empty:
        biggest_expense = debit_df.loc[debit_df["amount"].idxmin()]
        insights.append(
            f"Largest expense was ₹{abs(biggest_expense['amount']):,.2f} "
            f"for {biggest_expense['description']}."
        )

    # Biggest income
    if not credit_df.empty:
        biggest_income = credit_df.loc[credit_df["amount"].idxmax()]
        insights.append(
            f"Highest credit was ₹{biggest_income['amount']:,.2f} "
            f"from {biggest_income['description']}."
        )

    # Net cash flow
    total_credit = credit_df["amount"].sum() if not credit_df.empty else 0
    total_debit = abs(debit_df["amount"].sum()) if not debit_df.empty else 0
    net = total_credit - total_debit

    if net > 0:
        insights.append(
            f"You had a positive net cash flow of ₹{net:,.2f} this period."
        )
    else:
        insights.append(
            f"You had a negative net cash flow of ₹{abs(net):,.2f} this period."
        )

    # Transaction frequency
    merchant_words = []
    for desc in df["description"].dropna():
        merchant_words.extend(desc.split())

    common = Counter(merchant_words).most_common(1)
    if common:
        insights.append(
            f"Most frequent merchant keyword was '{common[0][0]}'."
        )

    # Recommendation
    insights.append(
        "Consider labeling transfer payments (rent, loan, family, savings) for better financial insights."
    )

    return insights