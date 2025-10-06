import streamlit as st
from src.dataloader import load_data
from src.analyzer import analyze_data
from src.categorizer import categorize_data

st.set_page_config(page_title="Data Intelligence Dashboard", layout="wide")

st.title("📊 AI Data Intelligence Dashboard")
st.write("Upload a dataset below to get instant AI-powered insights.")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 1️⃣ Load data
    with st.spinner("Loading data..."):
        df = load_data(uploaded_file)
    st.success("Data loaded successfully!")
    st.dataframe(df.head())

    # 2️⃣ Analyze data
    with st.spinner("Analyzing dataset..."):
        analysis_results = analyze_data(df)
    st.subheader("🧠 Data Analysis Insights")
    st.write(analysis_results)

    # 3️⃣ Categorize / Summarize
    with st.spinner("Categorizing and summarizing insights..."):
        categories = categorize_data(analysis_results)
    st.subheader("🏷️ Categorized Summary")
    st.write(categories)

else:
    st.info("👆 Upload a dataset to begin analysis.")
