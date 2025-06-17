from airflow.models.dag import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime

# Define the DAG
dag = DAG(
    'INGESTA_HISTORICA_ONETIME',
    description='carga de datos a bigquery desde csv',
    schedule_interval=None,
    start_date=datetime(2023, 7, 1),
    catchup=False
)

# carga csv jobs
load_bigquery_jobs = GCSToBigQueryOperator(
    task_id='load_bigquery_jobs',
    bucket='bkt-concept-test',
    source_objects=['input/jobs.csv'],
    destination_project_dataset_table='concept-test-463118.concept_test_ingest.jobs',
    schema_fields=[
        {'name': 'id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'job', 'type': 'STRING', 'mode': 'NULLABLE'}
    ],
    write_disposition='WRITE_TRUNCATE',
    source_format='CSV',
    dag=dag
)

# carga csv hired_employees
load_bigquery_hired_employees = GCSToBigQueryOperator(
    task_id='load_bigquery_hired_employees',
    bucket='bkt-concept-test',
    source_objects=['input/hired_employees.csv'],
    destination_project_dataset_table='concept-test-463118.concept_test_ingest.hired_employees',
    schema_fields=[
        {'name': 'id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'datetime', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'department_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'job_id', 'type': 'INTEGER', 'mode': 'NULLABLE'}
    ],
    write_disposition='WRITE_TRUNCATE',
    source_format='CSV',
    dag=dag
)

# carga csv departments
load_bigquery_departments = GCSToBigQueryOperator(
    task_id='load_bigquery_departments',
    bucket='bkt-concept-test',
    source_objects=['input/departments.csv'],
    destination_project_dataset_table='concept-test-463118.concept_test_ingest.departments',
    schema_fields=[
        {'name': 'id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'department', 'type': 'STRING', 'mode': 'NULLABLE'}
    ],
    write_disposition='WRITE_TRUNCATE',
    source_format='CSV',
    dag=dag
)

load_bigquery_jobs
load_bigquery_hired_employees
load_bigquery_departments