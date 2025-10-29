import os

# Fetch credentials from environment variables
account_name = os.environ["STORAGE_NAME"]
account_key = os.environ["ACCOUNT_KEY"]

# Set Spark config for accessing Azure Data Lake Storage Gen2
spark.conf.set(
    f"fs.azure.account.key.{account_name}.dfs.core.windows.net",
    account_key
)

# Define paths
raw_path = f"abfss://mycontainer@{account_name}.dfs.core.windows.net/raw/covid/*.parquet"
ingested_path = f"abfss://mycontainer@{account_name}.dfs.core.windows.net/ingested/covidclean/"

# Country list
countries = [
    'India', 'USA', 'UK', 'Germany', 'France', 'Brazil',
    'Italy', 'Canada', 'Australia', 'Russia', 'Mexico',
    'Spain', 'Japan', 'South Korea', 'South Africa',
    'China', 'Argentina', 'Netherlands', 'Turkey', 'Saudi Arabia',
    'Indonesia'
]

# Read all Parquet files from raw path
df = spark.read.parquet(raw_path)

# Filter, drop complex column, clean data
df_filtered = df.filter(df['country'].isin(countries)).drop("countryInfo")
df_clean = df_filtered.dropDuplicates().na.drop()

# Write to ingested path
df_clean.write.mode("overwrite").parquet(ingested_path)

# Display result
display(df_clean)