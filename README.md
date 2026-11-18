# URBAN PULSE – NYC 311 Citizen Complaint Intelligence & Resolution Analytics

## Project Overview
Urban Pulse is a data analytics project that explores NYC 311 service requests to understand complaint patterns, agency workload, borough distribution, and recorded resolution durations.

## Project Objectives
- Collect and prepare NYC 311 service-request data.
- Clean and transform data using Python.
- Store and analyze data using PostgreSQL.
- Perform SQL analysis and exploratory data analysis.
- Identify trends and potential resolution-time outliers.
- Build an interactive dashboard using Streamlit.

## Dataset
**Source:** NYC Open Data – 311 Service Requests from 2020 to Present.

The prepared dataset contains:
- 100,000 records
- 33 columns

## Technologies Used
- Python
- Pandas
- PostgreSQL
- SQL
- Streamlit
- Matplotlib
- GitHub

## Project Features
- Data extraction and preprocessing
- Data quality checks
- Statistical analysis
- SQL-based investigations
- 15 core analytical investigations
- Interactive dashboard with filters
- Five KPI metrics
- Data visualizations and key findings

## Dashboard KPIs
1. Total Requests
2. Closed Requests
3. Open Requests
4. Median Resolution Time
5. Requests Over 72 Hours

## Project Structure
- `PROJECT_DOCUMENTATION.md` – Project documentation
- `str_app.py` – Streamlit dashboard
- `visualizations.py` – Data visualizations
- `sql_query_to_dataframe.py` – SQL query integration
- `scraping.py` – Data extraction
- `select_columns.py` – Column selection
- `extract_1_lakh.py` – Data extraction script
- `import_cleaned_data.py` – Database loading
- `requirements.txt` – Python dependencies

## How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/fousfousiyadasthakeer-oss/Urban-Pulse-NYC-311.git
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL
Set the `DB_PASSWORD` environment variable on your computer and ensure PostgreSQL is running.

### 4. Run the dashboard
```bash
python -m streamlit run str_app.py
```

## Key Findings
- HEAT/HOT WATER was the most frequently reported complaint category.
- NYPD recorded the highest agency workload.
- Resolution durations showed a strongly right-skewed distribution.
- The median valid resolution duration was 22.12 hours.

## Author
Urban Pulse – NYC 311 Data Analytics Project
