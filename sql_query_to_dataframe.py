
import pandas as pd
import psycopg2
import os



conn = psycopg2.connect(
    host="localhost",
    database="urbanpulsenyc_db",
    user="postgres",
    password = os.getenv("DB_PASSWORD"),
    port="5432"
)


print("PostgreSQL connected successfully")



query1 = """
SELECT COUNT(DISTINCT unique_key) AS total_requests
FROM service_requests_stage;
"""

df1 = pd.read_sql_query(query1, conn)

print(df1)


query2 = """
SELECT
    complaint_type,
    COUNT(*) AS total_requests
FROM service_requests_stage
WHERE complaint_type IS NOT NULL
GROUP BY complaint_type
ORDER BY total_requests DESC
LIMIT 10;
"""

df2 = pd.read_sql_query(query2, conn)

print(df2)

query3 = """
SELECT
    agency,
    agency_name,
    COUNT(*) AS total_requests
FROM service_requests_stage
WHERE agency IS NOT NULL
GROUP BY agency, agency_name
ORDER BY total_requests DESC;
"""

df3 = pd.read_sql_query(query3, conn)

print(df3)

query4 = """
SELECT borough, COUNT(*) AS total_requests
FROM service_requests_stage
GROUP BY borough
ORDER BY total_requests DESC;
"""

df4 = pd.read_sql_query(query4, conn)
print(df4)

query5 = """
SELECT
    DATE_TRUNC('month', created_date) AS request_month,
    COUNT(*) AS total_requests
FROM service_requests_stage
WHERE created_date IS NOT NULL
GROUP BY request_month
ORDER BY request_month;
"""

df5 = pd.read_sql_query(query5, conn)
print(df5)

query6 = """
SELECT
    created_weekday,
    created_hour,
    COUNT(*) AS total_requests
FROM service_requests_stage
WHERE created_weekday IS NOT NULL
AND created_hour IS NOT NULL
GROUP BY created_weekday, created_hour
ORDER BY total_requests DESC;
"""

df6 = pd.read_sql_query(query6, conn)
print(df6)

query7 = """
SELECT status, COUNT(*) AS total_requests
FROM service_requests_stage
GROUP BY status
ORDER BY total_requests DESC;
"""

df7 = pd.read_sql_query(query7, conn)
print(df7)

query8 = """
SELECT COUNT(*) AS valid_records, ROUND(AVG(resolution_hours)::numeric, 2) AS average_hours,
    ROUND(
        (PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY resolution_hours))::numeric, 2
    ) AS median_hours,
    MIN(resolution_hours) AS minimum_hours,
    MAX(resolution_hours) AS maximum_hours,
    ROUND(STDDEV(resolution_hours)::numeric, 2) AS standard_deviation
FROM service_requests_stage
WHERE resolution_hours IS NOT NULL
AND resolution_hours >= 0;
"""

df8 = pd.read_sql_query(query8, conn)
print(df8)

query9 = """
SELECT
    complaint_type,
    COUNT(*) AS total_requests,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP
    (ORDER BY resolution_hours)::numeric, 2) AS median_hours
FROM service_requests_stage
WHERE complaint_type IS NOT NULL
AND resolution_hours IS NOT NULL
AND resolution_hours >= 0
GROUP BY complaint_type
ORDER BY median_hours DESC;
"""

df9 = pd.read_sql_query(query9, conn)
print(df9)

query10 = """
SELECT
    agency,
    COUNT(*) AS total_requests,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP
    (ORDER BY resolution_hours)::numeric, 2) AS median_hours
FROM service_requests_stage
WHERE agency IS NOT NULL
AND resolution_hours IS NOT NULL
AND resolution_hours >= 0
GROUP BY agency
ORDER BY median_hours DESC;
"""

df10 = pd.read_sql_query(query10, conn)
print(df10)
query11 = """
WITH quartiles AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP
        (ORDER BY resolution_hours) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP
        (ORDER BY resolution_hours) AS q3
    FROM service_requests_stage
    WHERE resolution_hours IS NOT NULL
    AND resolution_hours >= 0
)
SELECT
    s.unique_key,
    s.agency,
    s.complaint_type,
    s.resolution_hours
FROM service_requests_stage s
CROSS JOIN quartiles q
WHERE s.resolution_hours > q.q3 + 1.5 * (q.q3 - q.q1)
ORDER BY s.resolution_hours DESC
LIMIT 50;
"""

