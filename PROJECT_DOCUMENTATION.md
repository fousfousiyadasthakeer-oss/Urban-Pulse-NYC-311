# URBAN PULSE
## Citizen Complaint Intelligence & Resolution Analytics

### 1. Project Overview

URBAN PULSE is a data analytics project based on
NYC 311 Service Requests.

The project analyzes citizen complaints to understand
complaint patterns, agency workload, borough-wise
distribution, resolution time and service performance.

The project uses Python for data extraction and
cleaning, PostgreSQL for data storage and SQL
analysis, Pandas for data manipulation, Matplotlib
for visualization and Streamlit for dashboard development.

### 2. Project Objectives

- Collect approximately 100,000 NYC 311 records.
- Clean and prepare the dataset.
- Store and manage data using SQL.
- Perform 15 analytical investigations.
- Identify complaint trends and patterns.
- Analyze resolution time and outliers.
- Develop an interactive Streamlit dashboard.
- Present findings through KPIs and visualizations.


### 3. Dataset Description

**Dataset Name:** NYC 311 Service Requests from 2020 to Present

**Data Source:** NYC Open Data

**Dataset Link:**
https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present

**Database:** PostgreSQL

**Main Table:** service_requests_stage

**Dataset Size:**
- Total records: 100,000
- Selected columns: 33

### 4. Important Dataset Fields

The dataset contains information about citizen service
requests, including:

- unique_key – Unique request identifier.
- created_date – Date and time the request was created.
- closed_date – Date and time the request was closed.
- agency – Agency responsible for the request.
- complaint_type – Type of complaint.
- borough – Borough associated with the request.
- status – Current recorded request status.
- latitude – Geographic latitude.
- longitude – Geographic longitude.

### 5. Derived Fields

- resolution_hours – Recorded time between creation and closure.
- is_closed – Indicator of recorded closure.
- created weekday and hour – Used for temporal analysis.

## 6. Data Dictionary



| No. | Column name | PostgreSQL data type | Description |
| 1 | `unique_key` | bigint | Unique identifier for each request |
| 2 | `created_date` | timestamp without time zone | Request creation date and time |
| 3 | `closed_date` | timestamp without time zone | Request closure date and time |
| 4 | `due_date` | timestamp without time zone | Recorded due date |
| 5 | `agency` | character varying | Agency code |
| 6 | `agency_name` | character varying | Agency name |
| 7 | `complaint_type` | character varying | Complaint category |
| 8 | `descriptor` | text | Additional complaint description |
| 9 | `location_type` | character varying | Type of reported location |
| 10 | `incident_zip` | text | Incident ZIP code |
| 11 | `incident_address` | text | Incident address |
| 12 | `street_name` | text | Incident street name |
| 13 | `city` | character varying | Recorded city |
| 14 | `status` | character varying | Request status |
| 15 | `resolution_description` | text | Resolution description |
| 16 | `resolution_action_updated_date` | text | Resolution action update date |
| 17 | `community_board` | character varying | Community board information |
| 18 | `borough` | character varying | Borough of the request |
| 19 | `latitude` | double precision | Geographic latitude |
| 20 | `longitude` | double precision | Geographic longitude |
| 21 | `open_data_channel_type` | character varying | Request submission channel |
| 22 | `park_facility_name` | character varying | Park or facility name |
| 23 | `park_borough` | character varying | Borough of the park |
| 24 | `taxi_company_borough` | character varying | Taxi company borough information |
| 25 | `vehicle_type` | character varying | Vehicle type, if applicable |
| 26 | `resolution_hours` | double precision | Calculated resolution time in hours |
| 27 | `is_closed` | integer | Closure indicator: 1 = closed, 0 = not closed |
| 28 | `created_year` | integer | Year the request was created |
| 29 | `created_month` | integer | Month the request was created |
| 30 | `created_weekday` | character varying | Weekday the request was created |
| 31 | `created_hour` | integer | Hour the request was created |
| 32 | `invalid_date` | boolean | Flag for a date-quality issue |
| 33 | `resolution_outlier` | boolean | Flag for a potential resolution-time outlier |



