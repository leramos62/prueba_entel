from __future__ import annotations
 
import datetime
 
from airflow.models.dag import DAG
from airflow.models.param import Param
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
 
# --- Definir las variables de configuración ---
PROJECT_ID = "concept-test-463118"
BIGQUERY_DATASET = "concept_test_ingest"
GCS_BACKUP_BUCKET = "bkt-concept-test"
 
with DAG(
    dag_id="bigquery_restaurar_tabla_por_nombre_archivo_v3", # 
    start_date=datetime.datetime(2023, 10, 27),
    schedule=None,
    catchup=False,
    tags=["gcp", "bigquery", "restore", "on-demand", "robust"],
    params={
        "tabla_a_crear": Param(
            type="string", 
            title="Nombre para la nueva tabla",
            description="El nombre de la tabla a restaurar. No importa si lo escribes en mayúsculas o minúsculas."
        ),
        "fecha_backup": Param(
            type="string", 
            title="Fecha del Backup (YYYY-MM-DD)",
            description="(ej: '2023-10-29')."
        ),
    },
    doc_md="""
    ### DAG  para Restaurar una Tabla
   
    Este DAG crea una tabla en BigQuery a partir de un archivo de backup AVRO. 
    **Automáticamente convierte el nombre de la tabla a minúsculas** para evitar errores 404 por mayúsculas/minúsculas.
    
    **Debe ser ejecutado manualmente.**
    """,
) as dag:

    crear_y_cargar_tabla_desde_backup = GCSToBigQueryOperator(
        task_id="crear_y_cargar_tabla_desde_backup",
        
        bucket=GCS_BACKUP_BUCKET,

        source_objects=[
            "output/respaldo/{{ params.tabla_a_crear | lower }}/{{ params.fecha_backup }}/{{ params.tabla_a_crear | lower }}-*.avro"
        ],
        
        destination_project_dataset_table=f"{PROJECT_ID}.{BIGQUERY_DATASET}.{{{{ params.tabla_a_crear | lower }}}}",
        
        source_format="AVRO",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_EMPTY",
        
        gcp_conn_id="google_cloud_default",
    )