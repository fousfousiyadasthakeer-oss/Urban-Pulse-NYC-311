
import requests
import pandas as pd
import time
import os

api_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

batch_size = 10000
offset = 7070000
total_records = offset

file_name = "NYC_311_Full_Data.csv"

while True:

    params = {
        "$limit": batch_size,
        "$offset": offset,
        "$order": "unique_key"
    }

    print("Downloading from:", offset)

    success = False

    for attempt in range(5):

        try:
            response = requests.get(
                api_url,
                params=params,
                timeout=(30, 300)
            )

            response.raise_for_status()
            data = response.json()

            success = True
            break

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            print("Retrying...", attempt + 1)
            time.sleep(10 * (attempt + 1))

    if not success:
        print("Download paused. Previous data is saved.")
        break

    if not data:
        print("No more records available.")
        break

    df = pd.DataFrame(data)

    df.to_csv(
        file_name,
        mode="a",
        header=False,
        index=False
    )

    total_records += len(data)

    print("Total downloaded:", total_records)

    offset += len(data)

    if len(data) < batch_size:
        break

    time.sleep(1)

print("Download session completed.")
print("Total records:", total_records)