## 7. Data Cleaning and Preprocessing

The NYC 311 dataset was prepared for analysis using Python and Pandas.

The following preprocessing activities were included:

1. **Column Selection:** Selected 33 relevant columns from the original dataset for analysis.
2. **Date Handling:** Used the request creation date and closure date for time-based analysis.
3. **Resolution Time Calculation:** Created the `resolution_hours` field to calculate the time between request creation and closure.
4. **Closure Indicator:** Created the `is_closed` field to identify recorded closed and non-closed requests.
5. **Temporal Features:** Created `created_year`, `created_month`, `created_weekday`, and `created_hour` for trend analysis.
6. **Date Quality Check:** Created the `invalid_date` flag to identify potential date-related data quality issues.
7. **Outlier Identification:** Created the `resolution_outlier` flag to identify potential unusual resolution durations for further investigation.
8. **Database Preparation:** Prepared the processed dataset for storage in PostgreSQL.

The final prepared dataset contains 100,000 records and 33 columns.

Potential outliers were flagged for investigation rather than automatically treated as incorrect records.


## 8. Statistical Analysis and Outlier Detection

Statistical analysis was performed on the NYC 311 dataset to understand request resolution times and identify unusual values.

### 8.1 Descriptive Statistics

The following statistical measures were calculated for valid, non-negative resolution durations:

- Mean: 824.09 hours
- Median: 22.12 hours
- Standard deviation: 4,614.31 hours
- Valid records: 98,174

The mean is much higher than the median, indicating that some requests have very long recorded resolution durations.

### 8.2 Outlier Detection Using IQR

The Interquartile Range (IQR) method was used to identify potential outliers.

- Q1: 2.65 hours
- Q3: 87.55 hours
- IQR: 84.90 hours
- Upper outlier limit: 214.89 hours

Values above the upper limit were flagged for further investigation.

### 8.3 Skewness Analysis

The calculated skewness of resolution duration was 7.3515, indicating a strongly right-skewed distribution.

This means that most requests have shorter recorded resolution durations, while a smaller number have much longer durations.

### 8.4 Visualization

Histograms, boxplots, and other charts were created using Python to examine resolution-time distributions, compare values, and investigate potential outliers.

**Note:** Outlier flags are used for investigation. They do not automatically mean that a record is incorrect.


## 9. Database Storage and SQL Analysis

### 9.1 Database Configuration

PostgreSQL was used to store and query the prepared NYC 311 dataset.

- Database name: `urbanpulsenyc_db`
- Table name: `service_requests_stage`
- Total records loaded: 100,000
- Total columns: 33

### 9.2 Data Loading and Validation

The cleaned dataset was loaded into the PostgreSQL staging table.

The following validations were performed:

- Checked the total number of records.
- Verified the table structure and column data types.
- Checked request identifier uniqueness.
- Confirmed that the table contained 100,000 records.

### 9.3 SQL Analysis

SQL queries were used to investigate the NYC 311 service-request dataset.

The analysis included:

- Total request volume.
- Top 10 complaint categories.
- Agency workload distribution.
- Request volume by borough.
- Monthly request trends.
- Request demand by weekday and hour.
- Request status distribution.
- Resolution-time statistics.
- Median resolution time by complaint category and agency.
- Resolution-time outlier investigation.
- Resolution-time skewness.
- Geographic complaint concentration.
- Recorded closure-rate comparison.
- High-volume complaint categories with longer resolution times.

PostgreSQL aggregation, filtering, grouping, sorting, and date functions were used to perform these investigations.

## 10. Streamlit Dashboard

An interactive dashboard was developed using Streamlit to explore NYC 311 service-request data.

### 10.1 Dashboard Features

The dashboard includes:

