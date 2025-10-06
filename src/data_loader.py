import pandas as pd

def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Load transactions from a CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} transactions from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
