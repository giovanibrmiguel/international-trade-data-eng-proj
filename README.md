<h1 align="center">Data Engineering ETL pipeline using Airflow, Python, Google Cloud Storage, DBT, Big Query, and Data Studio</h1>

<p align="center">
  <a href="#about">About</a> •
  <a href="#context">Context</a> •
  <a href="#detailed-project-overview">Detailed Project Overview</a> •
  <a href="#airflow-python-orchestration-to-data-lake-on-gcs">Airflow Python Orchestration to Data Lake on GCS</a> •
  <a href="#airflow-orchestration-to-data-warehouse-on-big-query">Airflow Orchestration to Data Warehouse on Big Query</a> •
  <a href="#dbt-for-data-transformation">DBT for Data Transformation</a> •
  <a href="#dbt-pipeline-job-and-documentation">DBT Pipeline Job and Documentation</a> •
  <a href="#data-studio-dashboard">Data Studio Dashboard</a> •
</p>

---

## About

Final project for Data Engineering Zoomcamp / Bootcamp from DataTalksClub and Dphi, regarding building a Data Engineering Project involving an end-to-end ETL (Extract, Transform, Load) batch processing data pipeline.


Pipeline architecture:

<p align="center"><img src=https://user-images.githubusercontent.com/77297705/180217542-cb22a0be-39bc-44ea-ab76-a85a52d31eb1.png></p>

## Context
Harvard University's Growth Lab has provided access to their Atlas of Economic Complexity database, which consists of massive and complete data regarding importations and exportations from multiple countries taking into consideration multiple detailed products, as well as SITC (Standard International Trade Classification) complexity metrics and details. The goal of this project was to build an end-to-end data engineering pipeline to allow proactive data analysis insights and visualizations based on this vast dataset.

With the [dashboard created](https://datastudio.google.com/u/1/reporting/8264b415-b239-4f33-9992-700f1266e001/page/f6JyC) at the end of the project, resulting of our data engineering project, we are able to globallly track countries regarding their main product exportations from 1999 to 2019, as well as identify their trade partners, dig deeper into product detailing, and identify time-series trends.

## Detailed Project Overview

#### Airflow Python Orchestration to Data Lake on GCS
An Airflow batch processing dag using Python operators is used to orchestrate the data ingestion pipeline that process the raw data locally, optimizes it by converting from CSV to PARQUET, and stores it raw at a Data Lake built on Google Cloud Platform.
<p align="center"><img src=https://user-images.githubusercontent.com/77297705/180204014-1a22a729-64c3-4908-bfad-a02df89e654b.png></p>

#### Airflow Orchestration to Data Warehouse on Big Query
Via Airflow dags orchestration, the data is moved from the Data Lake to the Data Warehouse on Big Query, an external table is created (stored at Google Cloud Platform – created based on all PARQUET files stored), and finally a partitioned table is created on the Big Query Data Warehouse. The dags were configured to run on a yearly basis to match the periodicity of the data source ingested.
<p align="center"><img src=https://user-images.githubusercontent.com/77297705/180204141-df31af50-1f1a-4a91-b49b-768d8b092e2f.png></p>

#### DBT for Data Transformation
The analytics engineering steps were made by transforming data using DBT (Data Transform Tool), by building a data transformation pipeline using modularization (software engineering best practices). Initial simple transformations were made on a staging layer (renaming columns, casting data types), small CSV look-up files were ingested directly as dbt "seeds", and the final data transformations following business-rules were implemented on the fact table.

<p align="center"><img src=https://user-images.githubusercontent.com/77297705/180204519-fa49997c-d577-45f6-9eb8-37ebb5a96247.png></p>

#### DBT Pipeline Job and Documentation
A DBT job to implement the data transformations on the Big Query Data Warehouse was created and scheduled on the production environment. Testing and documented was also implemented using DBT Cloud.

<p align="center"><img src=https://user-images.githubusercontent.com/77297705/180204579-56943ca4-a0ac-4aaa-8f5b-e4568f4ba907.png></p>

#### Data Studio Dashboard
The outcome fact table was fed into Data Studio as a source, and a dashboard was built based on it. Find the dashboard [here](https://datastudio.google.com/u/1/reporting/8264b415-b239-4f33-9992-700f1266e001/page/f6JyC)

<p align="center"><img src=https://user-images.githubusercontent.com/77297705/180205757-ab0bc011-0d2d-48cc-afb0-fc46aa158210.gif></p>
