# Hotel Booking Cancellation Analysis — Management Report

## 1. Executive Summary
This report analyzes 1,000 hotel reservation records to identify patterns and risk factors associated with booking cancellations. With an **overall cancellation rate of 19.1%** (191 out of 1,000 bookings), the analysis quantifies the operational and revenue impact of cancellations and identifies which booking dimensions are most strongly associated with higher cancellation rates.

> **Note on Statistical Significance:** Chi-square tests of independence (α = 0.05) were run for every categorical variable. Of all dimensions tested, **only Deposit Type** shows a statistically significant relationship with cancellation (χ² = 17.60, p = 0.00015). All other dimensions (Season, Room Type, Customer Type, Booking Channel, Hotel Type, Market Segment, Meal Plan) do **not** reach statistical significance at the 0.05 level in this 1,000-record sample.

## 2. Methodology
The dataset was processed using Python in a modular pipeline (`main.py` → `data_loader` → `preprocessing` → `analysis` → `visualization`). Data was cleaned (duplicates removed, invalid values filtered), and several features were engineered (Lead-Time Bands, Booking Month, Booking Value, Stay Duration Band). Statistical significance was tested using chi-square tests of independence (scipy).

## 3. Key Findings

### 3.1 Overall Cancellation
| Metric | Value |
|---|---|
| Total Bookings | 1,000 |
| Cancelled | 191 (19.1%) |
| Not Cancelled | 809 (80.9%) |

### 3.2 Revenue Impact
Booking value is estimated as Room Rate × Nights.

| Metric | Value |
|---|---|
| Total Potential Revenue | $371,407.63 |
| Revenue Lost to Cancellations | $78,277.70 (21.1% of total) |
| Revenue Retained | $293,129.93 |
| Avg Booking Value (Cancelled) | $409.83 |
| Avg Booking Value (Retained) | $362.34 |

Cancelled bookings have a **higher average value** ($409.83) than retained bookings ($362.34), meaning cancellations disproportionately affect higher-value reservations. Cancellations account for 19.1% of bookings but 21.1% of potential revenue.

### 3.3 Seasonal Patterns
| Season | Bookings | Cancelled | Rate |
|---|---|---|---|
| Autumn | 245 | 56 | 22.86% |
| Summer | 288 | 63 | 21.88% |
| Winter | 181 | 28 | 15.47% |
| Spring | 286 | 44 | 15.38% |

Autumn and Summer show cancellation rates approximately 6–7 percentage points higher than Winter and Spring. However, the chi-square test for Season narrowly misses significance (p = 0.051), so this pattern should be monitored with more data before firm conclusions are drawn.

### 3.4 Lead Time Influence
| Lead-Time Band | Bookings | Cancelled | Rate |
|---|---|---|---|
| 91–180 Days | 160 | 47 | 29.38% |
| 61–90 Days | 133 | 39 | 29.32% |
| 31–60 Days | 261 | 45 | 17.24% |
| 8–30 Days | 289 | 44 | 15.22% |
| 0–7 Days | 157 | 16 | 10.19% |

There is a clear monotonic relationship: the further in advance a booking is made, the higher the cancellation rate. Bookings made 61+ days ahead cancel at roughly **3× the rate** of bookings made within a week. No bookings exceed 180 days in this dataset.

### 3.5 Deposit Type (Statistically Significant)
| Deposit Type | Bookings | Cancelled | Rate |
|---|---|---|---|
| Non Refund | 186 | 55 | **29.57%** |
| Refundable | 89 | 19 | 21.35% |
| No Deposit | 725 | 117 | 16.14% |

This is the **only statistically significant dimension** (χ² = 17.60, p = 0.00015). Counterintuitively, Non-Refundable deposits have the **highest** cancellation rate (29.57%), almost double the rate for No Deposit bookings (16.14%). This likely reflects selection bias: guests who are already uncertain about their plans may be routed into non-refundable bookings by the hotel or channel, making the deposit a marker of risk rather than a deterrent.

### 3.6 Customer Type
| Customer Type | Bookings | Cancelled | Rate |
|---|---|---|---|
| Group | 57 | 12 | 21.05% |
| Contract | 86 | 18 | 20.93% |
| Transient | 714 | 135 | 18.91% |
| Transient-Party | 143 | 26 | 18.18% |

Customer-type cancellation rates range only from 18.2% to 21.1%. The chi-square test is not significant (p = 0.94), indicating that customer type alone does not meaningfully predict cancellation in this sample.

### 3.7 Hotel Type
| Hotel Type | Bookings | Cancelled | Rate |
|---|---|---|---|
| City Hotel | 552 | 107 | 19.38% |
| Resort Hotel | 448 | 84 | 18.75% |

The difference is negligible (0.6 pp) and not significant (p = 0.86).

### 3.8 Booking Channel
| Channel | Bookings | Cancelled | Rate |
|---|---|---|---|
| Online | 576 | 118 | 20.49% |
| Offline | 103 | 19 | 18.45% |
| Agent | 253 | 45 | 17.79% |
| Corporate | 68 | 9 | 13.24% |

