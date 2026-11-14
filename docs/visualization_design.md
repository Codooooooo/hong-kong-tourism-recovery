# Visualization Design

## Tool allocation

- One visualization in Tableau Public.
- Two visualizations in Microsoft Power BI.
- All titles, labels, annotations and tooltips will be in English.

## Visualization 1 — Microsoft Power BI

**Working title:** Visitor Arrivals Recovered to 89% of the 2019 Level by 2025

**Purpose:** Show the scale of the collapse and subsequent recovery against the 2019 benchmark.

**Chart:** Annual column chart.

**Source table:** `tourism_annual_summary_2019_2025.csv`

**Fields:**

- Axis: `Year`
- Values: `VisitorArrivals`
- Tooltip: `VisitorRecoveryVs2019Pct`

**Design:** Use a neutral color for 2019–2024 and one accent color for 2025. Add a 2019 reference annotation and label the 2021 minimum and 2025 recovery level.

## Visualization 2 — Microsoft Power BI

**Working title:** Hotel Occupancy Rose with Visitor Arrivals, While Room Rates Varied

**Purpose:** Show the strong descriptive association between monthly visitor arrivals and hotel occupancy, with room rate as secondary context.

**Chart:** Scatter chart.

**Source table:** `tourism_hotel_monthly_2022_2025.csv`

**Fields:**

- X-axis: `VisitorArrivals`
- Y-axis: `HotelOccupancyRatePct`
- Legend: `Year`
- Details: `YearMonth`
- Size or tooltip context: `AverageRoomRateHKD`
- Tooltip: `Date`, `VisitorArrivals`, `HotelOccupancyRatePct`, `AverageRoomRateHKD`

**Design:** Use year as a restrained sequential color group, add a linear trend line and label only important points. Room-rate bubble size will be used only if it remains readable; otherwise room rate stays in the tooltip to avoid imprecise area comparisons.

**Interpretation limit:** The relationship is descriptive and partly reflects the common recovery trend. It does not prove causality.

## Visualization 3 — Tableau Public

**Working title:** Hong Kong's Tourism Recovery Spread Across the Calendar

**Purpose:** Show how the collapse and recovery unfolded month by month and reveal seasonal peaks.

**Chart:** Year-by-month highlight table or heatmap.

**Source table:** `visitor_arrivals_monthly_2019_2025.csv`

**Fields:**

- Rows: `Year`
- Columns: `MonthName`, sorted by `MonthNumber`
- Color: `VisitorArrivals`
- Tooltip: `Date`, `VisitorArrivals`

**Design:** Use one perceptually ordered color scale, show 2019–2025 in chronological order and add short annotations for the 2021 low point and the 2023–2025 recovery. Avoid a rainbow palette.

## Story sequence

1. Establish the magnitude and completeness of the recovery with the Power BI annual chart.
2. Explain the relationship between tourism volume and hotel occupancy with the Power BI scatter chart.
3. Show the monthly timing and seasonality of the recovery with the Tableau heatmap.
