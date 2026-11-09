"""Unit tests for analysis functions."""
import pytest
import pandas as pd

from src.analysis import (
    calculate_overall_cancellation,
    analyze_by_dimension,
    analyze_high_risk_segments,
    calculate_heatmap_data,
    analyze_revenue_impact,
)


# ---------------------------------------------------------------------------
# calculate_overall_cancellation
# ---------------------------------------------------------------------------

class TestOverallCancellation:
    def test_basic(self):
        df = pd.DataFrame({
            'Booking_ID': ['B1', 'B2', 'B3', 'B4', 'B5'],
            'Is_Canceled': [1, 0, 0, 1, 0],
        })
        result = calculate_overall_cancellation(df)
        assert result['Total_Bookings'] == 5
        assert result['Cancelled'] == 2
        assert result['Not_Cancelled'] == 3
        assert result['Cancellation_Rate'] == 40.0

    def test_all_cancelled(self):
        df = pd.DataFrame({'Is_Canceled': [1, 1, 1]})
        result = calculate_overall_cancellation(df)
        assert result['Cancellation_Rate'] == 100.0
        assert result['Not_Cancelled'] == 0

    def test_none_cancelled(self):
        df = pd.DataFrame({'Is_Canceled': [0, 0, 0, 0]})
        result = calculate_overall_cancellation(df)
        assert result['Cancellation_Rate'] == 0.0
        assert result['Cancelled'] == 0

    def test_single_row(self):
        df = pd.DataFrame({'Is_Canceled': [1]})
        result = calculate_overall_cancellation(df)
        assert result['Total_Bookings'] == 1
        assert result['Cancellation_Rate'] == 100.0


# ---------------------------------------------------------------------------
# analyze_by_dimension
# ---------------------------------------------------------------------------

class TestAnalyzeByDimension:
    def test_basic_grouping(self):
        df = pd.DataFrame({
            'Booking_ID': ['B1', 'B2', 'B3', 'B4'],
            'Is_Canceled': [1, 0, 1, 0],
            'Season': ['Summer', 'Summer', 'Winter', 'Winter'],
        })
        result = analyze_by_dimension(df, 'Season')
        assert len(result) == 2
        assert 'Cancellation_Rate' in result.columns
        assert 'Total_Bookings' in result.columns

    def test_sorted_descending(self):
        df = pd.DataFrame({
            'Booking_ID': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'],
            'Is_Canceled': [1, 1, 0, 0, 0, 0],
            'Season': ['Summer', 'Summer', 'Summer', 'Winter', 'Winter', 'Winter'],
        })
        result = analyze_by_dimension(df, 'Season')
        rates = result['Cancellation_Rate'].tolist()
        assert rates[0] >= rates[1], "Results should be sorted descending by rate"

    def test_single_category(self):
        df = pd.DataFrame({
            'Booking_ID': ['B1', 'B2'],
            'Is_Canceled': [1, 0],
            'Room': ['A', 'A'],
        })
        result = analyze_by_dimension(df, 'Room')
        assert len(result) == 1
        assert result.iloc[0]['Cancellation_Rate'] == 50.0


# ---------------------------------------------------------------------------
# analyze_high_risk_segments
# ---------------------------------------------------------------------------

class TestHighRiskSegments:
    @pytest.fixture
    def sample_df(self):
        """Create a small DataFrame with enough rows in one segment."""
        rows = []
        for i in range(40):
            rows.append({
                'Booking_ID': f'B{i}',
                'Is_Canceled': 1 if i < 20 else 0,  # 50% cancellation
                'Season': 'Summer',
                'Room_Type': 'Standard',
                'Lead_Time_Band': '0-7 Days',
                'Customer_Type': 'Transient',
            })
        return pd.DataFrame(rows)

    def test_finds_high_risk(self, sample_df):
        result = analyze_high_risk_segments(sample_df, min_bookings=30, min_rate=40.0)
        assert len(result) == 1
        assert result.iloc[0]['Cancellation_Rate'] == 50.0

    def test_threshold_too_high(self, sample_df):
        result = analyze_high_risk_segments(sample_df, min_bookings=30, min_rate=60.0)
        assert len(result) == 0

    def test_min_bookings_not_met(self, sample_df):
        result = analyze_high_risk_segments(sample_df, min_bookings=50, min_rate=40.0)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# calculate_heatmap_data
# ---------------------------------------------------------------------------

class TestHeatmapData:
    def test_basic_pivot(self):
        df = pd.DataFrame({
            'Season': ['Summer', 'Summer', 'Winter', 'Winter'],
            'Customer_Type': ['A', 'B', 'A', 'B'],
            'Is_Canceled': [1, 0, 0, 1],
        })
        result = calculate_heatmap_data(df, 'Season', 'Customer_Type')
        assert result.shape == (2, 2)

    def test_drops_all_nan_columns(self):
        df = pd.DataFrame({
            'Season': pd.Categorical(['Summer', 'Summer'], categories=['Summer', 'Winter']),
            'Customer_Type': pd.Categorical(['A', 'A'], categories=['A', 'B']),
            'Is_Canceled': [1, 0],
        })
        result = calculate_heatmap_data(df, 'Season', 'Customer_Type')
        # 'B' column and 'Winter' row should be dropped (all NaN)
        assert 'B' not in result.columns
        assert 'Winter' not in result.index


# ---------------------------------------------------------------------------
# analyze_revenue_impact
# ---------------------------------------------------------------------------

class TestRevenueImpact:
    def test_basic(self):
        df = pd.DataFrame({
            'Is_Canceled': [1, 0, 0],
            'Booking_Value': [500.0, 300.0, 200.0],
        })
        result = analyze_revenue_impact(df)
        assert result['total_potential_revenue'] == 1000.0
        assert result['revenue_lost'] == 500.0
        assert result['revenue_retained'] == 500.0
        assert result['revenue_lost_pct'] == 50.0
        assert result['avg_cancelled_value'] == 500.0
        assert result['avg_retained_value'] == 250.0
