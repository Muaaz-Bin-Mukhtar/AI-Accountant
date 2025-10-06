import pandas as pd

# Define some basic keyword-based categories
CATEGORY_KEYWORDS = {
    "Food": ["restaurant", "kfc", "pizza", "burger", "cafe", "coffee", "meal", "food", "biryani"],
    "Groceries": ["supermarket", "mart", "grocery", "store"],
    "Transport": ["uber", "careem", "fuel", "shell", "total", "petrol", "bus", "metro"],
    "Bills": ["electric", "gas", "water", "internet", "utility", "bill"],
    "Shopping": ["daraz", "mall", "clothes", "shoe", "fashion", "shop"],
    "Pharmacy": ["pharmacy", "medical", "clinic", "hospital", "med"],
    "Entertainment": ["cinema", "movie", "game", "netflix", "spotify"],
    "Other": []
}

def categorize_transaction(description):
    desc = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in desc for word in keywords):
            return category
    return "Other"

def categorize_transactions(df):
    df["category"] = df["description"].apply(categorize_transaction)
    return df
