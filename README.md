# 🔄 Sales Data Lakehouse Pipeline using Azure & Databricks

This project demonstrates how to build a **dynamic, end-to-end sales data pipeline** using modern data engineering tools like **Azure Data Factory**, **Databricks**, **PySpark**, and **Delta Lake**. It follows the **Medallion Architecture** to organize data into Bronze, Silver, and Gold layers and supports both **initial and incremental data loads**.

---

## 🧾 What’s in the Project?

We’re working with two CSV files:
- `salesdata.csv`: Full initial data
- `incremental.csv`: New/updated records

Both files are stored on GitHub and loaded into **Azure SQL Database** using a **dynamic Azure Data Factory pipeline**.

---

## 🏗️ Step-by-Step Workflow

### 1. Data Ingestion
- Use **ADF dynamic pipeline** to push both CSV files into Azure SQL Database.

### 2. Bronze Layer – Raw Zone
- Load data from Azure SQL to **Azure Data Lake Storage Gen2**.
- Save as **Parquet files** in the Bronze layer.
- Support both full and incremental loads.

### 3. Unity Catalog Setup
- Set up **Unity Catalog** in Databricks for schema and access control.
- Create schemas for Bronze, Silver, and Gold zones.

### 4. Silver Layer – Cleaned Zone
- Use **Databricks notebooks** to process incremental Bronze data.
- Clean and prepare the data for analytics.
- Store cleaned data as Parquet in the Silver layer.

### 5. Gold Layer – Curated Zone
- Create **fact and dimension tables** using PySpark.
- Use **MERGE statements** to handle Slowly Changing Dimensions (SCD).
- Store output as **Delta Tables** in the Gold layer.

### 6. Job Orchestration
- Build a **Databricks job** that runs all notebooks in order.
- Automate the entire ETL process with a single trigger.

---

## 📊 Final Output

You get a structured and optimized **Sales Analytics Model**, built on:
- Delta Lakehouse
- Medallion architecture
- Scalable ETL design

This model can be connected to Power BI or Databricks dashboards for business reporting and analytics.

---

## 🔍 Why This Project Matters

- Covers real-world challenges like **incremental loading** and **SCD handling**
- Uses **best practices in data lakehouse architecture**
- Demonstrates **governance** with Unity Catalog
- Ideal for showcasing in **data engineering interviews or portfolios**

---

## 🧱 Tools & Technologies

- **Azure Data Factory** (Dynamic Pipelines)
- **Azure SQL Database**
- **Azure Data Lake Storage Gen2**
- **Databricks & PySpark**
- **Unity Catalog**
- **Parquet & Delta Lake**

---


