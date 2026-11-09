import os
import sys
import logging

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import LEAD_TIME_BINS, LEAD_TIME_LABELS, NIGHT_BINS, NIGHT_LABELS

logger = logging.getLogger('hotel_analysis')


def clean_data(df):
    """
    Cleans the hotel booking dataset:
    - Drops duplicate rows
    - Converts date columns to datetime
    - Drops rows with missing values in critical columns
    - Removes rows with invalid Is_Canceled values (not 0 or 1)

    Args:
        df (pd.DataFrame): Raw dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    logger.info("Starting data cleaning...")
    initial_rows = len(df)

    # Drop duplicate rows
    df = df.drop_duplicates()
    dropped = initial_rows - len(df)
    if dropped > 0:
        logger.info("Dropped %d duplicate rows.", dropped)
    else:
        logger.info("No duplicate rows found.")

    # Convert date columns to datetime
    df["Booking_Date"] = pd.to_datetime(df["Booking_Date"], errors="coerce")
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], errors="coerce")

    # Drop rows with missing values in critical columns
    critical_cols = [
        "Booking_Date", "Arrival_Date", "Is_Canceled", "Room_Type",
        "Customer_Type", "Lead_Time_Days", "Season", "Booking_Channel"
    ]
    before = len(df)
    df = df.dropna(subset=critical_cols)
    dropped_nulls = before - len(df)
    if dropped_nulls > 0:
        logger.warning("Dropped %d rows with missing values in critical columns.", dropped_nulls)
    else:
        logger.info("No missing values in critical columns.")

    # Remove rows with invalid Is_Canceled values (must be 0 or 1)
    before = len(df)
    df = df[df["Is_Canceled"].isin([0, 1])]
    dropped_invalid = before - len(df)
    if dropped_invalid > 0:
        logger.warning("Dropped %d rows with invalid Is_Canceled values.", dropped_invalid)
    else:
        logger.info("All Is_Canceled values are valid (0 or 1).")

    # Log any remaining missing values in non-critical columns
    remaining_nulls = df.isnull().sum()
    if remaining_nulls.sum() > 0:
        logger.info("Remaining missing values in non-critical columns:")
        for col, count in remaining_nulls[remaining_nulls > 0].items():
            logger.info("  %s: %d missing", col, count)

    logger.info(
        "Data cleaning completed. %d rows retained from %d original.",
        len(df), initial_rows
    )
    return df


def feature_engineering(df):
    """
    Adds derived features to the cleaned dataframe:
    - Month: booking month as a period
    - Lead_Time_Band: categorized lead time
    - Booking_Value: Room_Rate × Nights (revenue proxy)
    - Stay_Duration_Band: categorized stay length
    - Total_Guests: Adults + Children

    Args:
        df (pd.DataFrame): Cleaned dataframe.

    Returns:
        pd.DataFrame: Dataframe with new engineered features.
    """
    # Create Month column
    df['Month'] = df['Booking_Date'].dt.to_period('M')

    # Create Lead Time Band
    df["Lead_Time_Band"] = pd.cut(
        df["Lead_Time_Days"],
        bins=LEAD_TIME_BINS,
        labels=LEAD_TIME_LABELS
    )

    # Create Booking Value (revenue proxy: rate × nights)
    df["Booking_Value"] = df["Room_Rate"] * df["Nights"]

    # Create Stay Duration Band
    df["Stay_Duration_Band"] = pd.cut(
        df["Nights"],
        bins=NIGHT_BINS,
        labels=NIGHT_LABELS
    )

    # Create Total Guests
    df["Total_Guests"] = df["Adults"] + df["Children"]

    logger.info(
        "Feature engineering completed. Added: Month, Lead_Time_Band, "
        "Booking_Value, Stay_Duration_Band, Total_Guests"
    )
    return df


def preprocess(df):
    """
    Orchestrates the full preprocessing pipeline.

    Args:
        df (pd.DataFrame): Raw dataframe.

    Returns:
        pd.DataFrame: Fully processed dataframe ready for analysis.
    """
    df_clean = clean_data(df)
    df_processed = feature_engineering(df_clean)
    return df_processed


if __name__ == "__main__":
    from config import setup_logging
    from src.data_loader import load_data

    setup_logging()
    df = load_data()
    if df is not None:
        df_processed = preprocess(df)
        print(df_processed.head())
        print(df_processed.dtypes)
