# Data Cleaning Log

## Source preservation

The official downloads in `data/raw/` are retained without editing. SHA-256 checksums and source URLs are recorded in `data/source_manifest.json`.

## Cleaning operations

### Visitor arrivals

- Read the official C&SD API JSON response.
- Selected `sv = VIS_ARR` and `REGIONDesc = Total`.
- Used official annual records for 2019–2025.
- Used official monthly records for January 2019–December 2025.
- Excluded regional market shares from the main analysis because the source classification changed in October 2024.
- No visitor-arrival value was rounded, imputed or redistributed.

### Hotel occupancy and room rate

- Read the two official monthly CSV files.
- Standardized `Year-Month` as a six-character key in `YYYYMM` format.
- Selected January 2022–December 2025, the complete common four-year period.
- Joined visitor arrivals, occupancy and room rate one-to-one by `YearMonth`.
- Added typed date, year, month number and English month name fields for Power BI.
- No occupancy or room-rate value was changed.

### Annual summary

- Visitor totals use the official annual visitor-arrival records.
- `VisitorRecoveryVs2019Pct` is calculated as annual arrivals divided by the 2019 total, multiplied by 100.
- Annual occupancy and room-rate figures are arithmetic means of the 12 published monthly observations.
- Empty hotel fields for 2019–2021 mean that those years are outside the chosen complete hotel-analysis period; they are not zeroes.

## Quality checks

- 48 expected monthly rows for 2022–2025: passed.
- Unique `YearMonth` join key: passed.
- Missing required monthly values: 0.
- Negative required values: 0.
- Occupancy values outside 0–100%: 0.
- Official source values modified: no.

## Material limitations

- The visitor-market classification changed from country/region of residence to nationality/region on 16 October 2024. Long-term regional-share comparisons would not be like-for-like.
- Monthly associations among arrivals, occupancy and room rate are descriptive. They do not establish causality and may partly reflect their shared recovery over time.
- The hotel datasets retain only the most recent five years, so the common complete joined analysis uses 2022–2025.
