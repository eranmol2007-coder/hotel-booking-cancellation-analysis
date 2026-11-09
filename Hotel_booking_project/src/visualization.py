import os
import logging

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for script usage
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger('hotel_analysis')


# ---------------------------------------------------------------------------
# Generic / reusable chart helpers
# ---------------------------------------------------------------------------

def plot_bar_chart(data, x_col, y_col="Cancellation_Rate", title="",
                   x_label="", y_label="Cancellation Rate (%)",
                   output_dir=None, filename=None):
    """Generic bar chart with value labels on each bar."""
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(data=data, x=x_col, y=y_col)
    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.1f}%',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='bottom', fontsize=9
        )
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    if output_dir and filename:
        plt.savefig(os.path.join(output_dir, filename), dpi=150)
    plt.close()


def plot_heatmap(data_matrix, title="", x_label="", y_label="",
                 output_dir=None, filename=None):
    """Heatmap visualization for cross-tabulation analysis."""
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        data_matrix,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        cbar_kws={"label": "Cancellation Rate (%)"},
        linewidths=0.5,
    )
    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.tight_layout()
    if output_dir and filename:
        plt.savefig(os.path.join(output_dir, filename), dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# Specific chart functions
# ---------------------------------------------------------------------------

def plot_overall_cancellation(overall_stats, output_dir=None):
    """Bar chart of overall booking status with count labels."""
    categories = ['Not Cancelled', 'Cancelled']
    counts = [overall_stats['Not_Cancelled'], overall_stats['Cancelled']]
    colors = ['#2ec4b6', '#e71d36']

    plt.figure(figsize=(7, 5))
    bars = plt.bar(categories, counts, color=colors, width=0.6)
    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2., bar.get_height() + 5,
            f'{int(bar.get_height())}',
            ha='center', va='bottom', fontweight='bold'
        )
    plt.title(
        f"Overall Booking Status "
        f"(Cancellation Rate: {overall_stats['Cancellation_Rate']}%)"
    )
    plt.ylabel("Number of Bookings")
    plt.tight_layout()
    if output_dir:
        plt.savefig(os.path.join(output_dir, 'overall_cancellation.png'), dpi=150)
    plt.close()


def plot_booking_channel_comparison(channel_analysis, output_dir=None):
    """Dual-axis chart: booking volume (bars) + cancellation rate (line)."""
    sns.set_theme(style="whitegrid")
    fig, ax1 = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=channel_analysis,
        x="Booking_Channel",
        y="Total_Bookings",
        alpha=0.6,
        color="steelblue",
        ax=ax1,
    )
    ax1.set_title(
        "Booking Channel: Volume vs. Cancellation Rate",
        fontsize=14, pad=20
    )
    ax1.set_xlabel("Booking Channel", fontsize=12)
    ax1.set_ylabel("Total Bookings", color="steelblue", fontsize=12)
    ax1.tick_params(axis="y", labelcolor="steelblue")

    ax2 = ax1.twinx()
    sns.lineplot(
        data=channel_analysis,
        x="Booking_Channel",
        y="Cancellation_Rate",
        color="crimson",
        marker="o",
        linewidth=2.5,
        ax=ax2,
        sort=False,
    )
    ax2.set_ylabel("Cancellation Rate (%)", color="crimson", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="crimson")
    ax2.yaxis.set_major_formatter("{x:.1f}%")

    plt.tight_layout()
    if output_dir:
        plt.savefig(
            os.path.join(output_dir, 'booking_channel_comparison.png'), dpi=150
        )
    plt.close()


def plot_monthly_trend(monthly_analysis, output_dir=None):
    """
    Monthly trend with dual axes:
    - Stacked bars for total / cancelled booking counts
    - Line for cancellation rate (%) on secondary axis
    """
    fig, ax1 = plt.subplots(figsize=(14, 7))

    x_pos = range(len(monthly_analysis))

    # Bars: total bookings (behind) and cancelled bookings (in front)
    ax1.bar(
        x_pos, monthly_analysis['Total_Bookings'],
        alpha=0.4, color='steelblue', label='Total Bookings'
    )
    ax1.bar(
        x_pos, monthly_analysis['Cancelled_Bookings'],
        alpha=0.7, color='salmon', label='Cancelled Bookings (count)'
    )
    ax1.set_xlabel('Month', fontsize=12)
    ax1.set_ylabel('Number of Bookings', fontsize=12, color='steelblue')
    ax1.set_xticks(list(x_pos))
    ax1.set_xticklabels(monthly_analysis['Month_Str'], rotation=45, ha='right')
    ax1.legend(loc='upper left')

    # Line: cancellation rate on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(
        list(x_pos), monthly_analysis['Cancellation_Rate'],
        color='crimson', marker='o', linewidth=2.5,
        label='Cancellation Rate (%)'
    )
    ax2.set_ylabel('Cancellation Rate (%)', fontsize=12, color='crimson')
    ax2.tick_params(axis='y', labelcolor='crimson')
    ax2.legend(loc='upper right')

    plt.title('Monthly Booking Volume and Cancellation Rate', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_dir:
        plt.savefig(os.path.join(output_dir, 'monthly_trend.png'), dpi=150)
    plt.close()


def plot_hotel_type_comparison(hotel_type_data, output_dir=None):
    """Side-by-side bar chart comparing City Hotel vs Resort Hotel."""
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(
        data=hotel_type_data, x='Hotel_Type', y='Cancellation_Rate',
        hue='Hotel_Type', palette=['#2ec4b6', '#ff6b6b'], legend=False
    )
    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.1f}%',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )
    plt.title('Cancellation Rate by Hotel Type', fontsize=14)
    plt.ylabel('Cancellation Rate (%)')
    plt.xlabel('Hotel Type')
    plt.tight_layout()
    if output_dir:
        plt.savefig(
            os.path.join(output_dir, 'hotel_type_comparison.png'), dpi=150
        )
    plt.close()


