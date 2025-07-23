from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime

with DAG(
    dag_id='gcs_to_bq_with_reservation',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ci', 'bq', 'composer']
) as dag:

    load_csv_to_bq = BigQueryInsertJobOperator(
        task_id='load_csv',
        configuration={
            "load": {
                "sourceUris": ["gs://healthpra18/healthcare_dataset.csv"],
                "destinationTable": {
                    "projectId": "consummate-fold-466316-c3",
                    "datasetId": "health",
                    "tableId": "health_table"
                },
                "sourceFormat": "CSV",
                "writeDisposition": "WRITE_TRUNCATE",
                "autodetect": True
            }
        },
        location="US",
        gcp_conn_id="google_cloud_default"
    )

