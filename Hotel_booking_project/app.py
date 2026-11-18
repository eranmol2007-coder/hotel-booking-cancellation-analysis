import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hotel Booking & Cancellation Intelligence",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished UI appearance
st.markdown("""
<style>
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 14px 18px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] label {
        color: #475569;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
    }

    /* Badges & Callout styling */
    .badge-sig {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-not-sig {
        background-color: #f1f5f9;
        color: #64748b;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
    }
    .risk-high {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .risk-med {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .risk-low {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .insight-card {
        background-color: #f0fdf4 !important;
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%) !important;
        border: 1px solid #bfdbfe !important;
        border-left: 5px solid #2563eb !important;
        padding: 16px 20px !important;
        border-radius: 8px !important;
        margin-bottom: 18px !important;
        color: #0f172a !important;
    }
    .insight-card strong,
    .insight-card span,
    .insight-card p,
    .insight-card li,
    .insight-card ul,
    .insight-card div {
        color: #0f172a !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Path Resolution & Core Imports
# -----------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    CURRENT_DIR,
    os.path.join(CURRENT_DIR, "hotel-booking-cancellation-analysis", "Hotel_booking_project"),
    os.path.join(CURRENT_DIR, "Hotel_booking_project"),
    os.path.dirname(CURRENT_DIR),
]

PROJECT_ROOT = None
for p in POSSIBLE_PATHS:
    if os.path.exists(os.path.join(p, "config.py")) and os.path.exists(os.path.join(p, "src", "preprocessing.py")):
        PROJECT_ROOT = p
        break

if PROJECT_ROOT is None:
    PROJECT_ROOT = CURRENT_DIR

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from config import (
        RAW_DATA_FILE, PROCESSED_DATA_FILE,
        LEAD_TIME_BINS, LEAD_TIME_LABELS, NIGHT_BINS, NIGHT_LABELS,
        HIGH_RISK_MIN_BOOKINGS, HIGH_RISK_MIN_CANCELLATION_RATE
    )
    from src.data_loader import load_data
    from src.preprocessing import preprocess
    from src.analysis import (
        calculate_overall_cancellation,
        analyze_by_dimension,
        analyze_high_risk_segments,
        calculate_heatmap_data,
        analyze_monthly_trend,
        analyze_revenue_impact,
        run_chi_square_tests
    )
except Exception as e:
    st.error(f"Error loading project modules from {PROJECT_ROOT}: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. Data Loading with Caching
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading hotel bookings data...")
def get_data():
    """Load and preprocess the dataset once and cache the result."""
    df_raw = load_data()
    if df_raw is None:
        # Fallback if raw file not found at default path
        fallback_path = os.path.join(PROJECT_ROOT, "data", "raw", "hotel_bookings.csv")
        df_raw = pd.read_csv(fallback_path)
    df_clean = preprocess(df_raw)
    return df_clean

raw_df = get_data()

# -----------------------------------------------------------------------------
# 4. Sidebar: Global Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&auto=format&fit=crop&q=60", use_container_width=True)
    st.title("🏨 Hotel Analytics")
    st.caption("Booking & Cancellation Intelligence System")
    st.markdown("---")
    
    st.subheader("Filter Dataset")
    
    # Hotel Type
    hotel_types = ["All"] + sorted(list(raw_df["Hotel_Type"].dropna().unique()))
    selected_hotel_type = st.selectbox("Hotel Type", hotel_types, index=0)
    
    # Season
    seasons = ["All"] + sorted(list(raw_df["Season"].dropna().unique()))
    selected_season = st.selectbox("Season", seasons, index=0)
    
    # Deposit Type
    deposit_types = ["All"] + sorted(list(raw_df["Deposit_Type"].dropna().unique()))
    selected_deposit = st.selectbox("Deposit Type", deposit_types, index=0)
    
    # Customer Type
    customer_types = ["All"] + sorted(list(raw_df["Customer_Type"].dropna().unique()))
    selected_customer = st.selectbox("Customer Type", customer_types, index=0)
    
    # Room Type
    room_types = ["All"] + sorted(list(raw_df["Room_Type"].dropna().unique()))
    selected_room = st.selectbox("Room Type", room_types, index=0)

    # Booking Channel
    channels = ["All"] + sorted(list(raw_df["Booking_Channel"].dropna().unique()))
    selected_channel = st.selectbox("Booking Channel", channels, index=0)

    # Lead Time Band
    lead_bands = ["All"] + list(raw_df["Lead_Time_Band"].cat.categories) if hasattr(raw_df["Lead_Time_Band"], "cat") else ["All"]
    selected_lead = st.selectbox("Lead Time Band", lead_bands, index=0)
    
    st.markdown("---")
    
    # Filter reset button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# Apply filters
df = raw_df.copy()
if selected_hotel_type != "All":
    df = df[df["Hotel_Type"] == selected_hotel_type]
if selected_season != "All":
    df = df[df["Season"] == selected_season]
if selected_deposit != "All":
    df = df[df["Deposit_Type"] == selected_deposit]
if selected_customer != "All":
    df = df[df["Customer_Type"] == selected_customer]
if selected_room != "All":
    df = df[df["Room_Type"] == selected_room]
if selected_channel != "All":
    df = df[df["Booking_Channel"] == selected_channel]
if selected_lead != "All":
    df = df[df["Lead_Time_Band"] == selected_lead]

with st.sidebar:
    st.metric("Records Matching Filters", f"{len(df):,} / {len(raw_df):,}")
    active_filters_count = sum([
        selected_hotel_type != "All", selected_season != "All",
        selected_deposit != "All", selected_customer != "All",
        selected_room != "All", selected_channel != "All", selected_lead != "All"
    ])
    if active_filters_count > 0:
        st.info(f"⚡ {active_filters_count} active filter(s) applied.")
    else:
        st.success("Displaying full dataset (1,000 bookings).")


# -----------------------------------------------------------------------------
# 5. Core Metric Calculations
# -----------------------------------------------------------------------------
if len(df) == 0:
    st.warning("⚠️ No bookings match the selected combination of filters. Please broaden your filter criteria in the sidebar.")
    st.stop()

overall = calculate_overall_cancellation(df)
revenue = analyze_revenue_impact(df)

# Header Title
st.title("🏨 Hotel Booking & Cancellation Analysis")
st.markdown(
    "Explore cancellation patterns, risk drivers, revenue implications, "
    "and actionable retention strategies through an interactive analytical dashboard."
)

# -----------------------------------------------------------------------------
# 6. Tab Navigation
# -----------------------------------------------------------------------------
tab_overview, tab_dimensional, tab_heatmaps, tab_data = st.tabs([
    "📊 Overview & KPIs",
    "🔍 Dimensional Drivers",
    "🗺️ Heatmaps & Matrix",
    "📋 Data & Management Report"
])


# =============================================================================
# TAB 1: OVERVIEW & KPIS
# =============================================================================
with tab_overview:
    st.subheader("Key Performance Indicators")
    
    # Metric cards row
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Bookings", f"{overall['Total_Bookings']:,}")
    kpi2.metric(
        "Cancellation Rate",
        f"{overall['Cancellation_Rate']:.1f}%",
        f"{overall['Cancelled']} cancelled",
        delta_color="inverse"
    )
    kpi3.metric("Total Potential Revenue", f"${revenue['total_potential_revenue']:,.0f}")
    kpi4.metric(
        "Revenue Lost",
        f"${revenue['revenue_lost']:,.0f}",
        f"{revenue['revenue_lost_pct']:.1f}% lost",
        delta_color="inverse"
    )
    kpi5.metric("Revenue Retained", f"${revenue['revenue_retained']:,.0f}")
    
    st.markdown("")
    
    # Insight banner
    st.markdown("""
    <div class="insight-card" style="color: #0f172a !important;">
        <strong style="color: #0f172a !important; font-size: 1.05rem;">💡 Strategic Executive Takeaways:</strong>
        <ul style="margin-bottom: 0; padding-left: 20px; color: #0f172a !important;">
            <li style="color: #0f172a !important; margin-top: 6px;"><strong style="color: #0f172a !important;">Disproportionate Financial Impact:</strong> While cancellations account for <strong style="color: #0f172a !important;">19.1% of volume</strong>, they represent <strong style="color: #0f172a !important;">21.1% of lost revenue</strong> because cancelled bookings carry a higher average value (<strong style="color: #0f172a !important;">$409.83</strong> vs <strong style="color: #0f172a !important;">$362.34</strong>).</li>
            <li style="color: #0f172a !important; margin-top: 6px;"><strong style="color: #0f172a !important;">Only Deposit Type is Statistically Significant (p = 0.00015):</strong> Counterintuitively, Non-Refundable bookings exhibit the highest cancellation rate (29.6%), indicating it serves as a risk marker rather than a deterrent.</li>
            <li style="color: #0f172a !important; margin-top: 6px;"><strong style="color: #0f172a !important;">Lead Time is the Dominant Pattern:</strong> Guests booking 61+ days ahead cancel at nearly <strong style="color: #0f172a !important;">3× the rate (29.4%)</strong> of last-minute bookings (10.2%).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview visual charts
    col_chart1, col_chart2 = st.columns([1, 2])
    
    with col_chart1:
        st.markdown("##### 📌 Booking Outcome Split")
        status_df = pd.DataFrame({
            "Status": ["Retained (Checked In)", "Cancelled"],
            "Count": [overall["Not_Cancelled"], overall["Cancelled"]],
            "Color": ["#10b981", "#ef4444"]
        })
        donut = alt.Chart(status_df).mark_arc(innerRadius=65).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(
                field="Status",
                type="nominal",
                scale=alt.Scale(domain=["Retained (Checked In)", "Cancelled"], range=["#10b981", "#ef4444"]),
                legend=alt.Legend(orient="bottom", title=None)
            ),
            tooltip=["Status", "Count"]
        ).properties(height=300)
        st.altair_chart(donut, use_container_width=True)
        
    with col_chart2:
        st.markdown("##### 📈 Monthly Booking Volume & Cancellation Rate")
        monthly_df = analyze_monthly_trend(df)
        
        # Dual-axis chart with Altair
        base = alt.Chart(monthly_df).encode(x=alt.X("Month_Str:N", title="Booking Month", sort=None))
        
        bars = base.mark_bar(opacity=0.6, color="#3b82f6").encode(
            y=alt.Y("Total_Bookings:Q", title="Total Bookings"),
            tooltip=["Month_Str", "Total_Bookings", "Cancelled_Bookings", alt.Tooltip("Cancellation_Rate:Q", format=".1f", title="Cancel Rate %")]
        )
        
        line = base.mark_line(color="#dc2626", strokeWidth=3, point=True).encode(
            y=alt.Y("Cancellation_Rate:Q", title="Cancellation Rate (%)", scale=alt.Scale(zero=False)),
            tooltip=["Month_Str", alt.Tooltip("Cancellation_Rate:Q", format=".1f", title="Cancel Rate %")]
        )
        
        combo = alt.layer(bars, line).resolve_scale(y="independent").properties(height=300)
        st.altair_chart(combo, use_container_width=True)

    # Seasonal & Channel Breakdown cards
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("##### 🍂 Seasonal Cancellation Profile")
        season_df = analyze_by_dimension(df, "Season")
        season_chart = alt.Chart(season_df).mark_bar().encode(
            x=alt.X("Season:N", sort="-y", title="Season"),
            y=alt.Y("Cancellation_Rate:Q", title="Cancellation Rate (%)"),
            color=alt.Color("Cancellation_Rate:Q", scale=alt.Scale(scheme="reds"), legend=None),
            tooltip=["Season", "Total_Bookings", "Cancelled_Bookings", alt.Tooltip("Cancellation_Rate:Q", format=".1f")]
        ).properties(height=240)
        st.altair_chart(season_chart, use_container_width=True)
        
    with col_s2:
        st.markdown("##### 🌐 Booking Channel Profile")
        channel_df = analyze_by_dimension(df, "Booking_Channel")
        channel_chart = alt.Chart(channel_df).mark_bar().encode(
            x=alt.X("Booking_Channel:N", sort="-y", title="Channel"),
            y=alt.Y("Cancellation_Rate:Q", title="Cancellation Rate (%)"),
            color=alt.Color("Cancellation_Rate:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=["Booking_Channel", "Total_Bookings", "Cancelled_Bookings", alt.Tooltip("Cancellation_Rate:Q", format=".1f")]
        ).properties(height=240)
        st.altair_chart(channel_chart, use_container_width=True)


# =============================================================================
# TAB 2: DIMENSIONAL ROOT CAUSE DRIVERS
# =============================================================================
with tab_dimensional:
    st.subheader("Cancellation Drivers & Dimensional Analysis")
    st.caption("Investigate how cancellation rates vary across customer profiles, booking behaviors, and room categories.")
    
    selected_dim = st.selectbox(
        "Choose Dimension to Analyze:",
        [
            "Lead Time Band (Advance Window)",
            "Deposit Type (Payment Security)",
            "Season (Time of Year)",
            "Room Type (Accommodation Category)",
            "Booking Channel (Acquisition Source)",
            "Customer Type (Guest Profile)",
            "Market Segment (Distribution Segment)",
            "Special Requests (Engagement Marker)",
            "Hotel Type (City vs. Resort)",
            "Stay Duration Band (Length of Stay)"
        ]
    )
    
    dim_col_map = {
        "Lead Time Band (Advance Window)": "Lead_Time_Band",
        "Deposit Type (Payment Security)": "Deposit_Type",
        "Season (Time of Year)": "Season",
        "Room Type (Accommodation Category)": "Room_Type",
        "Booking Channel (Acquisition Source)": "Booking_Channel",
        "Customer Type (Guest Profile)": "Customer_Type",
        "Market Segment (Distribution Segment)": "Market_Segment",
        "Special Requests (Engagement Marker)": "Special_Requests",
        "Hotel Type (City vs. Resort)": "Hotel_Type",
        "Stay Duration Band (Length of Stay)": "Stay_Duration_Band",
    }
    
    col_name = dim_col_map[selected_dim]
    dim_data = analyze_by_dimension(df, col_name)
    
    col_d1, col_d2 = st.columns([3, 2])
    
    with col_d1:
        st.markdown(f"##### Cancellation Rate by {selected_dim}")
        
        # Highlight highest rate bar with custom colors
        chart = alt.Chart(dim_data).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X(f"{col_name}:N", sort="-y", title=selected_dim),
            y=alt.Y("Cancellation_Rate:Q", title="Cancellation Rate (%)", scale=alt.Scale(domain=[0, max(dim_data["Cancellation_Rate"].max() * 1.25, 35)])),
            color=alt.Color(
                "Cancellation_Rate:Q",
                scale=alt.Scale(scheme="orangered"),
                legend=alt.Legend(title="Cancel %")
            ),
            tooltip=[col_name, "Total_Bookings", "Cancelled_Bookings", alt.Tooltip("Cancellation_Rate:Q", format=".2f")]
        )
        
        text = chart.mark_text(
            align="center",
            baseline="bottom",
            dy=-5,
            fontWeight="bold"
        ).encode(
            text=alt.Text("Cancellation_Rate:Q", format=".1f")
        )
        
        st.altair_chart((chart + text).properties(height=360), use_container_width=True)
        
    with col_d2:
        st.markdown("##### Detailed Breakdown Table")
        display_df = dim_data.copy()
        display_df["% of Total Bookings"] = (display_df["Total_Bookings"] / display_df["Total_Bookings"].sum() * 100).round(1)
        st.dataframe(
            display_df.style.format({
                "Cancellation_Rate": "{:.2f}%",
                "% of Total Bookings": "{:.1f}%",
                "Total_Bookings": "{:,}",
                "Cancelled_Bookings": "{:,}"
            }).background_gradient(subset=["Cancellation_Rate"], cmap="Reds"),
            use_container_width=True,
            hide_index=True
        )
        
        # Specific explanatory notes based on dimension
        if col_name == "Deposit_Type":
            st.error(
                "🚨 **Key Insight — The Deposit Paradox:** Non-Refundable bookings have a 29.6% cancellation rate, "
                "nearly double the 16.1% rate for No Deposit bookings! This is statistically significant (p = 0.00015). "
                "Non-refundable rates are likely selected by high-uncertainty travelers attempting to secure the cheapest rate."
            )
        elif col_name == "Lead_Time_Band":
            st.warning(
                "⏰ **Lead Time Pattern:** Strong upward trend. 91–180 Days ahead cancels at 29.4%, while 0–7 Days cancels at 10.2%. "
                "Cancellations accelerate heavily once lead time exceeds 60 days."
            )
        elif col_name == "Special_Requests":
            st.info(
                "🛎️ **Guest Engagement Effect:** Guests submitting 2 or 3 special requests have lower cancellation rates (13.6% - 15.2%), "
                "indicating higher travel intent and trip investment."
            )


