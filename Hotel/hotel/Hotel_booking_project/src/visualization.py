import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_overall_cancellation(overall_stats, output_dir=None):
    categories = ['Not Cancelled', 'Cancelled']
    counts = [overall_stats['Not_Cancelled'], overall_stats['Cancelled']]
    colors = ['#2ec4b6', '#e71d36']

    plt.figure(figsize=(7, 5))
    bars = plt.bar(categories, counts, color=colors, width=0.6)
    plt.title("Overall Bookings Status")
    plt.ylabel("Number of Bookings")
    plt.tight_layout()
    if output_dir:
        plt.savefig(os.path.join(output_dir, 'overall_cancellation.png'))
    plt.close()

def plot_bar_chart(data, x_col, y_col="Cancellation_Rate", title="", x_label="", y_label="Cancellation Rate (%)", output_dir=None, filename=None):
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data, x=x_col, y=y_col)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(rotation=30)
    plt.tight_layout()
    if output_dir and filename:
        plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plot_heatmap(data_matrix, title="", x_label="", y_label="", output_dir=None, filename=None):
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
        plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plot_booking_channel_comparison(channel_analysis, output_dir=None):
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
    ax1.set_title("Booking Channel Comparison: Volume vs. Cancellation Rate", fontsize=14, pad=20)
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
        plt.savefig(os.path.join(output_dir, 'booking_channel_comparison.png'))
    plt.close()

def plot_monthly_trend(monthly_analysis, output_dir=None):
    plt.figure(figsize=(14, 7))

    plt.plot(
        monthly_analysis['Month_Str'],
        monthly_analysis['Total_Bookings'],
        marker='o',
        linewidth=2,
        label='Monthly Booking Volume'
    )

    plt.plot(
        monthly_analysis['Month_Str'],
        monthly_analysis['Cancelled_Bookings'],
        marker='o',
        linewidth=2,
        label='Monthly Cancellation Trend'
    )

    plt.title('Monthly Booking Volume and Cancellation Trend', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Bookings', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if output_dir:
        plt.savefig(os.path.join(output_dir, 'monthly_trend.png'))
    plt.close()

def generate_all_visualizations(results, output_dir):
    """Generates and saves all visualizations."""
    
    plot_overall_cancellation(results['overall'], output_dir)
    
    plot_bar_chart(results['season'], 'Season', title='Cancellation Rate by Season', 
                   x_label='Season', output_dir=output_dir, filename='season_analysis.png')
                   
    plot_bar_chart(results['lead_time'], 'Lead_Time_Band', title='Cancellation Rate by Lead-Time Band', 
                   x_label='Lead-Time Band', output_dir=output_dir, filename='lead_time_analysis.png')
                   
    plot_bar_chart(results['customer_type'], 'Customer_Type', title='Cancellation Rate by Customer Type', 
                   x_label='Customer Type', output_dir=output_dir, filename='customer_analysis.png')
                   
    plot_heatmap(results['heatmap_season_customer'], title="Cancellation Rate: Season vs Customer Type", 
                 x_label="Customer Type", y_label="Season", output_dir=output_dir, filename='heatmap_season_customer.png')
                 
    plot_heatmap(results['heatmap_room_lead'], title="Cancellation Rate (%) by Room Type vs. Lead-Time Band", 
                 x_label="Lead-Time Band", y_label="Room Type", output_dir=output_dir, filename='heatmap_room_lead.png')
                 
    plot_booking_channel_comparison(results['booking_channel'], output_dir)
    
    plot_monthly_trend(results['monthly'], output_dir)
