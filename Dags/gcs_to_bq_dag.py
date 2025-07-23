from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime
import os

# Get the environment from ENV variable (set in Composer config)
ENV = os.getenv("ENV", "dev")  # default to "dev"

# Set variables based on environment
if ENV == "prod":
    gcs_uri = "gs://healthpra18/healthcare_dataset.csv"
    bq_table = "health_table"
else:
    gcs_uri = "gs://healthpra18/Health_sample.csv"  # only 100 rows
    bq_table = "health_sample"

with DAG(
    dag_id=f'gcs_to_bq_{ENV}',  # makes dag_id unique per environment
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ci', 'bq', 'composer', ENV]
) as dag:

    load_csv_to_bq = BigQueryInsertJobOperator(
        task_id='load_csv',
        configuration={
            "load": {
                "sourceUris": [gcs_uri],
                "destinationTable": {
                    "projectId": "consummate-fold-466316-c3",
                    "datasetId": "health",
                    "tableId": bq_table
                },
                "sourceFormat": "CSV",
                "writeDisposition": "WRITE_TRUNCATE",
                "autodetect": True
            }
        },
        location="US",
        gcp_conn_id="google_cloud_default"
    )
