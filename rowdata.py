import os
import requests
import datetime

today = datetime.date.today().isoformat()
url = "https://disease.sh/v3/covid-19/countries"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    raise Exception(f"API call failed: {response.status_code} - {response.text}")

def normalize_numbers(obj):
    if isinstance(obj, dict):
        return {k: normalize_numbers(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_numbers(i) for i in obj]
    elif isinstance(obj, int):
        return float(obj)
    else:
        return obj

normalized_data = normalize_numbers(data)

# 🔹 Get from environment variable
account_name = os.environ["STORAGE_NAME"]
account_key = os.environ["ACCOUNT_KEY"]

spark.conf.set(
    f"fs.azure.account.key.{account_name}.dfs.core.windows.net",
    account_key
)

df = spark.createDataFrame(normalized_data)

raw_path = (
    f"abfss://mycontainer@{account_name}.dfs.core.windows.net/raw/covid/"
    f"covid_raw_{today}.parquet"
)
df.write.mode("overwrite").parquet(raw_path)

display(df)