Corporate bookings have the lowest cancellation rate (13.24%) but also the lowest volume (68). Online is the highest-volume channel (576 bookings) with a 20.49% cancellation rate. The overall channel effect is not statistically significant (p = 0.47).

### 3.9 Market Segment
| Segment | Bookings | Cancelled | Rate |
|---|---|---|---|
| Corporate | 98 | 24 | 24.49% |
| Direct | 254 | 51 | 20.08% |
| Online TA | 423 | 83 | 19.62% |
| Groups | 51 | 10 | 19.61% |
| Offline TA/TO | 174 | 23 | 13.22% |

Online Travel Agents (Online TA) make up the largest segment (423 bookings, 19.62% cancellation). Offline TA/TO bookings have the lowest rate (13.22%). The overall difference is not significant (p = 0.20).

### 3.10 Room Type
| Room Type | Bookings | Cancelled | Rate |
|---|---|---|---|
| Superior | 188 | 39 | 20.74% |
| Deluxe | 276 | 53 | 19.20% |
| Standard | 459 | 86 | 18.74% |
| Suite | 77 | 13 | 16.88% |

Room type differences are small (16.9%–20.7%) and not significant (p = 0.89).

### 3.11 Special Requests
| Count | Bookings | Cancelled | Rate |
|---|---|---|---|
| 0 | 345 | 66 | 19.13% |
| 1 | 359 | 79 | 22.01% |
| 2 | 210 | 32 | 15.24% |
| 3 | 66 | 9 | 13.64% |
| 4 | 20 | 5 | 25.00% |

Bookings with 2–3 special requests show lower cancellation rates (13.6%–15.2%), though the category with 4 requests has too few bookings (n=20) to draw conclusions.

### 3.12 High-Risk Booking Segments
The multi-dimensional analysis filtered for segments (Season × Room Type × Lead-Time Band × Customer Type) with at least 30 bookings and a cancellation rate over 40%. **No segments met both thresholds** in this 1,000-record sample. The results (including the empty output) are saved to `outputs/high_risk_segments.csv` for monitoring as data grows.

## 4. Recommendations for Operational Planning

1. **Focus on Lead Time as the Strongest Predictor:**
   Bookings made 61+ days ahead cancel at ~29%, versus 10% for last-week bookings. Implement graduated engagement strategies (confirmation emails, early check-in offers) as the arrival date approaches for long-lead bookings.

2. **Revisit Non-Refundable Deposit Strategy:**
   Non-refundable bookings have the highest cancellation rate (29.57%), contrary to the assumption that deposits deter cancellations. Investigate whether non-refundable rates are attracting price-sensitive guests who are inherently more likely to cancel.

3. **Seasonal Overbooking Adjustments:**
   Autumn (22.9%) and Summer (21.9%) show elevated cancellation rates. While not yet statistically significant, consider slightly higher overbooking limits during these seasons, validated with additional data.

4. **Protect High-Value Bookings:**
   Cancelled bookings average $409.83 vs. $362.34 for retained bookings, meaning revenue impact (21.1%) is disproportionate to booking volume (19.1%). Consider dedicated retention outreach for bookings above the median value ($265.68).

5. **Corporate Channel Investment:**
   Corporate bookings show the lowest cancellation rate (13.24% by channel, 24.49% by market segment). The discrepancy between these two perspectives highlights that "Corporate" means different things in the channel vs. market-segment columns and warrants further investigation.

6. **Collect More Data:**
   With only 1,000 records, most dimensions do not reach statistical significance. Expanding the dataset will allow more confident segmentation and multi-dimensional high-risk detection.

## 5. Limitations
- **Descriptive, Not Predictive:** This analysis identifies correlations, not causes. A high cancellation rate in a segment does not prove the segment characteristics cause cancellations.
- **Sample Size:** With 1,000 records, only one variable (Deposit Type) reaches statistical significance. Multi-dimensional segments have too few bookings per cell for reliable inference.
- **Synthetic Data:** This dataset is synthetically generated for analytical practice. Real-world data would include more noise, missing values, and complex booking patterns.
- **Currency Not Specified:** Room rates are in an unspecified currency. Revenue figures should be interpreted as relative magnitudes.
- **No Predictive Model:** The current pipeline is purely descriptive. A logistic regression or decision-tree model could quantify the independent contribution of each factor.

## 6. Statistical Test Results
Full chi-square test results are saved to `outputs/statistical_tests.csv`. Summary:

| Variable | χ² | p-value | Significant? |
|---|---|---|---|
| Deposit_Type | 17.60 | 0.000151 | **Yes** |
| Season | 7.77 | 0.050959 | No (borderline) |
| Market_Segment | 5.98 | 0.200768 | No |
| Booking_Channel | 2.54 | 0.467971 | No |
| Meal_Plan | 1.85 | 0.604063 | No |
| Room_Type | 0.62 | 0.892949 | No |
| Customer_Type | 0.42 | 0.935616 | No |
| Hotel_Type | 0.03 | 0.862831 | No |
