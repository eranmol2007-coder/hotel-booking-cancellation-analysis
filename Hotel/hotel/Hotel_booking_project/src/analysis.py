import pandas as pd
import numpy as np

def calculate_overall_cancellation(df):
    """Calculates overall cancellation rate."""
    total_bookings = len(df)
    cancelled = df["Is_Canceled"].sum()
    not_cancelled = total_bookings - cancelled
    cancellation_rate = cancelled / total_bookings * 100
    
    return {
        "Total_Bookings": total_bookings,
        "Cancelled": cancelled,
        "Not_Cancelled": not_cancelled,
        "Cancellation_Rate": round(cancellation_rate, 2)
    }

def analyze_by_dimension(df, dimension):
    """
    Analyzes cancellation rate by a given dimension.
    """
    analysis = (
        df.groupby(dimension, observed=False)
          .agg(
              Total_Bookings=("Booking_ID", "count"),
              Cancelled_Bookings=("Is_Canceled", "sum"),
              Cancellation_Rate=("Is_Canceled", "mean")
          )
          .reset_index()
    )
    analysis["Cancellation_Rate"] *= 100
    return analysis.sort_values("Cancellation_Rate", ascending=False)

def analyze_high_risk_segments(df, min_bookings, min_rate):
    """
    Identifies high-risk booking segments based on multiple dimensions.
    """
    segment_analysis = (
        df.groupby(["Season", "Room_Type", "Lead_Time_Band", "Customer_Type"], observed=False)
          .agg(
              Total_Bookings=("Booking_ID", "count"),
              Cancelled_Bookings=("Is_Canceled", "sum"),
              Cancellation_Rate=("Is_Canceled", "mean")
          )
          .reset_index()
    )
    segment_analysis["Cancellation_Rate"] *= 100
    
    high_risk = segment_analysis[
        (segment_analysis["Total_Bookings"] >= min_bookings) &
        (segment_analysis["Cancellation_Rate"] >= min_rate)
    ].sort_values("Cancellation_Rate", ascending=False)
    
    return high_risk

def calculate_heatmap_data(df, index, columns):
    """
    Prepares data for heatmap visualization.
    """
    heatmap_data = (
        df.groupby([index, columns], observed=False)["Is_Canceled"]
        .mean()
        .reset_index()
    )
    heatmap_data["Is_Canceled"] *= 100
    pivot_matrix = heatmap_data.pivot(
        index=index, columns=columns, values="Is_Canceled"
    )
    return pivot_matrix

def analyze_monthly_trend(df):
    """
    Analyzes monthly booking and cancellation trends.
    """
    monthly_analysis = df.groupby('Month').agg(
        Total_Bookings=('Is_Canceled', 'count'),
        Cancelled_Bookings=('Is_Canceled', 'sum'),
        Cancellation_Rate=('Is_Canceled', 'mean')
    ).reset_index()
    
    monthly_analysis['Cancellation_Rate'] = monthly_analysis['Cancellation_Rate'] * 100
    
    # Convert Period to string for plotting purposes if needed
    monthly_analysis['Month_Str'] = monthly_analysis['Month'].astype(str)
    return monthly_analysis

def run_all_analysis(df, min_bookings=30, min_rate=40.0):
    """
    Runs all analyses and returns a dictionary of results.
    """
    results = {}
    
    results['overall'] = calculate_overall_cancellation(df)
    results['season'] = analyze_by_dimension(df, "Season")
    results['room_type'] = analyze_by_dimension(df, "Room_Type")
    results['lead_time'] = analyze_by_dimension(df, "Lead_Time_Band")
    results['customer_type'] = analyze_by_dimension(df, "Customer_Type")
    results['booking_channel'] = analyze_by_dimension(df, "Booking_Channel")
    results['deposit_type'] = analyze_by_dimension(df, "Deposit_Type")
    results['history'] = analyze_by_dimension(df, "Previous_Cancellations")
    results['high_risk'] = analyze_high_risk_segments(df, min_bookings, min_rate)
    results['monthly'] = analyze_monthly_trend(df)
    
    # Heatmap data
    results['heatmap_season_customer'] = calculate_heatmap_data(df, "Season", "Customer_Type")
    results['heatmap_room_lead'] = calculate_heatmap_data(df, "Room_Type", "Lead_Time_Band")
    
    return results
