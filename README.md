Hotel Booking Cancellation Analysis 🏨📊
1. Project Overview
Hotel booking cancellation is an important operational problem. Cancelled reservations create empty rooms, revenue uncertainty, inefficient staffing, and difficulty in inventory planning.

This is an Industry-Oriented Data Analytics Project designed to analyze hotel reservation data and understand which booking patterns are associated with higher cancellation rates.

The project focuses on cancellation rates by:

Season
Room Type
Lead Time
Customer Type
It strictly follows professional modular programming principles using pure Python scripts, avoiding notebook-based environments to ensure the solution is production-ready.

2. Business Scenario
As a Data Analyst for a hotel group, the goal is to reduce the impact of booking cancellations and improve room inventory planning by answering:

Which seasons have the highest cancellation rate?
Which room types have relatively high cancellation rates?
Does a longer booking lead time correspond to a higher cancellation rate?
Which customer types show different cancellation patterns?
Which combinations of booking characteristics represent high cancellation-risk segments?
3. Project Structure
The project code and resources are logically organized into the following structure:



├── main.py                 # Main entry point to run the analysis pipeline
  ├── config.py               # Configuration & constants
  ├── data/
  │   ├── raw/                # Contains the dataset (hotel_bookings.csv)
  │   └── processed/          # Contains data processed for Power BI
  ├── src/
  │   ├── data_loader.py      # Loads the CSV safely
  │   ├── preprocessing.py    # Cleans data and adds new features
  │   ├── analysis.py         # Performs groupby calculations and KPIs
  │   ├── visualization.py    # Generates Matplotlib/Seaborn charts
  │   └── utils.py            # Helper functions
  ├── outputs/                # Folder where all charts are saved
  ├── report.md               # Final management-ready business summary
  └── requirements.txt        # Python library dependencies
4. How to Run the Project
Prerequisites
Make sure you have Python installed. You will need pandas, numpy, matplotlib, and seaborn.

Clone the repository and navigate to the project folder:

git clone https://github.com/eranmol2007-coder/hotel-booking-cancellation-analysis.git
 cd hotel-booking-cancellation-analysis

Install the required libraries:

pip install -r requirements.txt

Run the Analysis Pipeline: Execute the main script. This will load the data, clean it, run the analysis, and generate the charts.

python main.py

View the Results:

Go to the outputs/ folder to see all the generated graphs.
Open report.md to read the business summary and operational recommendations.
The cleaned data is also automatically exported to data/processed/ for direct ingestion into Power BI.
5. Learning Outcomes Achieved
✅ Performed end-to-end exploratory data analysis with Pandas.
✅ Used groupby, aggregation, pivot tables, and categorical analysis.
✅ Created professional visualizations with Matplotlib and Seaborn.
✅ Transformed raw booking data into useful business KPIs.
✅ Maintained clean, reusable, and modular Python scripts.
