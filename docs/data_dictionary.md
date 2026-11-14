# Cleaned Data Dictionary

## tourism_hotel_monthly_2022_2025.csv

| Field | Type | Definition |
|---|---|---|
| Date | Date | First day of the reporting month, added for Power BI time analysis. |
| Year | Integer | Calendar year. |
| MonthNumber | Integer | Calendar month number from 1 to 12. |
| MonthName | Text | English calendar month name. |
| YearMonth | Text | Original monthly join key in `YYYYMM` format. |
| VisitorArrivals | Integer | Total visitor arrivals during the month. |
| HotelOccupancyRatePct | Number | Published monthly hotel room occupancy rate in percent. |
| AverageRoomRateHKD | Number | Published monthly average achieved hotel room rate in Hong Kong dollars. |

## visitor_arrivals_monthly_2019_2025.csv

Contains the date fields and official monthly Total visitor arrivals for the longer recovery trend.

## tourism_annual_summary_2019_2025.csv

| Field | Type | Definition |
|---|---|---|
| Year | Integer | Calendar year. |
| VisitorArrivals | Integer | Official annual Total visitor arrivals. |
| VisitorRecoveryVs2019Pct | Number | Annual visitor arrivals as a percentage of the 2019 total. |
| AverageHotelOccupancyRatePct | Number | Arithmetic mean of the 12 published monthly occupancy rates for 2022–2025. |
| AverageRoomRateHKD | Number | Arithmetic mean of the 12 published monthly achieved room rates for 2022–2025. |
