

import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import os



# PAGE CONFIGURATION
st.set_page_config(
    page_title="URBAN PULSE",
    page_icon="🏙️",
    layout="wide"
)

# DATABASE CONNECTION
@st.cache_data
def load_data():
    conn = psycopg2.connect(
        host="localhost",
        database="urbanpulsenyc_db",
        user="postgres",
        password = os.getenv("DB_PASSWORD"),
        port="5432"
    )

    data = pd.read_sql_query(
        "SELECT * FROM service_requests_stage",
        conn
    )

    conn.close()
    return data

df = load_data()

# TITLE
st.title("🏙️ URBAN PULSE")
st.subheader("Citizen Complaint Intelligence & Resolution Analytics")

st.markdown(
    "Analyze NYC 311 service requests, complaint trends, "
    "agency workload and resolution performance."
)

st.divider()

# FILTERS
st.subheader("Filter Service Requests")

col1, col2, col3 = st.columns(3)

with col1:
    boroughs = sorted(df["borough"].dropna().astype(str).unique())
    selected_borough = st.selectbox(
        "Select Borough", ["All"] + boroughs
    )

with col2:
    complaints = sorted(df["complaint_type"].dropna().astype(str).unique())
    selected_complaint = st.selectbox(
        "Select Complaint Type", ["All"] + complaints
    )

with col3:
    statuses = sorted(df["status"].dropna().astype(str).unique())
    selected_status = st.selectbox(
        "Select Status", ["All"] + statuses
    )
    # Date Range Filter

st.subheader("Select Date Range")

df["created_date"] = pd.to_datetime(
    df["created_date"], errors="coerce"
)

min_date = df["created_date"].min().date()
max_date = df["created_date"].max().date()

date_range = st.date_input(
    "Choose Start Date and End Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# APPLY FILTERS
filtered_df = df.copy()
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["created_date"].dt.date >= start_date) &
        (filtered_df["created_date"].dt.date <= end_date)
    ]

if selected_borough != "All":
    filtered_df = filtered_df[
        filtered_df["borough"].astype(str) == selected_borough
    ]

if selected_complaint != "All":
    filtered_df = filtered_df[
        filtered_df["complaint_type"].astype(str) == selected_complaint
    ]

if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["status"].astype(str) == selected_status
    ]

st.write("Total matching records:", len(filtered_df))


st.write("Status values:")
st.write(filtered_df["status"].value_counts())

st.write("is_closed values:")
st.write(filtered_df["is_closed"].value_counts())

st.write("Resolution hours:")
st.write(
    pd.to_numeric(
        filtered_df["resolution_hours"],
        errors="coerce"
    ).describe()
)

st.divider()


# KPI CALCULATIONS

total_requests = filtered_df["unique_key"].nunique()

closed_requests = (
    filtered_df["is_closed"] == 1
).sum()

open_requests = (
    filtered_df["is_closed"] == 0
).sum()

valid_resolution = pd.to_numeric(
    filtered_df["resolution_hours"],
    errors="coerce"
)

valid_resolution = valid_resolution[
    valid_resolution >= 0
].dropna()

median_resolution = (
    valid_resolution.median()
    if not valid_resolution.empty else 0
)

over_72 = (
    (valid_resolution > 72).sum()
    / len(valid_resolution) * 100
    if not valid_resolution.empty else 0
)

# KPI CARDS
st.subheader("Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Requests", f"{total_requests:,}")
c2.metric("Closed Requests", f"{closed_requests:,}")
c3.metric("Open Requests", f"{open_requests:,}")
c4.metric("Median Resolution", f"{median_resolution:.2f} hrs")
c5.metric("Over 72 Hours", f"{over_72:.2f}%")

st.divider()
st.header("📊 NYC 311 Analytics Dashboard")

st.markdown("""
Explore complaint patterns, agency performance,
borough-wise demand and service resolution trends.
""")
# CHART 1 - TOP COMPLAINTS
st.subheader("1. Top 10 Complaint Categories")

top_complaints = filtered_df["complaint_type"].value_counts().head(10)
st.bar_chart(top_complaints)

# CHART 2 - AGENCY WORKLOAD
st.subheader("2. Agency Workload Distribution")

agency_data = filtered_df["agency_name"].value_counts().head(10)
st.bar_chart(agency_data)

# CHART 3 - BOROUGH VOLUME
st.subheader("3. Request Volume by Borough")

borough_data = filtered_df["borough"].value_counts()
st.bar_chart(borough_data)

# CHART 4 - MONTHLY TREND
st.subheader("4. Monthly Request Trend")

monthly = pd.to_datetime(
    filtered_df["created_date"], errors="coerce"
).dt.to_period("M").value_counts().sort_index()

monthly.index = monthly.index.astype(str)
st.line_chart(monthly)

# CHART 5 - WEEKDAY AND HOUR
st.subheader("5. Requests by Weekday and Hour")

weekday_hour = filtered_df.pivot_table(
    index="created_weekday",
    columns="created_hour",
    values="unique_key",
    aggfunc="count",
    fill_value=0
)

st.dataframe(weekday_hour, use_container_width=True)

# CHART 6 - STATUS
st.subheader("6. Request Status Distribution")

