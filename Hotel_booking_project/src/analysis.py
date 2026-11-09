import os
import sys
import logging

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from scipy.stats import chi2_contingency

logger = logging.getLogger('hotel_analysis')


def calculate_overall_cancellation(df):
    """
    Calculates overall cancellation rate.

    Returns:
        dict: Total bookings, cancelled count, not-cancelled count, and rate (%).
    """
    total_bookings = len(df)
    cancelled = int(df["Is_Canceled"].sum())
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
    Analyzes cancellation rate by a given categorical dimension.

    Args:
        df (pd.DataFrame): Processed dataframe.
        dimension (str): Column name to group by.

    Returns:
        pd.DataFrame: Grouped analysis sorted by cancellation rate descending.
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
    analysis["Cancellation_Rate"] = analysis["Cancellation_Rate"].round(2)
    return analysis.sort_values("Cancellation_Rate", ascending=False)


def analyze_high_risk_segments(df, min_bookings=30, min_rate=40.0):
    """
    Identifies high-risk booking segments based on multiple dimensions.

    Segments with at least `min_bookings` bookings and a cancellation rate
    of at least `min_rate`% are flagged as high risk.

    Args:
        df (pd.DataFrame): Processed dataframe.
        min_bookings (int): Minimum number of bookings required.
        min_rate (float): Minimum cancellation rate (%) to qualify.

    Returns:
        pd.DataFrame: High-risk segments, sorted by cancellation rate descending.
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
    segment_analysis["Cancellation_Rate"] = segment_analysis["Cancellation_Rate"].round(2)

    # Filter to segments meeting both thresholds
    high_risk = segment_analysis[
        (segment_analysis["Total_Bookings"] >= min_bookings) &
        (segment_analysis["Cancellation_Rate"] >= min_rate)
    ].sort_values("Cancellation_Rate", ascending=False)

    return high_risk


def calculate_heatmap_data(df, index, columns):
    """
    Prepares a pivot matrix for heatmap visualization.
    Drops rows/columns that are entirely NaN (no bookings in that combination).

    Args:
        df (pd.DataFrame): Processed dataframe.
        index (str): Row dimension.
        columns (str): Column dimension.

    Returns:
        pd.DataFrame: Pivot matrix of cancellation rates (%).
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
    # Drop empty rows and columns (combinations with zero bookings)
    pivot_matrix = pivot_matrix.dropna(axis=1, how='all')
    pivot_matrix = pivot_matrix.dropna(axis=0, how='all')
    return pivot_matrix


def analyze_monthly_trend(df):
    """
    Analyzes monthly booking volume, cancellation counts, and cancellation rate.

    Returns:
        pd.DataFrame: Monthly trend data with rate as a percentage.
    """
    monthly_analysis = df.groupby('Month').agg(
        Total_Bookings=('Is_Canceled', 'count'),
        Cancelled_Bookings=('Is_Canceled', 'sum'),
        Cancellation_Rate=('Is_Canceled', 'mean')
    ).reset_index()

    monthly_analysis['Cancellation_Rate'] = (
        monthly_analysis['Cancellation_Rate'] * 100
    ).round(2)
    monthly_analysis['Month_Str'] = monthly_analysis['Month'].astype(str)
    return monthly_analysis


def analyze_revenue_impact(df):
    """
    Analyzes the revenue impact of cancellations using Booking_Value
    (Room_Rate × Nights).

    Returns:
        dict: Revenue statistics for cancelled vs. retained bookings.
    """
    cancelled = df[df['Is_Canceled'] == 1]
    retained = df[df['Is_Canceled'] == 0]

    total_potential = df['Booking_Value'].sum()
    revenue_lost = cancelled['Booking_Value'].sum()
    revenue_retained = retained['Booking_Value'].sum()

    return {
        'total_potential_revenue': round(total_potential, 2),
        'revenue_lost': round(revenue_lost, 2),
        'revenue_retained': round(revenue_retained, 2),
        'revenue_lost_pct': round(revenue_lost / total_potential * 100, 2),
        'avg_cancelled_value': round(cancelled['Booking_Value'].mean(), 2),
        'avg_retained_value': round(retained['Booking_Value'].mean(), 2),
        'median_cancelled_value': round(cancelled['Booking_Value'].median(), 2),
        'median_retained_value': round(retained['Booking_Value'].median(), 2),
    }


