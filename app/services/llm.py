import os
import pandas as pd
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_llm(records, question: str) -> str:
    print("GEMINI KEY FOUND:", bool(os.getenv("GEMINI_API_KEY")))

    df = pd.DataFrame(records)

    if df.empty:
        return "I could not find enough transaction data to answer that."

    total_credit = df[df["type"] == "credit"]["amount"].sum()
    total_debit = abs(df[df["type"] == "debit"]["amount"].sum())
    net = total_credit - total_debit

    top_categories = (
        df[df["type"] == "debit"]
        .groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .head(5)
    )

    top_merchants = (
        df[df["type"] == "debit"]
        .groupby("description")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .head(5)
    )

    category_text = "\n".join(
        [f"- {cat}: ₹{amt:,.2f}" for cat, amt in top_categories.items()]
    )

    merchant_text = "\n".join(
        [f"- {merchant}: ₹{amt:,.2f}" for merchant, amt in top_merchants.items()]
    )

    prompt = f"""
You are Pulse, an AI finance copilot.

User financial summary:
- Total income: ₹{total_credit:,.2f}
- Total spend: ₹{total_debit:,.2f}
- Net savings: ₹{net:,.2f}

Top spending categories:
{category_text}

Top merchants:
{merchant_text}

User question:
{question}

Answer like a sharp personal finance advisor.
Be concise, practical, and specific.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text