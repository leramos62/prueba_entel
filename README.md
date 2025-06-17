# Apache Airflow DAGs para Google Cloud Platform (GCP)

Este repositorio contiene DAGs  de Apache Airflow diseñados para automatizar tareas relacionadas con Google Cloud Platform (GCP), específicamente BigQuery y Google Cloud Storage (GCS).

## Descripción

Este conjunto de DAGs incluye:

*   **`dag_buckup.py`:**  Realiza backups de tablas específicas de BigQuery a Google Cloud Storage en formato AVRO. Los backups se organizan en carpetas por tabla y fecha.
*   **`restaura_tabla.py`:** Restaura una tabla de BigQuery desde un archivo de backup AVRO almacenado en GCS.  El DAG permite al usuario especificar el nombre de la tabla y la fecha del backup como parámetros.
*   **`ingesta_gcp_csv_v6.py`:**  Ingiere datos desde archivos CSV almacenados en GCS a tablas de BigQuery. Este DAG carga datos en las tablas `jobs`, `hired_employees` y `departments`.

## Flujo de Trabajo

1.  **`ingesta_gcp_csv_v6.py` (Ingesta):**
    *   Carga datos desde archivos CSV en GCS (carpeta `input/`) a las tablas correspondientes en BigQuery:
        *   `jobs.csv` -> `concept-test-463118.concept_test_ingest.jobs`
        *   `hired_employees.csv` -> `concept-test-463118.concept_test_ingest.hired_employees`
        *   `departments.csv` -> `concept-test-463118.concept_test_ingest.departments`
    *   Utiliza el operador `GCSToBigQueryOperator` de Airflow.
    *   Trunca la tabla antes de la carga ( `WRITE_TRUNCATE`).

2.  **`dag_buckup.py` (Backup):**
    *   Exporta las tablas especificadas ( `departments`, `hired_employees`, `jobs`) desde BigQuery.
    *   Guarda los backups como archivos AVRO en el bucket de GCS `bkt-concept-test` dentro de la carpeta `output/respaldo`.
    *   Organiza los backups por nombre de tabla y fecha (formato `YYYY-MM-DD`).

3.  **`restaura_tabla.py` (Restauración):**
    *   Permite la restauración de una tabla BigQuery desde un backup AVRO.
    *   Requiere que el usuario proporcione:
        *   `tabla_a_crear`: El nombre de la tabla que se va a restaurar.
        *   `fecha_backup`: La fecha del backup a utilizar (formato `YYYY-MM-DD`).
    *   El DAG convierte automáticamente el nombre de la tabla a minúsculas para evitar problemas de sensibilidad a mayúsculas.
    *   Crea la tabla si no existe y solo escribe datos si la tabla está vacía.



## Requisitos Previos

*   **Apache Airflow:** Debe tener una instalación funcional de Apache Airflow.
*   **Google Cloud Platform (GCP):**
    *   Cuenta de GCP con los siguientes servicios habilitados:
        *   BigQuery
        *   Google Cloud Storage
    *   Una conexión de Airflow a GCP configurada ( `google_cloud_default`).
    *   El bucket de GCS `bkt-concept-test` debe existir.
    *   El dataset BigQuery `concept_test_ingest` debe existir.
    *   Las tablas en BigQuery mencionadas en la sección de Ingesta ( `jobs`, `hired_employees`, `departments`) no necesitan existir, ya que el DAG de ingesta las creará si no existen debido al parámetro `write_disposition='WRITE_TRUNCATE'`.
*   **Archivos CSV (para el DAG de ingesta):** Los archivos CSV (`jobs.csv`, `hired_employees.csv`, `departments.csv`) deben estar presentes en la carpeta `input/` del bucket `bkt-concept-test` en GCS.
*   **Archivos AVRO (para el DAG de restauración):** Los archivos AVRO deben estar presentes en la estructura de carpetas `output/respaldo/{tabla_a_crear}/{fecha_backup}` en el bucket `bkt-concept-test` en GCS.  Estos archivos se generan con el DAG de backup.

## Configuración

1.  **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/leramos62/prueba_entel
    cd prueba_entel
    ```

2.  **Copiar los DAGs a la Carpeta de DAGs de Airflow:**

    Mueva los archivos `.py` ( `dag_buckup.py`, `restaura_tabla.py`, `ingesta_gcp_csv_v6.py`) a la carpeta de DAGs de su instalación de Airflow (normalmente configurada en `airflow.cfg`).

3.  **Configurar la Conexión de Google Cloud en Airflow:**

    *   Vaya a la interfaz de usuario de Airflow -> Admin -> Connections.
    *   Cree o edite una conexión con el `Conn Id` `google_cloud_default`.
    *   Seleccione `Google Cloud` como `Conn Type`.
    *   Proporcione la información de conexión necesaria (por ejemplo, clave JSON de la cuenta de servicio).

4.  **Verificar las Variables:**

    Asegúrese de que las variables `PROJECT_ID`, `BIGQUERY_DATASET`, `GCS_BACKUP_BUCKET` y `GCS_BACKUP_PATH` en los DAGs coincidan con su configuración de GCP.  Modifique los valores si es necesario.

## Uso

1.  **Activar los DAGs en Airflow:**

    *   Vaya a la interfaz de usuario de Airflow -> DAGs.
    *   Active los DAGs ( `backup_specific_bigquery_tables`, `bigquery_restaurar_tabla_por_nombre_archivo_v3`, `INGESTA_HISTORICA_ONETIME`).

2.  **Ejecutar los DAGs:**

    *   **Backup:** Ejecute el DAG `backup_specific_bigquery_tables` para crear backups de las tablas. Este DAG se ejecuta típicamente de forma programada (aunque en este ejemplo tiene `schedule=None`).
    *   **Restauración:** Ejecute el DAG `bigquery_restaurar_tabla_por_nombre_archivo_v3` manualmente. Se le pedirá que ingrese el nombre de la tabla y la fecha del backup.
    *   **Ingesta:** Ejecute el DAG `INGESTA_HISTORICA_ONETIME` para cargar datos desde CSV a BigQuery.

## Notas

*   El DAG de restauración (`restaura_tabla.py`) es diseñado para ser ejecutado manualmente y solicita parámetros de entrada.
*   El DAG de backup (`dag_buckup.py`) está configurado para exportar las tablas `departments`, `hired_employees` y `jobs`. Puede modificar la lista `TABLES_TO_BACKUP` para incluir otras tablas.
*   El DAG de ingesta (`ingesta_gcp_csv_v6.py`) usa `WRITE_TRUNCATE`, lo que significa que las tablas de BigQuery se truncarán (y los datos existentes se perderán) antes de la carga.