- Interactive borough filter.
- Complaint type filter.
- Request status filter.
- Date-range filter.
- Filtered dataset preview.
- KPI metrics.
- Data visualizations and analytical charts.
- Key findings and insights.

### 10.2 Five Key Performance Indicators (KPIs)

The dashboard displays five important metrics:

1. **Total Requests:** Number of distinct service requests in the filtered dataset.
2. **Closed Requests:** Number of requests marked as closed.
3. **Open Requests:** Number of requests marked as not closed.
4. **Median Resolution Time:** Median valid resolution duration, measured in hours.
5. **Requests Over 72 Hours:** Percentage of valid resolution durations greater than 72 hours.

### 10.3 Dashboard Technology

- Python
- Streamlit
- Pandas
- PostgreSQL
- Matplotlib and other Python visualization libraries

### 10.4 Dashboard Purpose

The dashboard helps users explore complaint patterns, compare service-request volumes, examine resolution durations, and understand recorded service trends through interactive filters and visualizations.
## 11. Key Findings and Insights

The analysis of 100,000 NYC 311 service requests revealed the following patterns:

1. **Complaint Categories:** HEAT/HOT WATER was the most frequently reported complaint category, with 10,438 requests.
2. **Agency Workload:** NYPD recorded the highest workload, with 32,909 requests.
3. **Borough Distribution:** Unspecified borough records accounted for 50,232 requests. This indicates that borough information was missing or not specified for many records.
4. **Request Status:** 98,156 requests were recorded with Closed status.
5. **Resolution Duration:** The median valid resolution duration was 22.12 hours.
6. **Long Resolution Duration:** 28.22% of valid resolution durations exceeded 72 hours.
7. **Resolution-Time Distribution:** The distribution was strongly right-skewed, indicating that a smaller number of requests had much longer recorded resolution durations.

These findings describe the selected dataset and should not be interpreted as proof of service quality or citizen satisfaction.
## 12. Project Limitations

The project has the following limitations:

1. **Data Completeness:** Some records contain missing values in fields such as borough, location, and dates.
2. **Data Quality:** Incorrect or inconsistent date values may affect resolution-time calculations.
3. **Geographic Accuracy:** Missing latitude and longitude values may limit geographic analysis.
4. **Resolution Time:** Some requests have unusually long resolution durations, which can influence the average.
5. **Dataset Coverage:** The analysis is based on a selected sample of 100,000 records and may not represent all NYC 311 requests.
6. **Interpretation:** Recorded closure does not necessarily indicate citizen satisfaction or the quality of the service provided.

These limitations should be considered when interpreting the analysis and dashboard results.

## 13. Project Deliverables

The following deliverables were prepared as part of the Urban Pulse project:

1. **Data Extraction:** Python script for retrieving NYC 311 service-request data.
2. **Cleaned Dataset:** Prepared dataset containing 100,000 records and 33 columns.
3. **Database:** PostgreSQL database containing the `service_requests_stage` table.
4. **SQL Analysis:** SQL queries covering the 15 core analyst investigations.
5. **Exploratory Data Analysis:** Python analysis and statistical visualizations.
6. **Streamlit Dashboard:** Interactive dashboard with filters, KPI metrics, charts, and key findings.
7. **Project Documentation:** Documentation describing the project workflow, data dictionary, preprocessing, analysis, dashboard, and limitations.


## 14. Conclusion

The Urban Pulse project demonstrates an end-to-end data analytics workflow using NYC 311 service-request data.

Python and Pandas were used for data preparation, cleaning, and exploratory analysis. PostgreSQL was used to store and query the prepared dataset. Statistical techniques were applied to understand request patterns, resolution durations, and potential outliers.

An interactive Streamlit dashboard was developed to present key performance indicators, visualizations, and analytical findings.

This project provided practical experience in API data extraction, data preprocessing, SQL analysis, statistical analysis, data visualization, and dashboard development.

Overall, Urban Pulse transforms raw civic service-request data into meaningful insights that can support better understanding of urban service demand and recorded resolution patterns.