# =============================================================================
# TAB 3: CROSS-DIMENSIONAL HEATMAPS & MATRIX
# =============================================================================
with tab_heatmaps:
    st.subheader("Cross-Dimensional Interaction Heatmaps")
    st.caption("Evaluate how two variables interact to reveal hidden micro-segments with extreme cancellation rates.")
    
    heatmap_choice = st.radio(
        "Select Heatmap View:",
        ["Season × Customer Type", "Room Type × Lead Time Band", "🛠️ Custom Multi-Dimension Matrix"],
        horizontal=True
    )
    
    if heatmap_choice == "Season × Customer Type":
        st.markdown("##### Heatmap: Season vs. Customer Type Cancellation Rate (%)")
        pivot = calculate_heatmap_data(df, "Season", "Customer_Type")
        
        fig, ax = plt.subplots(figsize=(9, 4.5))
        sns.heatmap(
            pivot, annot=True, fmt=".1f", cmap="YlOrRd",
            cbar_kws={"label": "Cancellation Rate (%)"}, linewidths=1, ax=ax,
            vmin=0, vmax=35
        )
        ax.set_ylabel("Season", fontsize=11, fontweight="bold")
        ax.set_xlabel("Customer Type", fontsize=11, fontweight="bold")
        st.pyplot(fig)
        plt.close(fig)
        
    elif heatmap_choice == "Room Type × Lead Time Band":
        st.markdown("##### Heatmap: Room Type vs. Lead Time Band Cancellation Rate (%)")
        pivot = calculate_heatmap_data(df, "Room_Type", "Lead_Time_Band")
        
        fig, ax = plt.subplots(figsize=(10, 4.5))
        sns.heatmap(
            pivot, annot=True, fmt=".1f", cmap="YlOrRd",
            cbar_kws={"label": "Cancellation Rate (%)"}, linewidths=1, ax=ax,
            vmin=0, vmax=45
        )
        ax.set_ylabel("Room Type", fontsize=11, fontweight="bold")
        ax.set_xlabel("Lead Time Band", fontsize=11, fontweight="bold")
        st.pyplot(fig)
        plt.close(fig)
        
    else:
        st.markdown("##### Build Your Own Custom Heatmap")
        hm_cols = [
            "Season", "Room_Type", "Customer_Type", "Booking_Channel",
            "Deposit_Type", "Hotel_Type", "Market_Segment", "Lead_Time_Band",
            "Stay_Duration_Band"
        ]
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            row_dim = st.selectbox("Row Dimension (Y-Axis)", hm_cols, index=0)
        with col_h2:
            col_dim = st.selectbox("Column Dimension (X-Axis)", hm_cols, index=7)
            
        if row_dim == col_dim:
            st.error("Please select two different dimensions for the heatmap.")
        else:
            custom_pivot = calculate_heatmap_data(df, row_dim, col_dim)
            if custom_pivot.empty:
                st.warning("No overlapping records for this combination in the filtered data.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.heatmap(
                    custom_pivot, annot=True, fmt=".1f", cmap="magma_r",
                    cbar_kws={"label": "Cancellation Rate (%)"}, linewidths=0.8, ax=ax
                )
                ax.set_ylabel(row_dim, fontsize=11, fontweight="bold")
                ax.set_xlabel(col_dim, fontsize=11, fontweight="bold")
                st.pyplot(fig)
                plt.close(fig)


