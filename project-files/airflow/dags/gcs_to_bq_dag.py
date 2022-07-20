import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'international_economics_data_lake')

CREATE_BQ_TBL_QUERY_COUNTRY_PRODUCT_TRADE = (
    f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.country_product_trade \
            ( \
            location_id INT64, \
            partner_id INT64, \
            product_id INT64, \
            year DATETIME, \
            export_value FLOAT64, \
            import_value FLOAT64, \
            sitc_eci FLOAT64, \
            sitc_coi FLOAT64, \
            location_code STRING, \
            partner_code STRING, \
            sitc_product_code INT64 \
            ) \
    PARTITION BY DATE(year) \
    OPTIONS( \
    partition_expiration_days=10000 \
    ) \
    AS ( \
        SELECT  \
            location_id,  \
            partner_id,  \
            product_id,  \
            CAST(CONCAT(CAST(year AS STRING), '-01-01') AS DATETIME) AS year, \
            export_value,  \
            import_value,  \
            sitc_eci,  \
            sitc_coi,  \
            location_code,  \
            partner_code,  \
            NULL AS sitc_product_code \
        FROM  \
            {BIGQUERY_DATASET}.country_product_trade_external_table \
    );" \
)

MAIN_FOLDER = 'international_economics'
TABLE_RANGE = {'country_product_trade': CREATE_BQ_TBL_QUERY_COUNTRY_PRODUCT_TRADE}
SOURCE_FOLDER = "raw"
INPUT_FILETYPE = "parquet"
DESTINATION_FOLDER = "data_lake"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="gcs_to_bq",
    schedule_interval="@yearly",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    for table, query in TABLE_RANGE.items():
        move_files_gcs_task = GCSToGCSOperator(
            task_id=f'move_{table}_files_task',
            source_bucket=BUCKET,
            source_object=f'{MAIN_FOLDER}/{SOURCE_FOLDER}/country_partner_*.{INPUT_FILETYPE}',
            destination_bucket=BUCKET,
            destination_object=f'{MAIN_FOLDER}/{DESTINATION_FOLDER}/{table}',
            move_object=True
        )

        bigquery_external_table_task = BigQueryCreateExternalTableOperator(
            task_id=f"bq_{table}_external_table_task",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": f"{table}_external_table",
                },
                "externalDataConfiguration": {
                    "autodetect": "True",
                    "sourceFormat": f"{INPUT_FILETYPE.upper()}",
                    "sourceUris": [f"gs://{BUCKET}/international_economics/{DESTINATION_FOLDER}/{table}*"],
                },
            },
        )

        # Create a partitioned table from external table
        bq_create_partitioned_table_job = BigQueryInsertJobOperator(
            task_id=f"bq_create_{table}_partitioned_table_task",
            configuration={
                "query": {
                    "query": query,
                    "useLegacySql": False,
                }
            }
        )

move_files_gcs_task >> bigquery_external_table_task >> bq_create_partitioned_table_job