"""Unit tests for preprocessing functions."""
import pytest
import pandas as pd

from src.preprocessing import clean_data, feature_engineering


# ---------------------------------------------------------------------------
# clean_data
# ---------------------------------------------------------------------------

class TestCleanData:
    def _make_valid_row(self, booking_id='B1', is_canceled=0):
        """Helper to create a valid row dict with all critical columns."""
        return {
            'Booking_ID': booking_id,
            'Is_Canceled': is_canceled,
            'Booking_Date': '2025-01-01',
            'Arrival_Date': '2025-01-10',
            'Room_Type': 'Standard',
            'Customer_Type': 'Transient',
            'Lead_Time_Days': 9,
            'Season': 'Winter',
            'Booking_Channel': 'Online',
        }

    def test_drops_duplicates(self):
        row = self._make_valid_row()
        df = pd.DataFrame([row, row, self._make_valid_row('B2', 1)])
        result = clean_data(df)
        assert len(result) == 2

    def test_removes_invalid_is_canceled(self):
        rows = [
            self._make_valid_row('B1', 0),
            self._make_valid_row('B2', 1),
            self._make_valid_row('B3', 2),  # invalid
        ]
        df = pd.DataFrame(rows)
        result = clean_data(df)
        assert len(result) == 2
        assert 2 not in result['Is_Canceled'].values

    def test_drops_rows_with_missing_critical_columns(self):
        rows = [
            self._make_valid_row('B1', 0),
            {**self._make_valid_row('B2', 0), 'Season': None},  # missing Season
        ]
        df = pd.DataFrame(rows)
        result = clean_data(df)
        assert len(result) == 1

    def test_converts_dates(self):
        df = pd.DataFrame([self._make_valid_row()])
        result = clean_data(df)
        assert pd.api.types.is_datetime64_any_dtype(result['Booking_Date'])
        assert pd.api.types.is_datetime64_any_dtype(result['Arrival_Date'])

    def test_clean_data_preserves_all_when_valid(self):
        rows = [self._make_valid_row(f'B{i}') for i in range(5)]
        df = pd.DataFrame(rows)
        result = clean_data(df)
        assert len(result) == 5


# ---------------------------------------------------------------------------
# feature_engineering
# ---------------------------------------------------------------------------

class TestFeatureEngineering:
    def _make_clean_df(self):
        """Create a small cleaned DataFrame suitable for feature engineering."""
        return pd.DataFrame({
            'Booking_ID': ['B1', 'B2'],
            'Booking_Date': pd.to_datetime(['2025-06-01', '2025-12-15']),
            'Lead_Time_Days': [5, 95],
            'Room_Rate': [100.0, 200.0],
            'Nights': [2, 5],
            'Adults': [2, 3],
            'Children': [1, 0],
        })

    def test_adds_month(self):
        df = self._make_clean_df()
        result = feature_engineering(df)
        assert 'Month' in result.columns

    def test_adds_lead_time_band(self):
        df = self._make_clean_df()
        result = feature_engineering(df)
        assert 'Lead_Time_Band' in result.columns
        bands = result['Lead_Time_Band'].tolist()
        assert str(bands[0]) == '0-7 Days'
        assert str(bands[1]) == '91-180 Days'

    def test_adds_booking_value(self):
        df = self._make_clean_df()
        result = feature_engineering(df)
        assert 'Booking_Value' in result.columns
        assert result.iloc[0]['Booking_Value'] == 200.0   # 100 * 2
        assert result.iloc[1]['Booking_Value'] == 1000.0   # 200 * 5

    def test_adds_total_guests(self):
        df = self._make_clean_df()
        result = feature_engineering(df)
        assert 'Total_Guests' in result.columns
        assert result.iloc[0]['Total_Guests'] == 3  # 2 adults + 1 child
        assert result.iloc[1]['Total_Guests'] == 3  # 3 adults + 0 children

    def test_adds_stay_duration_band(self):
        df = self._make_clean_df()
        result = feature_engineering(df)
        assert 'Stay_Duration_Band' in result.columns
