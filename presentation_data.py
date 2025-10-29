from pyspark.sql.functions import col, round, when, sum as _sum
import os

# Load credentials from environment variables
account_name = os.getenv("STORAGE_NAME")
account_key = os.getenv("ACCOUNT_KEY")

spark.conf.set(
    f"fs.azure.account.key.{account_name}.dfs.core.windows.net",
    account_key
)

# Paths (match your folder structure)
ingested_path = f"abfss://mycontainer@{account_name}.dfs.core.windows.net/ingested/covidclean/"
presentation_country = f"abfss://mycontainer@{account_name}.dfs.core.windows.net/presentation/country_summary/"
presentation_continent = f"abfss://mycontainer@{account_name}.dfs.core.windows.net/presentation/continent_summary/"

# Read ingested data
df = spark.read.parquet(ingested_path)

# Data cleaning and enrichment
df_clean = (
    df.filter(col("country").isNotNull())
      .withColumn("cases", col("cases").cast("long"))
      .withColumn("deaths", col("deaths").cast("long"))
      .withColumn("recovered", col("recovered").cast("long"))
      .withColumn("population", col("population").cast("long"))
)

# Derived KPIs
df_kpi = (
    df_clean.withColumn("death_rate", round((col("deaths") / col("cases")) * 100, 2))
            .withColumn("recovery_rate", round((col("recovered") / col("cases")) * 100, 2))
            .withColumn("case_per_million", round((col("cases") / col("population")) * 1_000_000, 2))
            .withColumn("continent", when(col("continent").isNull(), "Unknown").otherwise(col("continent")))
)

# Aggregation by continent
continent_summary = (
    df_kpi.groupBy("continent")
    .agg(
        _sum("cases").alias("total_cases"),
        _sum("deaths").alias("total_deaths"),
        _sum("recovered").alias("total_recovered"),
        round((_sum("deaths") / _sum("cases")) * 100, 2).alias("avg_death_rate"),
        round((_sum("recovered") / _sum("cases")) * 100, 2).alias("avg_recovery_rate")
    )
)

# Write both outputs
df_kpi.write.mode("overwrite").parquet(presentation_country)
continent_summary.write.mode("overwrite").parquet(presentation_continent)

# Display the data
display(df_kpi)
display(continent_summary)