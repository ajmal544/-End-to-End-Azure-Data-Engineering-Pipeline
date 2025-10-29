# -End-to-End-Azure-Data-Engineering-Pipeline
🦠 COVID-19 Azure Data Engineering Pipeline
🚀 End-to-End Data Engineering Project using Azure Databricks, ADLS, ADF, and Power BI

This project demonstrates a fully automated data pipeline built on Microsoft Azure. It extracts global COVID-19 data from a public API, processes it using Databricks and PySpark, stores the data in Azure Data Lake Storage (ADLS), and visualizes insights using Power BI.

🧩 Architecture Overview

Workflow:

Source: COVID-19 data from disease.sh API

Ingest: Databricks notebook extracts raw JSON and stores it in ADLS Raw Layer

Transform: PySpark cleans and aggregates data into the Presentation Layer

Analyze: Power BI connects to the Presentation Layer for reporting

Automation: Databricks Job / ADF pipeline schedules daily ETL runs

📥 Data Flow
1. Ingestion Layer (Raw Data)

Fetch data from the API:
https://disease.sh/v3/covid-19/countries

Save as JSON in the raw/ folder inside the ADLS container.

2. Transformation Layer (Cleaned Data)

Read raw data from ADLS

Clean and transform it using PySpark (select important fields, calculate metrics)

Store the cleaned data in the presentation/ folder.

3. Visualization Layer

Connect Power BI to the presentation layer (via Databricks or ADLS)

Create dashboards showing:

Total Cases, Deaths, Recoveries

Death Rate vs Recovery Rate

Cases by Continent & Country

KPI Cards and Trend Charts

📊 Power BI Dashboard

The Power BI report includes:

KPI Cards: Total Cases, Deaths, Recoveries

Line Chart: Death Rate vs Recovery Rate per Continent

Map Visualization: Cases by Country

Table View: Detailed Country Stats

Filters: Continent, Country

📸 Sample Dashboard
"C:\Users\ajmal\Downloads\POWER BI graph.jpeg (5).pbix"