# =============================================================================
# TAB 4: DATA EXPLORER & MANAGEMENT REPORT
# =============================================================================
with tab_data:
    subtab_data, subtab_report = st.tabs(["📊 Data Explorer", "📄 Management Report & Recommendations"])
    
    with subtab_data:
        st.subheader("Explore Dataset")
        st.caption("Filter and export full records.")
        
        # Search box
        search_query = st.text_input("🔍 Search Booking ID (e.g. HB100010):")
        display_data = df.copy()
        if search_query:
            display_data = display_data[display_data["Booking_ID"].str.contains(search_query, case=False, na=False)]
            
        # Select columns to display
        all_cols = list(display_data.columns)
        default_cols = ["Booking_ID", "Hotel_Type", "Season", "Room_Type", "Customer_Type", "Lead_Time_Days", "Deposit_Type", "Room_Rate", "Nights", "Booking_Value", "Is_Canceled"]
        selected_view_cols = st.multiselect("Columns to Display", all_cols, default=[c for c in default_cols if c in all_cols])
        
        st.dataframe(display_data[selected_view_cols], use_container_width=True, height=400)
        
        csv_data = display_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="hotel_bookings_filtered.csv",
            mime="text/csv"
        )
        
    with subtab_report:
        report_path = os.path.join(PROJECT_ROOT, "report.md")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()
            st.markdown(report_content)
        else:
            st.info("Report file report.md not found in project root.")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px 0;'>"
    "Hotel Booking Cancellation Analytics Platform • Antigravity Engineering • Streamlit Production Release"
    "</div>",
    unsafe_allow_html=True
)
