from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime
import os

# Get environment: dev or prod
ENV = os.environ.get("ENV", "dev")

# Dynamic GCS and BQ settings
if ENV == "dev":
    source_uri = "gs://healthpra18/sample_healthcare_dataset.csv"
    table_id = "health_table_dev"
elif ENV == "prod":
    source_uri = "gs://healthpra18/healthcare_dataset.csv"
    table_id = "health_table"
else:
    raise ValueError("Invalid ENV value. Use 'dev' or 'prod'.")

with DAG(
    dag_id='gcs_to_bq_with_reservation',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ci', 'bq', 'composer', ENV]
) as dag:

    load_csv_to_bq = BigQueryInsertJobOperator(
        task_id='load_csv',
        configuration={
            "load": {
                "sourceUris": [source_uri],
                "destinationTable": {
                    "projectId": "consummate-fold-466316-c3",
                    "datasetId": "health",
                    "tableId": table_id
                },
                "sourceFormat": "CSV",
                "writeDisposition": "WRITE_TRUNCATE",
                "autodetect": True
            }
        },
        location="US",
        gcp_conn_id="google_cloud_default"
    )
