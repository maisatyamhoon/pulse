import os
import pandas as pd
from google import genai
from app.services.compare import compare_statements

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def compare_with_llm(records_a, records_b):
    comparison = compare_statements(records_a, records_b)

    summary = comparison["summary"]
    cat_df = pd.DataFrame(comparison["category_changes"])

    top_changes = cat_df.sort_values("change", ascending=False).head(5)

    change_lines = "\n".join([
        f"- {row['category']}: ₹{row['change']:,.2f}"
        for _, row in top_changes.iterrows()
    ])

    prompt = f"""
You are Pulse, an AI finance copilot.

Compare these two months and explain what changed.

Previous month:
- Spend: ₹{summary['previous_spend']:,.2f}
- Income: ₹{summary['previous_income']:,.2f}
- Net: ₹{summary['previous_net']:,.2f}

Current month:
- Spend: ₹{summary['current_spend']:,.2f}
- Income: ₹{summary['current_income']:,.2f}
- Net: ₹{summary['current_net']:,.2f}

Top category changes:
{change_lines}

Explain:
1. What got worse
2. What improved
3. Biggest behavior change
4. What to fix next month

Be concise, practical, and specific.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    comparison["llm_insight"] = response.text
    return comparison