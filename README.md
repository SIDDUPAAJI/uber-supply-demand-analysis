
# Uber Supply-Demand Gap Analysis

This project performs exploratory data analysis (EDA) on Uber ride request data to identify supply-demand gaps, ride completion trends, and operational inefficiencies using Python, SQL, and visual storytelling.

## Project Structure

- `Uber Request Data.csv` - Raw dataset
- `uber_eda_project_cleaned.py` - Cleaned Python analysis script
- `uber_sql_queries.sql` - SQL queries for insights
- `uber_dashboard.xlsx` - Excel-based dashboard (optional)
- `README.md` - Project documentation

## Tools & Technologies Used

- Python: pandas, matplotlib, seaborn
- SQL: SQLite (via `sqlite3`)
- Excel: Pivot tables and visual charts

## Key Analyses Performed

- Total ride requests by time slot
- Status distribution (Completed, Cancelled, No Cars Available)
- Ride volume by pickup point
- Trip completion heatmaps by location and time
- Hourly ride trends
- Cancellation and no-car trends
- Trip completion rates by time slot

## Insights

- The highest supply-demand gap occurs during Late Night and Early Morning.
- Airport pickups have the highest cancellation rate.
- No Cars Available is more common during peak hours.
- Trip Completion Rate is lowest during early morning due to driver unavailability.

## Recommendations

- Incentivize night and early morning driver availability
- Introduce surge or guaranteed pay in low-completion windows
- Real-time distribution of cars using historical trend mapping

## How to Run

1. Clone the repo or download ZIP
2. Ensure Python 3.x is installed with required libraries
3. Run the `.py` script or explore via Jupyter Notebook

```bash
python uber_eda_project_cleaned.py
```

## Author

SIDDESH

## License

For academic or demo use only.
