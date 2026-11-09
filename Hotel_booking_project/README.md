# Hotel Booking Cancellation Analysis 🏨📊

## 1. Project Overview
Hotel booking cancellation is an important operational problem. Cancelled reservations create empty rooms, revenue uncertainty, inefficient staffing, and difficulty in inventory planning.

This is a **data analytics project** that analyzes 1,000 hotel reservation records to understand which booking patterns are associated with higher cancellation rates. The analysis covers **every column** in the dataset, runs **chi-square significance tests** to distinguish real patterns from noise, and quantifies the **revenue impact** of cancellations.

The project follows modular programming principles using pure Python scripts organized into a clear pipeline.

> **Data Provenance:** The dataset (`data/raw/hotel_bookings.csv`) is a synthetic/generated dataset of 1,000 booking records created for analytical practice. It is not sourced from a real hotel. Column names and value ranges are modeled after typical hotel booking systems.

---

## 2. Business Questions Addressed
1. Which seasons have the highest cancellation rate?
2. Does a longer booking lead time correspond to a higher cancellation rate?
3. Which deposit types are associated with higher cancellation rates?
4. How do booking channels and market segments compare?
5. How does hotel type (City vs Resort) affect cancellation?
6. What is the revenue impact of cancellations?
7. Are the observed differences statistically significant?
8. Which multi-dimensional booking segments represent the highest risk?

---

## 3. Project Structure

```text
├── main.py                 # Main entry point — runs the full pipeline
├── config.py               # Configuration constants and logging setup
├── data/
│   ├── raw/                # Raw dataset (hotel_bookings.csv)
│   └── processed/          # Cleaned data exported as CSV (for Power BI / dashboards)
├── src/
│   ├── __init__.py         # Package marker
│   ├── data_loader.py      # Loads the CSV with error handling
│   ├── preprocessing.py    # Cleans data and engineers new features
│   ├── analysis.py         # Groupby calculations, revenue analysis, chi-square tests
│   ├── visualization.py    # Generates 13 Matplotlib/Seaborn charts
│   └── utils.py            # Shared helper functions (directory creation, formatting, CSV export)
├── outputs/                # All generated charts + CSV exports
│   ├── *.png               # 13 visualization files
│   ├── high_risk_segments.csv   # Multi-dimensional risk analysis results
│   └── statistical_tests.csv   # Chi-square test results
├── tests/
│   ├── conftest.py         # Path setup for pytest
│   ├── test_analysis.py    # Unit tests for analysis functions
│   └── test_preprocessing.py   # Unit tests for preprocessing functions
├── report.md               # Management-ready business summary with real numbers
├── requirements.txt        # Pinned Python dependencies for reproducibility
├── .gitignore              # Standard Python .gitignore
└── LICENSE                 # MIT License
```

---

## 4. Key Results (Summary)

| Metric | Value |
|---|---|
| Overall Cancellation Rate | 19.1% (191 / 1,000) |
| Revenue Lost to Cancellations | $78,278 (21.1% of total potential) |
| Only Statistically Significant Factor | **Deposit Type** (χ² = 17.60, p = 0.00015) |
| Highest Cancellation Rate by Lead Time | 91–180 Days: 29.4% |
| Lowest Cancellation Rate by Lead Time | 0–7 Days: 10.2% |
| Highest Deposit Cancellation | Non Refund: 29.6% |
| Lowest Deposit Cancellation | No Deposit: 16.1% |

See [`report.md`](report.md) for the full management report with detailed tables and recommendations.

---

## 5. Visualizations Generated (13 charts)

| Chart | File |
|---|---|
| Overall booking status | `overall_cancellation.png` |
| Cancellation rate by season | `season_analysis.png` |
| Cancellation rate by room type | `room_type_analysis.png` |
| Cancellation rate by lead-time band | `lead_time_analysis.png` |
| Cancellation rate by customer type | `customer_analysis.png` |
| Cancellation rate by deposit type | `deposit_type_analysis.png` |
| Cancellation rate by market segment | `market_segment_analysis.png` |
| Hotel type comparison (City vs Resort) | `hotel_type_comparison.png` |
| Booking channel: volume vs. cancellation rate | `booking_channel_comparison.png` |
| Monthly booking volume and cancellation rate | `monthly_trend.png` |
| Heatmap: Season × Customer Type | `heatmap_season_customer.png` |
| Heatmap: Room Type × Lead-Time Band | `heatmap_room_lead.png` |
| Revenue impact (avg value + pie chart) | `revenue_impact.png` |