st.bar_chart(filtered_df["status"].value_counts())

# CHART 7 - RESOLUTION STATISTICS
st.subheader("7. Resolution Time Statistics")

st.metric("Average Resolution Hours",
          f"{valid_resolution.mean():.2f}" if len(valid_resolution) else "N/A")

# CHART 8 - MEDIAN BY COMPLAINT
st.subheader("8. Median Resolution by Complaint")

complaint_resolution = filtered_df.groupby(
    "complaint_type"
)["resolution_hours"].median().dropna().nlargest(10)

st.bar_chart(complaint_resolution)

# CHART 9 - MEDIAN BY AGENCY
st.subheader("9. Median Resolution by Agency")

agency_resolution = filtered_df.groupby(
    "agency"
)["resolution_hours"].median().dropna().nlargest(10)

st.bar_chart(agency_resolution)

# CHART 10 - OUTLIERS
st.subheader("10. Resolution Time Outliers")

outlier_data = valid_resolution[
    valid_resolution > valid_resolution.quantile(0.75)
    + 1.5 * (
        valid_resolution.quantile(0.75)
        - valid_resolution.quantile(0.25)
    )
]

if not outlier_data.empty:
    fig, ax = plt.subplots()
    ax.boxplot(valid_resolution)
    ax.set_ylabel("Resolution Hours")
    ax.set_title("Resolution Time Outlier Analysis")
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No outlier records in this selection.")

# CHART 11 - DISTRIBUTION
st.subheader("11. Resolution Time Distribution")

if not valid_resolution.empty:
    fig, ax = plt.subplots()
    ax.hist(valid_resolution, bins=30)
    ax.set_xlabel("Resolution Hours")
    ax.set_ylabel("Frequency")
    ax.set_title("Resolution Time Histogram")
    st.pyplot(fig)
    plt.close(fig)

# CHART 12 - GEOGRAPHIC CONCENTRATION
st.subheader("12. Geographic Complaint Concentration")

geo = filtered_df.dropna(subset=["latitude", "longitude"]).copy()

geo["latitude"] = pd.to_numeric(geo["latitude"], errors="coerce")
geo["longitude"] = pd.to_numeric(geo["longitude"], errors="coerce")
geo = geo.dropna(subset=["latitude", "longitude"])

if not geo.empty:
    st.map(geo[["latitude", "longitude"]].rename(
        columns={"latitude": "lat", "longitude": "lon"}
    ))
else:
    st.info("No valid geographic coordinates in this selection.")

# CHART 13 - CLOSURE RATE
st.subheader("13. Closure Rate by Borough")

closure = filtered_df.groupby("borough").agg(
    total=("unique_key", "count"),
    closed=("is_closed", lambda x: x.astype(str).str.lower()
            .isin(["true", "1", "yes"]).sum())
)

closure["closure_rate"] = (
    closure["closed"] / closure["total"] * 100
)

st.bar_chart(closure["closure_rate"])

# CHART 14 - HIGH VOLUME AND LONG RESOLUTION
st.subheader("14. High Volume and Long Resolution Categories")

high_volume = filtered_df.groupby("complaint_type").agg(
    total_requests=("unique_key", "count"),
    median_hours=("resolution_hours", "median")
).dropna()

st.dataframe(
    high_volume.sort_values(
        ["total_requests", "median_hours"],
        ascending=False
    ).head(20),
    use_container_width=True
)

# CHART 15 - VOLUME VS RESOLUTION
st.subheader("15. Complaint Volume vs Resolution Time")

if not high_volume.empty:
    fig, ax = plt.subplots()
    ax.scatter(
        high_volume["total_requests"],
        high_volume["median_hours"]
    )
    ax.set_xlabel("Total Requests")
    ax.set_ylabel("Median Resolution Hours")
    ax.set_title("Complaint Volume vs Resolution Time")
    st.pyplot(fig)
    plt.close(fig)
# KEY FINDINGS AND INSIGHTS

st.divider()
st.header("🔍 Key Findings & Insights")

# Top complaint category
top_complaint = (
    filtered_df["complaint_type"].value_counts()
)

# Top borough
top_borough = filtered_df["borough"].value_counts()

# Top agency
top_agency = filtered_df["agency_name"].value_counts()

col1, col2, col3 = st.columns(3)

with col1:
    if not top_complaint.empty:
        st.metric(
            "Most Reported Complaint",
            top_complaint.index[0],
            f"{top_complaint.iloc[0]:,} requests"
        )

with col2:
    if not top_borough.empty:
        st.metric(
            "Highest Complaint Borough",
            top_borough.index[0],
            f"{top_borough.iloc[0]:,} requests"
        )

with col3:
    if not top_agency.empty:
        st.metric(
            "Highest Workload Agency",
            top_agency.index[0],
            f"{top_agency.iloc[0]:,} requests"
        )

st.write(
    f"Median valid resolution time: "
    f"{median_resolution:.2f} hours."
)

st.write(
    f"Requests taking more than 72 hours: "
    f"{over_72:.2f}% of valid resolution records."
)
# DATA PREVIEW
st.divider()
st.subheader("Service Request Data Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

st.caption(
    f"Showing up to 100 records from {len(filtered_df):,} matching records."
)
