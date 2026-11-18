
import pandas as pd

# Read only first 1 lakh records
df = pd.read_csv(
    "NYC_311_Full_Data.csv",
    nrows=100000
)

# Save as a new CSV file
df.to_csv(
    "NYC_311_100K.csv",
    index=False
)

print("Extraction completed!")
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print(df.head())
