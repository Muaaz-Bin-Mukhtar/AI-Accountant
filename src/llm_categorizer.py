import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Get API key and Base URL from .env
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Safety check for missing API key
if not api_key:
    raise ValueError("❌ Missing OPENAI_API_KEY. Please check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key, base_url=base_url)

# Allowed spending categories
ALLOWED_CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills", "Pharmacy",
    "Groceries", "Entertainment", "Utilities", "Other"
]

def categorize_with_llm(df):
    """Categorize transactions using LLM if category is 'Other'."""
    unknowns = df[df["category"] == "Other"]
    if unknowns.empty:
        print("✅ No 'Other' transactions — nothing to send to LLM.")
        return df

    print(f"🔍 Sending {len(unknowns)} uncategorized transactions to LLM...")

    # Prepare transactions for LLM
    transactions = unknowns[["description", "amount"]].to_dict(orient="records")

    prompt = f"""
You are a financial transaction categorizer.
Assign each transaction one of these categories ONLY: {', '.join(ALLOWED_CATEGORIES)}.
Return a valid JSON array where each item contains:
"description", "amount", "category", and a short "rationale".

Transactions:
{json.dumps(transactions, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You must return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON safely
        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            print("❌ Failed to parse LLM response as JSON.")
            print("Response content:", content)
            return df

        # Merge categorized results back into DataFrame
        for row in result:
            desc = row.get("description")
            if desc in df["description"].values:
                df.loc[df["description"] == desc, "category"] = row.get("category", "Other")
                df.loc[df["description"] == desc, "rationale"] = row.get("rationale", "")

        print("✅ LLM categorization complete.")
        return df

    except Exception as e:
        print("❌ LLM categorization failed:", e)
        return df
