import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "cleaned"
DOCS = ROOT / "data"

VISITOR_JSON = SOURCE / "visitor_arrivals_by_region_original_en.json"
OCCUPANCY_CSV = SOURCE / "hotel_room_occupancy_rate_monthly_original_en.csv"
ROOM_RATE_CSV = SOURCE / "average_achieved_hotel_room_rate_original_en.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_two_column_csv(path: Path, value_column: str) -> dict[str, float]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = {}
    for row in rows:
        period = row["Year-Month"].strip()
        value = row[value_column].strip()
        if not period or not value:
            raise ValueError(f"Blank required value in {path.name}: {row}")
        if period in result:
            raise ValueError(f"Duplicate month in {path.name}: {period}")
        result[period] = float(value)
    return result


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    CLEAN.mkdir(parents=True, exist_ok=True)
    with VISITOR_JSON.open("r", encoding="utf-8-sig") as handle:
        visitor_payload = json.load(handle)

    records = visitor_payload["dataSet"]
    total_monthly = {}
    total_annual = {}
    for row in records:
        if row.get("REGIONDesc") != "Total" or row.get("sv") != "VIS_ARR":
            continue
        period = str(row["period"])
        figure = row["figure"]
        if row.get("freq") == "M" and "201901" <= period <= "202512":
            if period in total_monthly:
                raise ValueError(f"Duplicate monthly visitor total: {period}")
            total_monthly[period] = int(figure)
        elif row.get("freq") == "Y" and "2019" <= period <= "2025":
            if period in total_annual:
                raise ValueError(f"Duplicate annual visitor total: {period}")
            total_annual[period] = int(figure)

    occupancy = read_two_column_csv(
        OCCUPANCY_CSV, "Hotel_room_occupancy_rate(%)"
    )
    room_rate = read_two_column_csv(
        ROOM_RATE_CSV, "Average_achieved_hotel_room_rate(HKD)"
    )

    expected_months = [f"{year}{month:02d}" for year in range(2022, 2026) for month in range(1, 13)]
    missing = {
        "visitor_arrivals": sorted(set(expected_months) - set(total_monthly)),
        "hotel_occupancy": sorted(set(expected_months) - set(occupancy)),
        "hotel_room_rate": sorted(set(expected_months) - set(room_rate)),
    }
    if any(missing.values()):
        raise ValueError(f"Missing months in the common 2022-2025 window: {missing}")

    monthly_rows = []
    for period in expected_months:
        date = datetime.strptime(period, "%Y%m")
        monthly_rows.append(
            {
                "Date": date.strftime("%Y-%m-01"),
                "Year": date.year,
                "MonthNumber": date.month,
                "MonthName": date.strftime("%B"),
                "YearMonth": period,
                "VisitorArrivals": total_monthly[period],
                "HotelOccupancyRatePct": int(occupancy[period]) if occupancy[period].is_integer() else occupancy[period],
                "AverageRoomRateHKD": int(room_rate[period]) if room_rate[period].is_integer() else room_rate[period],
            }
        )

    visitor_monthly_rows = []
    for period in sorted(total_monthly):
        date = datetime.strptime(period, "%Y%m")
        visitor_monthly_rows.append(
            {
                "Date": date.strftime("%Y-%m-01"),
                "Year": date.year,
                "MonthNumber": date.month,
                "MonthName": date.strftime("%B"),
                "YearMonth": period,
                "VisitorArrivals": total_monthly[period],
            }
        )

    by_year = defaultdict(list)
    for row in monthly_rows:
        by_year[row["Year"]].append(row)

    baseline_2019 = total_annual["2019"]
    annual_rows = []
    for year in range(2019, 2026):
        year_str = str(year)
        months = by_year.get(year, [])
        annual_rows.append(
            {
                "Year": year,
                "VisitorArrivals": total_annual[year_str],
                "VisitorRecoveryVs2019Pct": round(total_annual[year_str] / baseline_2019 * 100, 2),
                "AverageHotelOccupancyRatePct": round(sum(r["HotelOccupancyRatePct"] for r in months) / len(months), 2) if months else "",
                "AverageRoomRateHKD": round(sum(r["AverageRoomRateHKD"] for r in months) / len(months), 2) if months else "",
            }
        )

    monthly_path = CLEAN / "tourism_hotel_monthly_2022_2025.csv"
    visitor_monthly_path = CLEAN / "visitor_arrivals_monthly_2019_2025.csv"
    annual_path = CLEAN / "tourism_annual_summary_2019_2025.csv"

    write_csv(monthly_path, list(monthly_rows[0]), monthly_rows)
    write_csv(visitor_monthly_path, list(visitor_monthly_rows[0]), visitor_monthly_rows)
    write_csv(annual_path, list(annual_rows[0]), annual_rows)

    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_title": "From Collapse to Recovery: Hong Kong Tourism and Hotel Performance, 2019-2025",
        "sources": [
            {
                "file": VISITOR_JSON.name,
                "dataset": "Visitor arrivals by nationality/region",
                "dataset_page": "https://data.gov.hk/en-data/dataset/hk-censtatd-tablechart-650-80001",
                "download_url": "https://www.censtatd.gov.hk/api/get.php?id=650-80001&lang=en&full_series=1",
                "sha256": sha256(VISITOR_JSON),
            },
            {
                "file": OCCUPANCY_CSV.name,
                "dataset": "Hotel room occupancy rate",
                "dataset_page": "https://data.gov.hk/en-data/dataset/hk-cstb-cstb_tc-tc-hotel-room-occupancy-rate",
                "download_url": "https://www.tourism.gov.hk/datagovhk/hotelroomoccupancy/hotel_room_occupancy_rate_monthly_en.csv",
                "sha256": sha256(OCCUPANCY_CSV),
            },
            {
                "file": ROOM_RATE_CSV.name,
                "dataset": "Average achieved hotel room rate in Hong Kong",
                "dataset_page": "https://data.gov.hk/en-data/dataset/hk-cstb-cstb_tc-tc-average-achieved-hotel-room-rate",
                "download_url": "https://www.tourism.gov.hk/datagovhk/hotelroomrate/average_achieved_hotel_room_rate_en.csv",
                "sha256": sha256(ROOM_RATE_CSV),
            },
        ],
        "outputs": {
            monthly_path.name: len(monthly_rows),
            visitor_monthly_path.name: len(visitor_monthly_rows),
            annual_path.name: len(annual_rows),
        },
        "quality_checks": {
            "common_months_2022_2025": 48,
            "monthly_join_key_unique": len({r["YearMonth"] for r in monthly_rows}) == len(monthly_rows),
            "missing_required_values": sum(any(r[k] == "" for k in ["VisitorArrivals", "HotelOccupancyRatePct", "AverageRoomRateHKD"]) for r in monthly_rows),
            "negative_required_values": sum(any(float(r[k]) < 0 for k in ["VisitorArrivals", "HotelOccupancyRatePct", "AverageRoomRateHKD"]) for r in monthly_rows),
            "occupancy_outside_0_100": sum(not 0 <= float(r["HotelOccupancyRatePct"]) <= 100 for r in monthly_rows),
            "official_values_modified": False,
        },
        "caveats": [
            "Visitor market classification changed from country/region of residence to nationality/region on 16 October 2024. Long-term analysis therefore uses Total arrivals rather than regional shares.",
            "The 2022-2025 merged monthly table supports descriptive association, not causal claims.",
            "Annual hotel occupancy and room-rate values are arithmetic means of the 12 published monthly observations.",
        ],
    }
    with (DOCS / "source_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)

    print(json.dumps(manifest["outputs"], indent=2))
    print(json.dumps(manifest["quality_checks"], indent=2))


if __name__ == "__main__":
    main()
