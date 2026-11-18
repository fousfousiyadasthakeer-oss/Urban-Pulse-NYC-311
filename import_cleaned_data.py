import pandas as pd
import pg8000

# 1. Read cleaned dataset
df = pd.read_csv("NYC_311_Cleaned.csv")

print("Records to import:", len(df))
print("Selected columns:", len(df.columns))