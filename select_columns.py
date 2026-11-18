import pandas as pd
#i have checked the datas
df = pd.read_csv("NYC_311_100K.csv", low_memory=False)
print(df.head())
print(df.tail())
print(df.sample())
print(df.shape)
print(df.describe())
df.info()
print(df.dtypes)
df.describe
print(df.isnull().sum())
print(df.duplicated().sum())

#second step reduce the 44 columns into 25.
selected_columns = [
    "unique_key",
    "created_date",
    "closed_date",
    "due_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "location_type",
    "incident_zip",
    "incident_address",
    "street_name",
    "city",
    "status",
    "resolution_description",
    "resolution_action_updated_date",
    "community_board",
    "borough",
    "latitude",
    "longitude",
    "open_data_channel_type",
    "park_facility_name",
    "park_borough",
    "taxi_company_borough",
    "vehicle_type"
]

selected_df = df[selected_columns]
selected_df["created_date"] = pd.to_datetime(selected_df["created_date"], errors="coerce")
print(selected_df["created_date"].dtype)
selected_df["closed_date"] = pd.to_datetime(selected_df["closed_date"], errors="coerce")
print(selected_df["closed_date"].dtype)
selected_df["due_date"] = pd.to_datetime(selected_df["due_date"], errors="coerce")
print(selected_df["due_date"].dtype)
selected_df["resolution_hours"] = (selected_df["closed_date"] - selected_df["created_date"]).dt.total_seconds() / 3600
selected_df["is_closed"] = selected_df["closed_date"].notna().astype(int)
print(selected_df["is_closed"].value_counts())
selected_df["created_year"] = selected_df["created_date"].dt.year
print(selected_df["created_year"].value_counts())
selected_df["created_month"] = selected_df["created_date"].dt.month
print(selected_df["created_month"].value_counts().sort_index())
selected_df["created_weekday"] = selected_df["created_date"].dt.day_name()
print(selected_df["created_weekday"].value_counts())
print(selected_df["resolution_hours"].describe())
selected_df["created_hour"] = selected_df["created_date"].dt.hour
print(selected_df["created_hour"].value_counts().sort_index())
print(selected_df.dtypes)
selected_df["unique_key"].value_counts()
print(selected_df["unique_key"].value_counts())
selected_df["incident_zip"].value_counts()
print(selected_df["incident_zip"].value_counts())
print(selected_df["unique_key"].duplicated().sum())
print(selected_df.isnull().sum())
print(selected_df.isnull().mean() * 100)
print(selected_df.isnull().mean().sort_values(ascending=False) * 100)
print(selected_df.columns[selected_df.isnull().mean() > 0.5])


core_columns = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "complaint_type",
    "borough",
    "status",
    "latitude",
    "longitude"
]

print(selected_df[core_columns].isnull().sum())

print(selected_df[selected_df["borough"].isnull()].shape)



missing_borough = selected_df[selected_df["borough"].isnull()]

print(missing_borough[["unique_key", "city", "incident_zip", "latitude", "longitude"]])
print(selected_df[["latitude", "longitude"]].isnull().sum())
print(selected_df
      [
    selected_df["latitude"].isnull() != selected_df["longitude"].isnull()
].shape)


print(((selected_df["latitude"] < -90) | (selected_df["latitude"] > 90)).sum())
print(((selected_df["longitude"] < -180) | (selected_df["longitude"] > 180)).sum())
print((selected_df["closed_date"] < selected_df["created_date"]).sum())

selected_df["invalid_date"] = (
    selected_df["closed_date"] < selected_df["created_date"]
)

print(selected_df["invalid_date"].sum())

selected_df["invalid_date"] = (
    selected_df["closed_date"] < selected_df["created_date"]
)

print(selected_df["invalid_date"].sum())
print(selected_df["resolution_hours"].describe())

Q1 = selected_df["resolution_hours"].quantile(0.25)
print(Q1)

Q3 = selected_df["resolution_hours"].quantile(0.75)
print(Q3)

IQR = Q3 - Q1
print(IQR)

lower_limit = Q1 - (1.5 * IQR)
print(lower_limit)

upper_limit = Q3 + (1.5 * IQR)
print(upper_limit)


outliers = selected_df[
    (selected_df["resolution_hours"] < lower_limit) |
    (selected_df["resolution_hours"] > upper_limit)
]

print(outliers.shape[0])

selected_df["resolution_outlier"] = (
    (selected_df["resolution_hours"] < lower_limit) |
    (selected_df["resolution_hours"] > upper_limit)
)

print(selected_df["resolution_outlier"].sum())

valid_resolution = selected_df[
    (selected_df["invalid_date"] == False) &
    (selected_df["resolution_hours"].notna())
]

print(valid_resolution["resolution_hours"].describe())

print(valid_resolution.shape[0])
print(valid_resolution["resolution_hours"].median())

print(valid_resolution["resolution_hours"].mean())

print(valid_resolution["resolution_hours"].std())

print(valid_resolution["resolution_hours"].quantile(0.95))
print("90th percentile:", valid_resolution["resolution_hours"].quantile(0.90))
print("95th percentile:", valid_resolution["resolution_hours"].quantile(0.95))


print(valid_resolution["resolution_hours"].quantile(0.99))

print(valid_resolution["resolution_hours"].skew())

print(valid_resolution["resolution_hours"].kurt())

selected_df.to_csv("NYC_311_Cleaned.csv", index=False)

cleaned_df = pd.read_csv("NYC_311_Cleaned.csv")
print(cleaned_df.shape)


print(cleaned_df.columns.tolist())



cleaned_df = pd.read_csv("NYC_311_Cleaned.csv", low_memory=False)

print("\nCLEANED CSV COLUMN POSITIONS")

for i, col in enumerate(cleaned_df.columns):
    print(i, col)

    print(cleaned_df.loc[
    cleaned_df["unique_key"] == 45349407,
    ["unique_key", "community_board", "borough",
     "resolution_action_updated_date", "resolution_description"]
].to_string(index=False))


print(df.loc[
    df["unique_key"] == 45349407
].T)

print(df.columns.tolist())


print("\nCHECKING ORIGINAL CSV DATA")

row = df[df["unique_key"] == 45349407]

print(row[[
    "unique_key",
    "resolution_description",
    "resolution_action_updated_date",
    "community_board",
    "borough"
]].T)

print("\nCOMPLETE ORIGINAL RECORD")

print(row.T)

with open("row_check.txt", "w", encoding="utf-8") as f:
    for col, val in zip(df.columns, row.iloc[0]):
        f.write(f"{col} = {val}\n")

print("Column mapping saved successfully")


import csv

with open("NYC_311_100K.csv", "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)

    for values in reader:
        if values and values[0] == "45349407":
            print("Header columns:", len(header))
            print("Row columns:", len(values))

            for i, (col, val) in enumerate(zip(header, values)):
                print(i, col, "=", val)

            break

        check_columns = [
    "unique_key",
    "city",
    "resolution_description",
    "resolution_action_updated_date",
    "community_board",
    "council_district",
    "borough",
    "open_data_channel_type",
    "park_facility_name",
    "road_ramp"
]

print(df[check_columns].head(10).to_string(index=False))