df11 = pd.read_sql_query(query11, conn)
print(df11)
query12 = """
SELECT
    COUNT(*) AS valid_records,
    ROUND(AVG(resolution_hours)::numeric, 2) AS average_hours,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP
    (ORDER BY resolution_hours)::numeric, 2) AS median_hours,
    ROUND(STDDEV(resolution_hours)::numeric, 2) AS standard_deviation,
    ROUND(
        (
            AVG(POWER(resolution_hours - avg_hours, 3))
            / NULLIF(POWER(STDDEV(resolution_hours), 3), 0)
        )::numeric, 4
    ) AS skewness
FROM service_requests_stage
CROSS JOIN (
    SELECT AVG(resolution_hours) AS avg_hours
    FROM service_requests_stage
    WHERE resolution_hours IS NOT NULL
    AND resolution_hours >= 0
) a
WHERE resolution_hours IS NOT NULL
AND resolution_hours >= 0;
"""

df12 = pd.read_sql_query(query12, conn)
print(df12)
query13 = """
SELECT
    ROUND(latitude::numeric, 2) AS latitude,
    ROUND(longitude::numeric, 2) AS longitude,
    borough,
    COUNT(*) AS total_requests
FROM service_requests_stage
WHERE latitude IS NOT NULL
AND longitude IS NOT NULL
AND latitude BETWEEN 40.4 AND 41.0
AND longitude BETWEEN -74.3 AND -73.6
GROUP BY
    ROUND(latitude::numeric, 2),
    ROUND(longitude::numeric, 2),
    borough
ORDER BY total_requests DESC
LIMIT 20;
"""

df13 = pd.read_sql_query(query13, conn)
print(df13)


query14 = """
SELECT
    borough,
    COUNT(*) AS total_requests,
    SUM(is_closed) AS closed_requests,
    COUNT(*) - SUM(is_closed) AS open_requests,
    ROUND(
        SUM(is_closed)::numeric /
        NULLIF(COUNT(*), 0) * 100, 2
    ) AS closure_rate_percentage
FROM service_requests_stage
WHERE borough IS NOT NULL
GROUP BY borough
ORDER BY closure_rate_percentage DESC;
"""

df14 = pd.read_sql_query(query14, conn)
print(df14)

query15 = """
SELECT
    complaint_type,
    COUNT(*) AS total_requests,
    COUNT(resolution_hours) FILTER (
        WHERE resolution_hours >= 0
    ) AS valid_duration_records,
    ROUND(
        (
            PERCENTILE_CONT(0.5)
            WITHIN GROUP (ORDER BY resolution_hours)
            FILTER (WHERE resolution_hours >= 0)
        )::numeric, 2
    ) AS median_resolution_hours
FROM service_requests_stage
WHERE complaint_type IS NOT NULL
GROUP BY complaint_type
ORDER BY total_requests DESC, median_resolution_hours DESC
LIMIT 20;
"""

df15 = pd.read_sql_query(query15, conn)
print(df15)



print("Total requests:", len(df1))
print("Top complaints:", len(df2))
print("Agency workload:", len(df3))
print("Borough volume:", len(df4))
print("Monthly trend:", len(df5))
print("Weekday and hour:", len(df6))
print("Status:", len(df7))
print("Resolution statistics:", len(df8))
print("Complaint resolution:", len(df9))
print("Agency resolution:", len(df10))
print("Outliers:", len(df11))
print("Distribution:", len(df12))
print("Geographic concentration:", len(df13))
print("Closure rate:", len(df14))
print("High volume and long duration:", len(df15))

dataframes = [
    df1, df2, df3, df4, df5,
    df6, df7, df8, df9, df10,
    df11, df12, df13, df14, df15
]

for i, df in enumerate(dataframes, start=1):
    print(f"df{i} shape:", df.shape)