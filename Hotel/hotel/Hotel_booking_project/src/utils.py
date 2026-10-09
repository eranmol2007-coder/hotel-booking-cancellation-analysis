import os

def create_directory_if_not_exists(directory_path):
    """
    Utility function to create a directory if it does not already exist.
    
    Args:
        directory_path (str): The path to the directory to create.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def format_percentage(value):
    """
    Utility function to format a decimal as a percentage string.
    
    Args:
        value (float): The decimal value.
        
    Returns:
        str: Formatted percentage string.
    """
    return f"{value:.2f}%"