def run_chi_square_tests(df):
    """
    Runs chi-square tests of independence for each categorical variable
    against Is_Canceled. This checks whether the cancellation rate truly
    differs across categories in a statistically significant way.

    Returns:
        pd.DataFrame: Test results with chi-square statistic, p-value,
                       degrees of freedom, and significance flag (α=0.05).
    """
    categorical_cols = [
        'Season', 'Room_Type', 'Customer_Type', 'Booking_Channel',
        'Deposit_Type', 'Hotel_Type', 'Market_Segment', 'Meal_Plan'
    ]

    results = []
    for col in categorical_cols:
        if col in df.columns:
            contingency = pd.crosstab(df[col], df['Is_Canceled'])
            chi2, p, dof, expected = chi2_contingency(contingency)
            results.append({
                'Variable': col,
                'Chi_Square': round(chi2, 4),
                'P_Value': round(p, 6),
                'Degrees_of_Freedom': dof,
                'Significant_at_0.05': p < 0.05
            })
            logger.info(
                "  Chi-square test for %s: χ²=%.2f, p=%.6f %s",
                col, chi2, p,
                "(SIGNIFICANT)" if p < 0.05 else "(not significant)"
            )

    return pd.DataFrame(results)


def run_all_analysis(df, min_bookings=30, min_rate=40.0):
    """
    Runs the complete analysis pipeline and returns all results.

    Args:
        df (pd.DataFrame): Fully processed dataframe.
        min_bookings (int): Minimum bookings for high-risk segment detection.
        min_rate (float): Minimum cancellation rate (%) for high-risk flagging.

    Returns:
        dict: Dictionary of all analysis results keyed by analysis name.
    """
    results = {}

    # Overall statistics
    results['overall'] = calculate_overall_cancellation(df)
    logger.info("Overall cancellation rate: %.2f%%", results['overall']['Cancellation_Rate'])

    # Dimensional analysis — every categorical column
    results['season'] = analyze_by_dimension(df, "Season")
    results['room_type'] = analyze_by_dimension(df, "Room_Type")
    results['lead_time'] = analyze_by_dimension(df, "Lead_Time_Band")
    results['customer_type'] = analyze_by_dimension(df, "Customer_Type")
    results['booking_channel'] = analyze_by_dimension(df, "Booking_Channel")
    results['deposit_type'] = analyze_by_dimension(df, "Deposit_Type")
    results['history'] = analyze_by_dimension(df, "Previous_Cancellations")
    results['hotel_type'] = analyze_by_dimension(df, "Hotel_Type")
    results['market_segment'] = analyze_by_dimension(df, "Market_Segment")
    results['meal_plan'] = analyze_by_dimension(df, "Meal_Plan")
    results['special_requests'] = analyze_by_dimension(df, "Special_Requests")
    results['stay_duration'] = analyze_by_dimension(df, "Stay_Duration_Band")

    # High-risk multi-dimensional segments
    results['high_risk'] = analyze_high_risk_segments(df, min_bookings, min_rate)
    if len(results['high_risk']) > 0:
        logger.info("Found %d high-risk segments.", len(results['high_risk']))
    else:
        logger.info(
            "No high-risk segments found (thresholds: >=%d bookings, >=%.0f%% cancellation).",
            min_bookings, min_rate
        )

    # Monthly trends
    results['monthly'] = analyze_monthly_trend(df)

    # Heatmap cross-tabulations (empty combinations are dropped)
    results['heatmap_season_customer'] = calculate_heatmap_data(df, "Season", "Customer_Type")
    results['heatmap_room_lead'] = calculate_heatmap_data(df, "Room_Type", "Lead_Time_Band")

    # Revenue impact analysis
    results['revenue'] = analyze_revenue_impact(df)
    logger.info(
        "Revenue at risk from cancellations: $%.2f (%.1f%% of total)",
        results['revenue']['revenue_lost'],
        results['revenue']['revenue_lost_pct']
    )

    # Statistical significance testing
    logger.info("Running chi-square independence tests...")
    results['chi_square'] = run_chi_square_tests(df)

    return results
