import os

def export_categorized_csv(df, filename="categorized_transactions.csv"):
    """Export the final categorized transactions to the 'data' folder."""
    if df.empty:
        print("❌ No data to export.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_dir, "../data", filename)
    df.to_csv(output_path, index=False)
    print(f"✅ Exported categorized data to: {output_path}")
