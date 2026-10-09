import os
import sys

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR, PROCESSED_DATA_FILE
from src.data_loader import load_data
from src.preprocessing import preprocess
from src.analysis import run_all_analysis
from src.visualization import generate_all_visualizations

def main():
    print("Starting Hotel Booking Cancellation Analysis Project...")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # 1. Load Data
    print("\n--- 1. Loading Data ---")
    df_raw = load_data()
    if df_raw is None:
        print("Failed to load data. Exiting.")
        return
        
    # 2. Preprocess Data
    print("\n--- 2. Preprocessing Data ---")
    df_processed = preprocess(df_raw)
    
    # Save the processed data for Power BI dashboards
    print(f"Saving processed data to: {PROCESSED_DATA_FILE}")
    # Convert 'Month' period column to string before saving to CSV for Power BI compatibility
    if 'Month' in df_processed.columns:
        df_processed['Month'] = df_processed['Month'].astype(str)
    df_processed.to_csv(PROCESSED_DATA_FILE, index=False)
    print("Processed data saved successfully!")
    
    # 3. Analyze Data
    print("\n--- 3. Running Analysis ---")
    results = run_all_analysis(df_processed)
    
    # Print some key findings
    print("\nKey Findings:")
    print(f"Overall Cancellation Rate: {results['overall']['Cancellation_Rate']}%")
    
    print("\nHigh-Risk Segments (Top 5):")
    print(results['high_risk'].head(5))
    
    # 4. Generate Visualizations
    print("\n--- 4. Generating Visualizations ---")
    generate_all_visualizations(results, OUTPUT_DIR)
    print(f"Visualizations saved to {OUTPUT_DIR}")
    
    print("\nProject execution completed successfully.")

if __name__ == "__main__":
    main()
