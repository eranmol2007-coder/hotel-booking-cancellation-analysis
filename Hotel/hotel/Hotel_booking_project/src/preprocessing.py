import pandas as pd
import numpy as np

def clean_data(df):
    """
    Cleans the hotel booking dataset.
    
    Args:
        df (pd.DataFrame): Raw dataframe
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print("Starting data cleaning...")
    
    # Check duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {initial_rows - len(df)} duplicate rows.")
    
    # Convert date columns to datetime
    df["Booking_Date"] = pd.to_datetime(df["Booking_Date"], errors="coerce")
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], errors="coerce")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print("Missing values found:")
        print(missing_values[missing_values > 0])
        
    # Check for valid binary values in Is_Canceled
    invalid_cancellations = df[~df["Is_Canceled"].isin([0, 1])]
    if len(invalid_cancellations) > 0:
        print(f"Found {len(invalid_cancellations)} rows with invalid Is_Canceled values.")
        
    print("Data cleaning completed.")
    return df

def feature_engineering(df):
    """
    Adds derived features like Month and Lead_Time_Band.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        
    Returns:
        pd.DataFrame: Dataframe with new features
    """
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import LEAD_TIME_BINS, LEAD_TIME_LABELS
    
    # Create a Month column
    df['Month'] = df['Booking_Date'].dt.to_period('M')
    
    # Create Lead Time Band
    df["Lead_Time_Band"] = pd.cut(
        df["Lead_Time_Days"],
        bins=LEAD_TIME_BINS,
        labels=LEAD_TIME_LABELS
    )
    
    return df

def preprocess(df):
    """
    Orchestrates the preprocessing steps.
    """
    df_clean = clean_data(df)
    df_processed = feature_engineering(df_clean)
    return df_processed

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import load_data
    from config import PROCESSED_DATA_FILE
    
    df = load_data()
    if df is not None:
        df_processed = preprocess(df)
        print(df_processed.head())
        # Optionally save processed data
        # df_processed.to_csv(PROCESSED_DATA_FILE, index=False)