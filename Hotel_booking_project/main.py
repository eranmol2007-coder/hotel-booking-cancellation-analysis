import os
import sys

# Ensure project root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    OUTPUT_DIR, PROCESSED_DATA_DIR, PROCESSED_DATA_FILE,
    HIGH_RISK_FILE, STATS_FILE, setup_logging,
    HIGH_RISK_MIN_BOOKINGS, HIGH_RISK_MIN_CANCELLATION_RATE
)
from src.data_loader import load_data
from src.preprocessing import preprocess
from src.analysis import run_all_analysis
from src.visualization import generate_all_visualizations
from src.utils import create_directory_if_not_exists, save_dataframe_to_csv, format_percentage


def main():
    logger = setup_logging()
    logger.info("Starting Hotel Booking Cancellation Analysis Project...")

    # Ensure output directories exist
    create_directory_if_not_exists(OUTPUT_DIR)
    create_directory_if_not_exists(PROCESSED_DATA_DIR)

    # ------------------------------------------------------------------
    # 1. Load Data
    # ------------------------------------------------------------------
    logger.info("--- Step 1: Loading Data ---")
    df_raw = load_data()
    if df_raw is None:
        logger.error("Failed to load data. Exiting.")
        return

    # ------------------------------------------------------------------
    # 2. Preprocess Data
    # ------------------------------------------------------------------
    logger.info("--- Step 2: Preprocessing Data ---")
    df_processed = preprocess(df_raw)

    # Save processed data for Power BI / downstream tools
    df_export = df_processed.copy()
    if 'Month' in df_export.columns:
        df_export['Month'] = df_export['Month'].astype(str)
    save_dataframe_to_csv(df_export, PROCESSED_DATA_FILE, "processed data (Power BI ready)")

    # ------------------------------------------------------------------
    # 3. Analyze Data
    # ------------------------------------------------------------------
    logger.info("--- Step 3: Running Analysis ---")
    results = run_all_analysis(
        df_processed,
        min_bookings=HIGH_RISK_MIN_BOOKINGS,
        min_rate=HIGH_RISK_MIN_CANCELLATION_RATE
    )

    # Print key findings
    overall = results['overall']
    logger.info("=== KEY FINDINGS ===")
    logger.info(
        "Overall: %d bookings, %d cancelled (%s)",
        overall['Total_Bookings'], overall['Cancelled'],
        format_percentage(overall['Cancellation_Rate'])
    )

    # Revenue impact
    rev = results['revenue']
    logger.info("Revenue Impact:")
    logger.info("  Total potential revenue: $%.2f", rev['total_potential_revenue'])
    logger.info(
        "  Revenue lost to cancellations: $%.2f (%s)",
        rev['revenue_lost'], format_percentage(rev['revenue_lost_pct'])
    )
    logger.info("  Avg retained booking value: $%.2f", rev['avg_retained_value'])
    logger.info("  Avg cancelled booking value: $%.2f", rev['avg_cancelled_value'])

    # Statistical tests summary
    logger.info("Statistical Significance (Chi-Square, α=0.05):")
    for _, row in results['chi_square'].iterrows():
        sig_label = "SIGNIFICANT" if row['Significant_at_0.05'] else "not significant"
        logger.info(
            "  %s: χ²=%.2f, p=%.6f (%s)",
            row['Variable'], row['Chi_Square'], row['P_Value'], sig_label
        )

    # Save high-risk segments to CSV
    save_dataframe_to_csv(results['high_risk'], HIGH_RISK_FILE, "high-risk segments")
    if len(results['high_risk']) == 0:
        logger.info(
            "No segments met the high-risk threshold "
            "(≥%d bookings AND ≥%.0f%% cancellation rate).",
            HIGH_RISK_MIN_BOOKINGS, HIGH_RISK_MIN_CANCELLATION_RATE
        )

    # Save statistical test results to CSV
    save_dataframe_to_csv(results['chi_square'], STATS_FILE, "statistical test results")

    # ------------------------------------------------------------------
    # 4. Generate Visualizations
    # ------------------------------------------------------------------
    logger.info("--- Step 4: Generating Visualizations ---")
    generate_all_visualizations(results, OUTPUT_DIR)
    logger.info("All outputs saved to %s", OUTPUT_DIR)

    logger.info("=== Project execution completed successfully. ===")


if __name__ == "__main__":
    main()
