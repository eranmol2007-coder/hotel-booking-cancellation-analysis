import os
import logging

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
HIGH_RISK_FILE = os.path.join(OUTPUT_DIR, 'high_risk_segments.csv')
STATS_FILE = os.path.join(OUTPUT_DIR, 'statistical_tests.csv')

# Lead time binning
LEAD_TIME_BINS = [-1, 7, 30, 60, 90, 180, float("inf")]
LEAD_TIME_LABELS = ["0-7 Days", "8-30 Days", "31-60 Days", "61-90 Days", "91-180 Days", "181+ Days"]

# Stay duration binning
NIGHT_BINS = [0, 1, 3, 5, 7, float("inf")]
NIGHT_LABELS = ["1 Night", "2-3 Nights", "4-5 Nights", "6-7 Nights", "8+ Nights"]

# High-risk segment thresholds
HIGH_RISK_MIN_BOOKINGS = 30
HIGH_RISK_MIN_CANCELLATION_RATE = 40.0


def setup_logging():
    """Configure project-wide logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger('hotel_analysis')