---

## 6. How to Run the Project

### Prerequisites
Python 3.10+ with `pip`.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/eranmol2007-coder/hotel-booking-cancellation-analysis.git
   cd hotel-booking-cancellation-analysis
   ```

2. **Install dependencies (pinned versions):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis pipeline:**
   ```bash
   python main.py
   ```

4. **View results:**
   - `outputs/` — all 13 charts + `high_risk_segments.csv` + `statistical_tests.csv`
   - `report.md` — full business report with numbers and recommendations
   - `data/processed/processed_hotel_bookings.csv` — cleaned data for import into Power BI or other dashboarding tools

5. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

---

## 7. Columns Analyzed

All 19 columns in the dataset are used:

| Column | How It's Used |
|---|---|
| `Booking_ID` | Row identifier for counting |
| `Hotel_Type` | City vs Resort comparison |
| `Booking_Date` | Converted to Month for trend analysis |
| `Arrival_Date` | Date parsing and validation |
| `Season` | Seasonal cancellation analysis |
| `Room_Type` | Room type comparison |
| `Customer_Type` | Customer segment analysis |
| `Lead_Time_Days` | Binned into Lead_Time_Band; key predictor |
| `Adults` | Combined into Total_Guests feature |
| `Children` | Combined into Total_Guests feature |
| `Nights` | Binned into Stay_Duration_Band; used for Booking_Value |
| `Meal_Plan` | Meal plan cancellation analysis |
| `Booking_Channel` | Channel comparison (Online, Offline, Agent, Corporate) |
| `Market_Segment` | Segment analysis (Online TA, Direct, Offline TA/TO, etc.) |
| `Deposit_Type` | **Only statistically significant factor** |
| `Room_Rate` | Multiplied by Nights for revenue analysis |
| `Previous_Cancellations` | Cancellation history analysis |
| `Special_Requests` | Engagement proxy analysis |
| `Is_Canceled` | Target variable (0/1) |

---

## 8. Technical Details

- **Logging:** Uses Python's `logging` module (not print statements) throughout the pipeline.
- **Statistical Tests:** Chi-square tests of independence via `scipy.stats.chi2_contingency` for all categorical variables.
- **Data Cleaning:** Missing values in critical columns and invalid `Is_Canceled` values are dropped (not just reported).
- **Heatmaps:** Empty combinations (e.g., the 181+ Days band with zero bookings) are automatically removed.
- **Utility Functions:** `src/utils.py` functions (`create_directory_if_not_exists`, `format_percentage`, `save_dataframe_to_csv`) are used throughout `main.py`.
- **Reproducibility:** `requirements.txt` uses pinned versions (`==`) instead of minimum versions (`>=`).

---

## 9. Limitations
- **Descriptive, Not Predictive:** No ML model is included. The analysis identifies correlations, not causes.
- **Sample Size:** With only 1,000 records, most dimensions do not reach statistical significance. Highly segmented multi-dimensional patterns lack enough bookings per cell.
- **Synthetic Data:** The dataset is generated, not from a real hotel.
- **No Power BI Dashboard:** The cleaned CSV is exported for dashboard tools, but no `.pbix` file or dashboard screenshots are included.
- **Currency:** Room rates are in an unspecified currency.

---

## 10. Learning Outcomes
- ✅ End-to-end exploratory data analysis with Pandas across all dataset columns.
- ✅ Groupby aggregation and cross-tabulation analysis.
- ✅ Chi-square statistical significance testing with SciPy.
- ✅ Revenue impact analysis using derived features.
- ✅ Professional visualizations with Matplotlib and Seaborn (13 charts).
- ✅ Modular Python project structure with logging, tests, and pinned dependencies.
- ✅ Data exported for downstream dashboarding tools (Power BI, Tableau, etc.).
