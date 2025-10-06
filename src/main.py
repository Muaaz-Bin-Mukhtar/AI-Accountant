import os
from data_loader import load_transactions
from categorizer import categorize_transactions
from analyzer import summarize_spending, plot_spending
from summarizer import summarize_overall
from exporter import export_categorized_csv
from llm_categorizer import categorize_with_llm


def main():
    """Main entry point for the AI Accountant backend."""
    print("🚀 Starting AI Accountant pipeline...\n")

    # Resolve absolute path to CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(base_dir, "../data/transactions.csv"))

    # Step 1: Load transactions
    print("📥 Loading transactions...")
    df = load_transactions(data_path)

    if df.empty:
        print("❌ No transactions found. Exiting.")
        return

    # Step 2: Basic rule-based categorization
    print("\n🧮 Performing initial categorization...")
    df = categorize_transactions(df)
    print(df.head(10))

    # Step 3: LLM-based categorization (refine unknowns)
    print("\n🤖 Refining 'Other' transactions using LLM...")
    try:
        df = categorize_with_llm(df)
    except Exception as e:
        print(f"⚠️  Skipping LLM step due to error: {e}")

    # Step 4: Analyze spending
    print("\n📊 Generating spending summary and charts...")
    try:
        summary = summarize_spending(df)
        plot_spending(summary)
        summarize_overall(df)
    except Exception as e:
        print(f"⚠️  Analysis step failed: {e}")

    # Step 5: Export results
    print("\n💾 Exporting final categorized transactions...")
    try:
        export_categorized_csv(df)
    except Exception as e:
        print(f"⚠️  Export failed: {e}")

    print("\n✅ All steps completed successfully!")


if __name__ == "__main__":
    main()
