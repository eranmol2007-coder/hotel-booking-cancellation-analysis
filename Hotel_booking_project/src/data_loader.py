import os
import sys
import logging

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import RAW_DATA_FILE

logger = logging.getLogger('hotel_analysis')


def load_data(file_path=RAW_DATA_FILE):
    """
    Load raw hotel bookings data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame or None: The loaded DataFrame, or None on failure.
    """
    try:
        df = pd.read_csv(file_path)
        logger.info("Data loaded successfully from %s", file_path)
        logger.info("Dataset shape: %d rows × %d columns", df.shape[0], df.shape[1])
        return df
    except FileNotFoundError:
        logger.error("Data file not found: %s", file_path)
        return None
    except Exception as e:
        logger.error("Error loading data from %s: %s", file_path, e)
        return None


if __name__ == "__main__":
    from config import setup_logging
    setup_logging()
    df = load_data()
    if df is not None:
        print(df.head())
        print(df.info())
