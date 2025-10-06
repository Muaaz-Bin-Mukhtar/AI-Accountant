def summarize_overall(df):
    """Prints a readable summary of total and category-wise spending."""
    if df.empty:
        print("❌ No data to summarize.")
        return

    total = df["amount"].sum()
    print(f"\n💰 Total Spending: {total:.2f}")

    by_cat = df.groupby("category")["amount"].sum().sort_values(ascending=False)

    print("\n📂 Spending Breakdown by Category:")
    for category, amount in by_cat.items():
        percent = (amount / total) * 100
        print(f"  - {category}: {amount:.2f} ({percent:.1f}%)")

    top_cat = by_cat.idxmax()
    print(f"\n🏆 Highest spending category: {top_cat} ({by_cat.max():.2f})")

    avg = df["amount"].mean()
    print(f"📈 Average Transaction Amount: {avg:.2f}\n")
