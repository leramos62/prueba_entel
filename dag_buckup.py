from __future__ import annotations

import datetime

from airflow.models.dag import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator

PROJECT_ID = "concept-test-463118"
BIGQUERY_DATASET = "concept_test_ingest"
GCS_BACKUP_BUCKET = "bkt-concept-test"
GCS_BACKUP_PATH = f"gs://{GCS_BACKUP_BUCKET}/output/respaldo"  
TABLES_TO_BACKUP = [
    f"{PROJECT_ID}.{BIGQUERY_DATASET}.departments",
    f"{PROJECT_ID}.{BIGQUERY_DATASET}.hired_employees",
    f"{PROJECT_ID}.{BIGQUERY_DATASET}.jobs",
]

with DAG(
    dag_id="backup_specific_bigquery_tables",
    start_date=datetime.datetime(2023, 11, 2),
    schedule=None,  
    catchup=False,
    tags=["gcp", "bigquery", "backup"],
    doc_md="""
    ### DAG para respaldar tablas específicas de BigQuery a GCS

    Este DAG exporta las tablas especificadas a GCS en formato AVRO,
    organizadas en carpetas por tabla y fecha.
    """,
) as dag:
    for table_id in TABLES_TO_BACKUP:
        # Extraer el nombre de la tabla para la ruta de destino en GCS
        table_name = table_id.split(".")[-1]  # Extrae "departments", "hired_employees", etc.

        exportar_tabla_a_gcs_avro = BigQueryToGCSOperator(
            task_id=f"exportar_{table_name}_a_gcs_como_avro",
            source_project_dataset_table=table_id,
            destination_cloud_storage_uris=[
                f"{GCS_BACKUP_PATH}/{table_name}/{{{{ ds }}}}/{table_name}-*.avro"
            ],
            export_format="AVRO",
            compression="SNAPPY",
            gcp_conn_id="google_cloud_default",
        )