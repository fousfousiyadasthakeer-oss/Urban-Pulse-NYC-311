from sql_query_to_dataframe import *
import matplotlib.pyplot as plt
import pandas as pd
#chart 1
plt.figure(figsize=(12, 6))

plt.barh(df2["complaint_type"], df2["total_requests"])

plt.xlabel("Total Requests")
plt.ylabel("Complaint Type")
plt.title("Top 10 Complaint Categories")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()

#chart 2
plt.figure(figsize=(12, 6))

plt.bar(df3["agency"], df3["total_requests"])

plt.xlabel("Agency")
plt.ylabel("Total Requests")
plt.title("Agency Workload Distribution")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#chart 3
chart3 = df4.copy()

chart3["borough"] = chart3["borough"].fillna("Unknown").astype(str)

chart3["total_requests"] = pd.to_numeric(
    chart3["total_requests"], errors="coerce"
)

chart3 = chart3.dropna(subset=["total_requests"])

plt.figure(figsize=(10, 6))

plt.bar(
    chart3["borough"],
    chart3["total_requests"]
)

plt.xlabel("Borough")
plt.ylabel("Total Requests")
plt.title("Request Volume by Borough")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#chatrt 4

plt.plot(
    df5["request_month"],
    df5["total_requests"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Total Requests")
plt.title("Monthly NYC 311 Request Trend")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()




#chart 5
plt.figure(figsize=(12, 6))

pivot_df = df6.pivot(
    index="created_weekday",
    columns="created_hour",
    values="total_requests"
)

plt.imshow(pivot_df, aspect="auto")

plt.colorbar(label="Total Requests")

plt.xlabel("Hour of Day")
plt.ylabel("Weekday")
plt.title("NYC 311 Requests by Weekday and Hour")

plt.xticks(range(len(pivot_df.columns)), pivot_df.columns)
plt.yticks(range(len(pivot_df.index)), pivot_df.index)

plt.tight_layout()
plt.show()



#chart 6
plt.figure(figsize=(10, 6))

plt.bar(
    df7["status"],
    df7["total_requests"]
)

plt.xlabel("Request Status")
plt.ylabel("Total Requests")
plt.title("NYC 311 Request Status Distribution")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#chart 7
plt.figure(figsize=(10, 6))

metrics = [
    "average_hours",
    "median_hours",
    "minimum_hours",
    "maximum_hours"
]

values = df8[metrics].iloc[0]

plt.bar(metrics, values)

plt.xlabel("Statistics")
plt.ylabel("Resolution Hours")
plt.title("Resolution Time Statistics")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



#chart 8
plt.figure(figsize=(12, 7))

plt.barh(
    df9["complaint_type"],
    df9["median_hours"]
)

plt.xlabel("Median Resolution Time (Hours)")
plt.ylabel("Complaint Type")
plt.title("Median Resolution Time by Complaint Category")

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()



#chart 9
plt.figure(figsize=(12, 6))

plt.bar(
    df10["agency"],
    df10["median_hours"]
)

plt.xlabel("Agency")
plt.ylabel("Median Resolution Time (Hours)")
plt.title("Median Resolution Time by Agency")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



#chart 10
plt.figure(figsize=(12, 6))

plt.scatter(
    range(len(df11)),
    df11["resolution_hours"]
)

plt.xlabel("Outlier Record Index")
plt.ylabel("Resolution Time (Hours)")
plt.title("Resolution Time Outlier Analysis")

plt.tight_layout()
plt.show()

#chart 11
plt.figure(figsize=(10, 6))

metrics = [
    "average_hours",
    "median_hours",
    "standard_deviation"
]

values = df12[metrics].iloc[0]

plt.bar(metrics, values)

plt.xlabel("Statistical Measures")
plt.ylabel("Resolution Hours")
plt.title("Resolution Time Distribution")

plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

#chart 12
plt.figure(figsize=(10, 7))

plt.scatter(
    df13["longitude"],
    df13["latitude"],
    s=df13["total_requests"],
    alpha=0.6
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Geographic Complaint Concentration")

plt.tight_layout()
plt.show()


#chart 13
plt.figure(figsize=(10, 6))

plt.bar(
    df14["borough"],
    df14["closure_rate_percentage"]
)

plt.xlabel("Borough")
plt.ylabel("Closure Rate (%)")
plt.title("Closure Rate by Borough")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#chart 14
plt.figure(figsize=(12, 7))

plt.barh(
    df15["complaint_type"],
    df15["median_resolution_hours"]
)

plt.xlabel("Median Resolution Time (Hours)")
plt.ylabel("Complaint Type")
plt.title("High-Volume Complaints and Long Resolution Time")

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()



#chart 15
plt.figure(figsize=(10, 6))

plt.scatter(
    df15["total_requests"],
    df15["median_resolution_hours"],
    s=60,
    alpha=0.7
)

plt.xlabel("Total Requests")
plt.ylabel("Median Resolution Time (Hours)")
plt.title("Complaint Volume vs Resolution Time")

plt.tight_layout()
plt.show()
