import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "https://pulse-a00c.onrender.com"

st.set_page_config(page_title="Pulse", layout="wide")

st.title("Pulse — Finance AI")

mode = st.radio(
    "Choose Mode",
    ["Analyze One Statement", "Compare Two Statements"],
    horizontal=True
)

# =========================================================
# MODE 1: SINGLE STATEMENT
# =========================================================
if mode == "Analyze One Statement":
    st.subheader("Single Statement Analysis")

    uploaded = st.file_uploader("Upload statement", type=["pdf"], key="single")

    if uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE}/upload", files=files)

        if response.status_code == 200:
            data = response.json()

            records = data.get("records", [])
            insights = data.get("insights", [])
            recommendations = data.get("recommendations", [])
            score = data.get("score", {})

            if not records:
                st.warning("No transactions found.")
                st.stop()

            df = pd.DataFrame(records)

            total_credit = df[df["type"] == "credit"]["amount"].sum()
            total_debit = abs(df[df["type"] == "debit"]["amount"].sum())
            net = total_credit - total_debit

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Credit", f"₹{total_credit:,.2f}")
            c2.metric("Total Debit", f"₹{total_debit:,.2f}")
            c3.metric("Net", f"₹{net:,.2f}")

            st.subheader("Financial Health Score")
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Spending Discipline", f"{score.get('spending_discipline', 0)}/100")
            s2.metric("Savings Health", f"{score.get('savings_health', 0)}/100")
            s3.metric("Risk Score", f"{score.get('risk_score', 0)}/100")
            s4.metric("Overall Score", f"{score.get('overall_score', 0)}/100")

            st.subheader("Transactions")
            st.dataframe(df, use_container_width=True)

            st.subheader("AI Insights")
            for insight in insights:
                st.info(insight)

            st.subheader("Smart Recommendations")
            for rec in recommendations:
                st.warning(rec)

            st.subheader("Ask Pulse")
            question = st.text_input("Ask anything about your money")

            if question:
                qa_response = requests.post(
                    f"{API_BASE}/ask",
                    json={"records": records, "question": question}
                )

                if qa_response.status_code == 200:
                    st.success(qa_response.json()["answer"])

# =========================================================
# MODE 2: COMPARE TWO STATEMENTS
# =========================================================
else:
    st.subheader("Compare Two Statements")

    file_a = st.file_uploader("Upload Previous Statement", type=["pdf"], key="a")
    file_b = st.file_uploader("Upload Current Statement", type=["pdf"], key="b")

    if file_a and file_b:
        if st.button("Compare Statements"):
            files_a = {"file": (file_a.name, file_a.getvalue(), "application/pdf")}
            files_b = {"file": (file_b.name, file_b.getvalue(), "application/pdf")}

            res_a = requests.post(f"{API_BASE}/upload", files=files_a)
            res_b = requests.post(f"{API_BASE}/upload", files=files_b)

            if res_a.status_code == 200 and res_b.status_code == 200:
                data_a = res_a.json()
                data_b = res_b.json()

                compare_res = requests.post(
                    f"{API_BASE}/compare",
                    json={
                        "records_a": data_a["records"],
                        "records_b": data_b["records"]
                    }
                )

                if compare_res.status_code == 200:
                    comp = compare_res.json()
                    summary = comp["summary"]

                    st.subheader("Comparison Summary")

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Spend Change", f"₹{summary['spend_change']:,.2f}")
                    c2.metric("Income Change", f"₹{summary['income_change']:,.2f}")
                    c3.metric("Net Change", f"₹{summary['net_change']:,.2f}")

                    st.subheader("Category Changes")
                    cat_df = pd.DataFrame(comp["category_changes"])
                    st.dataframe(cat_df, use_container_width=True)

                    fig = px.bar(
                        cat_df,
                        x="category",
                        y="change",
                        title="Category Spend Change"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.subheader("AI Comparison Insight")
                    st.success(comp["llm_insight"])