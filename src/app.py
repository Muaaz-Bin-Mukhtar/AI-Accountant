import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from data_loader import load_transactions
from categorizer import categorize_transactions
from analyzer import summarize_spending
from summarizer import summarize_overall
from exporter import export_categorized_csv
from llm_categorizer import categorize_with_llm

# --- Streamlit App Config ---
st.set_page_config(page_title="💰 AI Expense Analyzer", layout="wide")

st.title("💰 AI-Powered Expense Categorizer & Analyzer")
st.write("Upload your CSV file to automatically categorize and analyze your transactions.")

uploaded_file = st.file_uploader("📤 Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Step 1: Load Data
    df = load_transactions(uploaded_file)
    if df.empty:
        st.error("❌ No transactions found in the uploaded file.")
    else:
        st.success("✅ Transactions loaded successfully!")
        st.dataframe(df.head(10))

        # Step 2: Basic Categorization
        st.subheader("🧮 Basic Categorization")
        df = categorize_transactions(df)
        st.dataframe(df.head(10))

        # Step 3: LLM Categorization
        st.subheader("🤖 Refining 'Other' Categories with LLM")
        with st.spinner("Contacting AI model for categorization..."):
            df = categorize_with_llm(df)
        st.success("✅ LLM-based categorization complete!")
        st.dataframe(df.head(10))

        # Step 4: Spending Summary
        st.subheader("📊 Spending Summary")
        summary = summarize_spending(df)
        st.dataframe(summary)

        # --- Bar Chart ---
        st.subheader("📈 Category-wise Spending (Bar Chart)")
        fig_bar, ax_bar = plt.subplots()
        ax_bar.bar(summary["category"], summary["amount"])
        ax_bar.set_xlabel("Category")
        ax_bar.set_ylabel("Amount (PKR)")
        ax_bar.set_title("Spending by Category")
        st.pyplot(fig_bar)

        # --- Pie Chart ---
        st.subheader("🥧 Spending Breakdown (Pie Chart)")
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(summary["amount"], labels=summary["category"], autopct="%1.1f%%", startangle=90)
        ax_pie.axis("equal")
        st.pyplot(fig_pie)

        # --- LLM Rationale ---
        st.subheader("🤖 LLM Categorization Rationale")
        if "rationale" in df.columns:
            st.dataframe(df[["description", "category", "rationale"]])
        else:
            st.info("No LLM rationale available.")

        # --- Category Filter ---
        st.subheader("🔎 Filter Transactions by Category")
        categories = ["All"] + sorted(df["category"].unique().tolist())
        selected_category = st.selectbox("Choose a category:", categories)
        if selected_category != "All":
            filtered_df = df[df["category"] == selected_category]
        else:
            filtered_df = df
        st.dataframe(filtered_df)

        # --- Overall Summary ---
        summarize_overall(df)

        # --- Download Button ---
        st.subheader("💾 Export Categorized CSV")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Categorized Transactions",
            data=csv,
            file_name="categorized_transactions.csv",
            mime="text/csv",
        )

        st.success("✅ All analyses completed successfully!")

else:
    st.info("📄 Please upload a transactions CSV file to begin.")
