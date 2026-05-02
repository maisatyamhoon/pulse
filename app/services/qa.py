import pandas as pd
from app.services.llm import ask_llm


def answer_question(records, question: str) -> str:
    try:
        return ask_llm(records, question)
    except Exception as e:
        return f"LLM ERROR: {str(e)}"

    df = pd.DataFrame(records)

    if df.empty:
        return "No transactions found."