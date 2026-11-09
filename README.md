# Hotel Booking Cancellation Analysis 🏨📊

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-green.svg)](https://pandas.pydata.org/)

> **An industry-oriented data analytics project** analyzing hotel booking cancellation patterns to identify high-risk segments and quantify revenue impact using Python, Pandas, and statistical testing.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Business Questions](#-business-questions-addressed)
- [Key Findings](#-key-findings-summary)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [Visualizations](#-visualizations-generated)
- [Technical Details](#-technical-details)
- [Dataset Information](#-dataset-information)
- [Results & Reports](#-results--reports)
- [Technologies Used](#-technologies-used)
- [Learning Outcomes](#-learning-outcomes)
- [Limitations](#-limitations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

Hotel booking cancellations create **empty rooms, revenue uncertainty, inefficient staffing**, and difficulty in inventory planning. This project analyzes **1,000 hotel reservation records** to understand which booking patterns are associated with higher cancellation rates.

### What This Project Does:
- ✅ Analyzes **all 19 columns** in the hotel booking dataset
- ✅ Runs **chi-square significance tests** to distinguish real patterns from noise
- ✅ Quantifies the **revenue impact** of cancellations ($78,278 lost revenue)
- ✅ Identifies **high-risk booking segments** across multiple dimensions
- ✅ Generates **13 professional visualizations** for stakeholder presentation
- ✅ Exports cleaned data for **Power BI/Tableau dashboards**
- ✅ Provides a **management-ready business report** with actionable recommendations

### Key Findings at a Glance:
- **19.1% overall cancellation rate** (191 out of 1,000 bookings)
- **21.1% of potential revenue lost** to cancellations ($78,278)
- **Only Deposit Type** shows statistical significance (p < 0.001)
- **Lead time is the strongest predictor**: 29.4% cancellation for 91-180 day bookings vs. 10.2% for last-week bookings
- Cancelled bookings have **higher average value** ($409.83) than retained ones ($362.34)

---

## 🔍 Business Questions Addressed

1. ❓ Which **seasons** have the highest cancellation rate?
2. ❓ Does a **longer booking lead time** correspond to higher cancellation rates?
3. ❓ Which **deposit types** are associated with higher cancellations?
4. ❓ How do **booking channels** and **market segments** compare?
5. ❓ How does **hotel type** (City vs Resort) affect cancellation?
6. ❓ What is the **revenue impact** of cancellations?
7. ❓ Are the observed differences **statistically significant**?
8. ❓ Which **multi-dimensional booking segments** represent the highest risk?

---

## 📊 Key Findings (Summary)

| Metric | Value |
|--------|-------|
| **Overall Cancellation Rate** | 19.1% (191 / 1,000 bookings) |
| **Revenue Lost** | $78,278 (21.1% of total potential) |
| **Statistically Significant Factor** | **Deposit Type** (χ² = 17.60, p = 0.00015) |
| **Highest Risk Lead Time** | 91–180 Days → 29.4% cancellation |
| **Lowest Risk Lead Time** | 0–7 Days → 10.2% cancellation |
| **Highest Risk Deposit** | Non-Refundable → 29.6% cancellation |
| **Lowest Risk Deposit** | No Deposit → 16.1% cancellation |
| **Highest Risk Season** | Autumn → 22.9% cancellation |
| **Lowest Risk Season** | Spring → 15.4% cancellation |

### 💡 Surprising Insight:
**Non-refundable deposits have the HIGHEST cancellation rate** (29.6%) — almost double the rate for bookings with no deposit (16.1%). This counterintuitive finding suggests that non-refundable bookings may be selected by guests who are already uncertain about their plans, making the deposit a **marker of risk rather than a deterrent**.

📄 **Full business report with detailed recommendations:** [`Hotel_booking_project/report.md`](Hotel_booking_project/report.md)

---

## 📁 Project Structure

```
hotel-booking-cancellation-analysis/
│
├── Hotel_booking_project/          # Main project directory
│   ├── main.py                     # 🚀 Main entry point — runs the full pipeline
│   ├── config.py                   # ⚙️ Configuration constants and logging setup
│   │
│   ├── data/
│   │   ├── raw/                    # 📥 Raw dataset (hotel_bookings.csv)
│   │   └── processed/              # 📤 Cleaned data (for Power BI / Tableau)
│   │
│   ├── src/                        # 💻 Source code modules
│   │   ├── __init__.py
│   │   ├── data_loader.py          # Loads CSV with error handling
│   │   ├── preprocessing.py        # Data cleaning + feature engineering
│   │   ├── analysis.py             # Groupby calculations, revenue analysis, chi-square tests
│   │   ├── visualization.py        # Generates 13 Matplotlib/Seaborn charts
│   │   └── utils.py                # Shared helper functions
│   │
│   ├── outputs/                    # 📊 All generated visualizations + CSV exports
│   │   ├── *.png                   # 13 visualization files
│   │   ├── high_risk_segments.csv  # Multi-dimensional risk analysis
│   │   └── statistical_tests.csv   # Chi-square test results
│   │
│   ├── tests/                      # ✅ Unit tests (pytest)
│   │   ├── conftest.py
│   │   ├── test_analysis.py
│   │   └── test_preprocessing.py
│   │
│   ├── report.md                   # 📈 Management-ready business report
│   ├── requirements.txt            # 📦 Pinned Python dependencies
│   ├── .gitignore                  # Git ignore patterns
│   └── LICENSE                     # MIT License
│
└── README.md                       # 📖 This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.10+** (recommended: 3.10 or 3.11)
- **pip** package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/eranmol2007-coder/hotel-booking-cancellation-analysis.git
cd hotel-booking-cancellation-analysis
```

### Step 2: Install Dependencies
All dependencies are pinned to specific versions for reproducibility:

```bash
cd Hotel_booking_project
pip install -r requirements.txt
```

**Dependencies installed:**
- `pandas==2.2.3` — Data manipulation
- `numpy==1.26.4` — Numerical operations
- `matplotlib==3.9.2` — Visualization
- `seaborn==0.13.2` — Statistical visualizations
- `scipy==1.14.1` — Chi-square statistical tests
- `pytest==8.3.3` — Unit testing

---

## ▶️ How to Run

### Run the Complete Analysis Pipeline

```bash
cd Hotel_booking_project
python main.py
```

### What Happens When You Run:
1. ✅ **Loads raw data** from `data/raw/hotel_bookings.csv`
2. ✅ **Cleans and preprocesses** (removes duplicates, handles missing values, engineers features)
3. ✅ **Runs comprehensive analysis** (groupby aggregations, revenue calculations, chi-square tests)
4. ✅ **Generates 13 visualizations** saved to `outputs/` folder
5. ✅ **Exports results** to CSV files:
   - `data/processed/processed_hotel_bookings.csv` (for Power BI/Tableau)
   - `outputs/high_risk_segments.csv` (risk analysis)
   - `outputs/statistical_tests.csv` (significance test results)
6. ✅ **Logs key findings** to console and log file

### Expected Runtime:
⏱️ **~10-15 seconds** on standard hardware

### Run Unit Tests

```bash
pytest tests/ -v
```

---

## 📊 Visualizations Generated

The project creates **13 professional visualizations** in the `outputs/` folder:

| # | Visualization | File Name | Description |
|---|---------------|-----------|-------------|
| 1 | Overall Booking Status | `overall_cancellation.png` | Pie chart showing cancelled vs. not cancelled |
| 2 | Season Analysis | `season_analysis.png` | Cancellation rate by season (Autumn, Summer, Winter, Spring) |
| 3 | Room Type Analysis | `room_type_analysis.png` | Cancellation rate by room type (Standard, Deluxe, Superior, Suite) |
| 4 | Lead Time Analysis | `lead_time_analysis.png` | Cancellation rate by lead-time bands (0-7, 8-30, 31-60, 61-90, 91-180 days) |
| 5 | Customer Analysis | `customer_analysis.png` | Cancellation rate by customer type (Transient, Group, Contract, etc.) |
| 6 | Deposit Type Analysis | `deposit_type_analysis.png` | **Most important** — shows Non-Refundable has highest cancellation rate |
| 7 | Market Segment | `market_segment_analysis.png` | Comparison across Online TA, Direct, Corporate, etc. |
| 8 | Hotel Type Comparison | `hotel_type_comparison.png` | City Hotel vs. Resort Hotel cancellation rates |
| 9 | Booking Channel | `booking_channel_comparison.png` | Volume and cancellation rate by channel (Online, Agent, Corporate, Offline) |
| 10 | Monthly Trend | `monthly_trend.png` | Booking volume and cancellation rate over time |
| 11 | Heatmap: Season × Customer | `heatmap_season_customer.png` | Cross-dimensional cancellation patterns |
| 12 | Heatmap: Room × Lead Time | `heatmap_room_lead.png` | Room type vs. lead-time band heatmap |
| 13 | Revenue Impact | `revenue_impact.png` | Shows avg booking value and revenue lost to cancellations |

---

## 🔧 Technical Details

### Modular Architecture
The project follows **clean code principles** with a modular structure:

```
main.py → orchestrates the pipeline
   ↓
data_loader.py → loads raw CSV
   ↓
preprocessing.py → cleans data, engineers features
   ↓
analysis.py → runs statistical analysis
   ↓
visualization.py → generates charts
```

### Key Technical Features:
- ✅ **Logging:** Uses Python's `logging` module (not print statements) for professional logging
- ✅ **Error Handling:** Comprehensive try-except blocks with graceful failures
- ✅ **Statistical Rigor:** Chi-square tests of independence via `scipy.stats.chi2_contingency`
- ✅ **Data Validation:** Removes invalid `Is_Canceled` values, handles missing data
- ✅ **Feature Engineering:** Creates `Lead_Time_Band`, `Booking_Month`, `Booking_Value`, `Stay_Duration_Band`, `Total_Guests`
- ✅ **Reproducibility:** Pinned dependencies in `requirements.txt`
- ✅ **Unit Testing:** Pytest tests for analysis and preprocessing functions
- ✅ **Export Ready:** Cleaned data saved as CSV for downstream BI tools

### Statistical Methods:
- **Chi-Square Test of Independence** (α = 0.05) for categorical variables
- **Revenue Analysis:** Booking Value = Room Rate × Nights
- **Multi-Dimensional Segmentation:** Season × Room Type × Lead-Time × Customer Type

---

## 📦 Dataset Information

### Dataset Overview
- **File:** `data/raw/hotel_bookings.csv`
- **Records:** 1,000 hotel bookings
- **Columns:** 19 features
- **Target Variable:** `Is_Canceled` (0 = Not Cancelled, 1 = Cancelled)

### Data Provenance
⚠️ **This is a synthetic/generated dataset** created for analytical practice. It is **not sourced from a real hotel**. Column names and value ranges are modeled after typical hotel booking systems.

### All 19 Columns Analyzed:

| Column | Description | How It's Used |
|--------|-------------|---------------|
| `Booking_ID` | Unique booking identifier | Row counting |
| `Hotel_Type` | City Hotel or Resort Hotel | Hotel type comparison |
| `Booking_Date` | Date of booking | Converted to Month for trend analysis |
| `Arrival_Date` | Date of arrival | Date validation |
| `Season` | Season of arrival | Seasonal cancellation analysis |
| `Room_Type` | Standard, Deluxe, Superior, Suite | Room type comparison |
| `Customer_Type` | Transient, Group, Contract, etc. | Customer segment analysis |
| `Lead_Time_Days` | Days between booking and arrival | **Key predictor** — binned into bands |
| `Adults` | Number of adults | Combined into Total_Guests |
| `Children` | Number of children | Combined into Total_Guests |
| `Nights` | Number of nights stayed | Used for revenue calculation |
| `Meal_Plan` | Meal plan type | Meal plan cancellation analysis |
| `Booking_Channel` | Online, Offline, Agent, Corporate | Channel comparison |
| `Market_Segment` | Online TA, Direct, Offline TA/TO, etc. | Market segment analysis |
| `Deposit_Type` | No Deposit, Refundable, Non-Refundable | **Statistically significant factor** |
| `Room_Rate` | Rate per night | Multiplied by Nights for revenue |
| `Previous_Cancellations` | Count of past cancellations | Cancellation history analysis |
| `Special_Requests` | Number of special requests | Engagement proxy |
| `Is_Canceled` | 0 = No, 1 = Yes | **Target variable** |

---

## 📈 Results & Reports

### Output Files:

1. **`report.md`** — Comprehensive management report with:
   - Executive summary
   - Detailed findings with tables
   - Statistical test results
   - Operational recommendations
   - Limitations and next steps

2. **`outputs/statistical_tests.csv`** — Chi-square test results for all variables

3. **`outputs/high_risk_segments.csv`** — Multi-dimensional high-risk segments (if any meet threshold)

4. **`data/processed/processed_hotel_bookings.csv`** — Cleaned dataset ready for Power BI/Tableau

### Key Recommendations from Report:
1. **Focus on Lead Time:** Implement graduated engagement strategies for long-lead bookings
2. **Revisit Non-Refundable Strategy:** Investigate why non-refundable bookings have highest cancellation rates
3. **Seasonal Overbooking:** Consider higher overbooking limits in Autumn and Summer
4. **Protect High-Value Bookings:** Dedicated retention outreach for bookings above median value
5. **Corporate Channel Investment:** Corporate bookings show lowest cancellation rates

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Matplotlib** | Base visualization library |
| **Seaborn** | Statistical data visualization |
| **SciPy** | Chi-square statistical tests |
| **Pytest** | Unit testing framework |
| **Git & GitHub** | Version control |

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

- ✅ **End-to-End EDA:** Complete exploratory data analysis workflow
- ✅ **Data Wrangling:** Cleaning, validation, missing value handling
- ✅ **Feature Engineering:** Creating derived features for analysis
- ✅ **Statistical Analysis:** Chi-square tests, hypothesis testing
- ✅ **Revenue Analysis:** Business metrics calculation
- ✅ **Data Visualization:** Professional charts with Matplotlib/Seaborn
- ✅ **Modular Programming:** Clean, reusable code architecture
- ✅ **Logging & Debugging:** Professional logging practices
- ✅ **Unit Testing:** Test-driven development with Pytest
- ✅ **Documentation:** Technical and business reporting
- ✅ **Data Export:** Preparing data for BI tools

---

## ⚠️ Limitations

1. **Descriptive, Not Predictive:** This analysis identifies correlations, not causes. No machine learning model is included.

2. **Sample Size:** With only 1,000 records, most dimensions do not reach statistical significance (p < 0.05). Multi-dimensional segments lack enough bookings per cell.

3. **Synthetic Data:** The dataset is generated for practice, not from a real hotel.

4. **No Power BI Dashboard:** Cleaned CSV is exported, but no `.pbix` file or dashboard screenshots are included.

5. **Currency Not Specified:** Room rates are in an unspecified currency.

6. **No Predictive Model:** A logistic regression or decision-tree model could quantify the independent contribution of each factor (future enhancement).

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Suggested Enhancements:
- [ ] Add machine learning model (Logistic Regression, Random Forest)
- [ ] Create Power BI dashboard with `.pbix` file
- [ ] Expand dataset to 10,000+ records for better statistical power
- [ ] Add time-series forecasting for cancellation trends
- [ ] Implement automated testing with CI/CD
- [ ] Add data quality checks and validation rules

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](Hotel_booking_project/LICENSE) file for details.

---

## 👤 Author

**Eran Mol (eranmol2007-coder)**

- 🔗 GitHub: [@eranmol2007-coder](https://github.com/eranmol2007-coder)
- 📧 Project Link: [hotel-booking-cancellation-analysis](https://github.com/eranmol2007-coder/hotel-booking-cancellation-analysis)

---

## ⭐ If You Find This Useful

If this project helped you learn data analytics or Python, please consider:
- ⭐ **Starring** the repository
- 🍴 **Forking** it for your own projects
- 📣 **Sharing** it with others

---

<div align="center">

### 🏨 Happy Analyzing! 📊

*Built with ❤️ using Python, Pandas, and Data Science*

</div>
