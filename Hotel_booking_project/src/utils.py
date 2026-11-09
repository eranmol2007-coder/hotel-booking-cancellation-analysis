import os
import logging
import pandas as pd

logger = logging.getLogger('hotel_analysis')


def create_directory_if_not_exists(directory_path):
    """
    Create a directory if it does not already exist.

    Args:
        directory_path (str): The path to the directory to create.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info("Created directory: %s", directory_path)


def format_percentage(value):
    """
    Format a numeric value as a percentage string.

    Args:
        value (float): The numeric value (e.g. 19.1 for 19.1%).

    Returns:
        str: Formatted percentage string like '19.10%'.
    """
    return f"{value:.2f}%"


def save_dataframe_to_csv(df, file_path, description="data"):
    """
    Save a DataFrame to CSV with logging.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): Destination file path.
        description (str): Human-readable label for log messages.
    """
    create_directory_if_not_exists(os.path.dirname(file_path))
    df.to_csv(file_path, index=False)
    logger.info("Saved %s to %s (%d rows)", description, file_path, len(df))
