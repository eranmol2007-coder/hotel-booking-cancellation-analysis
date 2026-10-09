import os

# Project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Output directories
OUTPUT_DIR = os.path.join(ROOT_DIR, 'outputs')

# File paths
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, 'hotel_bookings.csv')
PROCESSED_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, 'processed_hotel_bookings.csv')

# Configuration constants
LEAD_TIME_BINS = [-1, 7, 30, 60, 90, 180, float("inf")]
LEAD_TIME_LABELS = ["0-7 Days", "8-30 Days", "31-60 Days", "61-90 Days", "91-180 Days", "181+ Days"]
HIGH_RISK_MIN_BOOKINGS = 30
HIGH_RISK_MIN_CANCELLATION_RATE = 40.0
