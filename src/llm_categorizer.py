import os
import json
import re
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


def categorize_with_llm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize transactions using LLM if category is 'Other'.
    Returns DataFrame with updated 'category' only.
    """

    # Filter transactions with 'Other' category
    df_to_categorize = df[df['category'] == 'Other'].copy()
    if df_to_categorize.empty:
        print("ℹ️ No transactions with category 'Other' to categorize.")
        return df

    print(f"🔍 Sending {len(df_to_categorize)} uncategorized transactions to LLM...")

    # Prepare transactions for LLM
    transactions = df_to_categorize[["description", "amount"]].to_dict(orient="records")

    prompt = f"""
You are a financial transaction categorizer.
Assign each transaction one of the categories.
There should be no vague category like 'Other'.
Return ONLY a valid JSON array, no explanations, no markdown, no text.
Each item must contain:
- "description"
- "amount"
- "category"

Transactions:
{json.dumps(transactions, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You must return ONLY valid JSON array. Nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Debug: print raw LLM response
        print("🔹 LLM raw response:\n", content)

        # Extract JSON array using regex
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if not match:
            print("❌ No JSON array found in LLM response.")
            return df

        try:
            result = json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print("❌ Failed to parse extracted JSON:", e)
            return df

        # Merge categorized results back into DataFrame
        for row in result:
            desc = row.get("description")
            if desc in df["description"].values:
                df.loc[df["description"] == desc, "category"] = row.get("category", "Other")

        print("✅ LLM categorization complete.")
        return df

    except Exception as e:
        print("❌ LLM categorization failed:", e)
        return df
