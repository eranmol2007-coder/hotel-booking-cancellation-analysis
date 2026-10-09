import pandas as pd
import os
import sys

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import RAW_DATA_FILE

def load_data(file_path=RAW_DATA_FILE):
    """
    Load raw hotel bookings data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        print(f"Dataset shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Test data loading
    df = load_data()
    if df is not None:
        print(df.head())
        print(df.info())