def plot_revenue_impact(revenue_data, output_dir=None):
    """
    Two-panel figure:
    - Left: average booking value for retained vs. cancelled
    - Right: pie chart of revenue retained vs. lost
    """
    categories = ['Retained\nBookings', 'Cancelled\nBookings']
    values = [revenue_data['avg_retained_value'],
              revenue_data['avg_cancelled_value']]
    colors = ['#2ec4b6', '#e71d36']

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left panel: average booking value
    bars = axes[0].bar(categories, values, color=colors, width=0.5)
    for bar, val in zip(bars, values):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2., bar.get_height() + 2,
            f'${val:,.0f}', ha='center', va='bottom', fontweight='bold'
        )
    axes[0].set_title('Average Booking Value: Retained vs Cancelled')
    axes[0].set_ylabel('Average Booking Value ($)')

    # Right panel: revenue split
    labels = ['Revenue Retained', 'Revenue Lost\nto Cancellations']
    sizes = [revenue_data['revenue_retained'], revenue_data['revenue_lost']]
    axes[1].pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 10}
    )
    axes[1].set_title('Revenue Distribution')

    plt.suptitle(
        f"Revenue Impact Analysis "
        f"(Total Potential: ${revenue_data['total_potential_revenue']:,.0f})",
        fontsize=14, fontweight='bold'
    )
    plt.tight_layout()
    if output_dir:
        plt.savefig(os.path.join(output_dir, 'revenue_impact.png'), dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# Master function
# ---------------------------------------------------------------------------

def generate_all_visualizations(results, output_dir):
    """Generates and saves all visualizations to the output directory."""

    plot_overall_cancellation(results['overall'], output_dir)
    logger.info("  ✓ overall_cancellation.png")

    plot_bar_chart(
        results['season'], 'Season',
        title='Cancellation Rate by Season', x_label='Season',
        output_dir=output_dir, filename='season_analysis.png'
    )
    logger.info("  ✓ season_analysis.png")

    plot_bar_chart(
        results['room_type'], 'Room_Type',
        title='Cancellation Rate by Room Type', x_label='Room Type',
        output_dir=output_dir, filename='room_type_analysis.png'
    )
    logger.info("  ✓ room_type_analysis.png")

    plot_bar_chart(
        results['lead_time'], 'Lead_Time_Band',
        title='Cancellation Rate by Lead-Time Band', x_label='Lead-Time Band',
        output_dir=output_dir, filename='lead_time_analysis.png'
    )
    logger.info("  ✓ lead_time_analysis.png")

    plot_bar_chart(
        results['customer_type'], 'Customer_Type',
        title='Cancellation Rate by Customer Type', x_label='Customer Type',
        output_dir=output_dir, filename='customer_analysis.png'
    )
    logger.info("  ✓ customer_analysis.png")

    plot_bar_chart(
        results['deposit_type'], 'Deposit_Type',
        title='Cancellation Rate by Deposit Type', x_label='Deposit Type',
        output_dir=output_dir, filename='deposit_type_analysis.png'
    )
    logger.info("  ✓ deposit_type_analysis.png")

    plot_bar_chart(
        results['market_segment'], 'Market_Segment',
        title='Cancellation Rate by Market Segment', x_label='Market Segment',
        output_dir=output_dir, filename='market_segment_analysis.png'
    )
    logger.info("  ✓ market_segment_analysis.png")

    plot_hotel_type_comparison(results['hotel_type'], output_dir)
    logger.info("  ✓ hotel_type_comparison.png")

    plot_heatmap(
        results['heatmap_season_customer'],
        title="Cancellation Rate (%): Season vs Customer Type",
        x_label="Customer Type", y_label="Season",
        output_dir=output_dir, filename='heatmap_season_customer.png'
    )
    logger.info("  ✓ heatmap_season_customer.png")

    plot_heatmap(
        results['heatmap_room_lead'],
        title="Cancellation Rate (%): Room Type vs Lead-Time Band",
        x_label="Lead-Time Band", y_label="Room Type",
        output_dir=output_dir, filename='heatmap_room_lead.png'
    )
    logger.info("  ✓ heatmap_room_lead.png")

    plot_booking_channel_comparison(results['booking_channel'], output_dir)
    logger.info("  ✓ booking_channel_comparison.png")

    plot_monthly_trend(results['monthly'], output_dir)
    logger.info("  ✓ monthly_trend.png")

    plot_revenue_impact(results['revenue'], output_dir)
    logger.info("  ✓ revenue_impact.png")

    logger.info("All 13 visualizations generated successfully.")
