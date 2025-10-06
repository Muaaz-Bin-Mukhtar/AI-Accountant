import pandas as pd
import matplotlib.pyplot as plt

def summarize_spending(df):
    # Group by category and sum amounts
    summary = df.groupby("category")["amount"].sum().reset_index()
    summary = summary.sort_values(by="amount", ascending=False)

    # Calculate percentage share
    total = summary["amount"].sum()
    summary["percentage"] = (summary["amount"] / total * 100).round(2)

    print("\n--- Spending Summary by Category ---")
    print(summary)

    return summary


def plot_spending(summary):
    plt.figure(figsize=(8, 5))
    plt.bar(summary["category"], summary["amount"])
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (PKR)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
