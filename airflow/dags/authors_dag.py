import sys
import os
from dotenv import load_dotenv

# Añadir el directorio raíz del proyecto (donde viven src/ y tests/)
if '/app' not in sys.path:
    sys.path.insert(0, '/app')

# Cargar variables de entorno
load_dotenv()

# Asegurar que el directorio TMP existe (mejor hacerlo tras cargar dotenv)
TMP_DIR = os.getenv("TMP_DIR", "/tmp")
os.makedirs(TMP_DIR, exist_ok=True)

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

from src.transforms.authors_transform import (
    transform_authors,
    extract_authors,
    validate_authors,
)

from plugins.operators.mysql_loader_operator import insert_authors_from_rows

from tests.test_authors_load import test_authors_row_count

# Get the absolute path of the authors.csv file
CSV_FILE_PATH = "/app/data/authors.csv"

with DAG(
    dag_id='authors_data_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["goodreads", "authors", "mysql", "etl"],
    description='Pipeline para cargar CSV de autores en la base de datos de Goodreads',
) as dag:

    start = EmptyOperator(task_id='start')

    extract_authors_task = PythonOperator(
        task_id='extract_authors',
        python_callable=extract_authors,
        op_kwargs={'csv_path': CSV_FILE_PATH},  # Use the absolute path
        provide_context=True,
    )

    transform_authors_task = PythonOperator(
        task_id='transform_authors',
        python_callable=transform_authors,
        provide_context=True,
    )

    validate_authors_task = PythonOperator(
        task_id='validate_authors',
        python_callable=validate_authors,
        provide_context=True,
    )

    load_authors_task = PythonOperator(
        task_id='load_authors',
        python_callable=insert_authors_from_rows,
        provide_context=True,
    )

    test_authors_task = PythonOperator(
        task_id='test_authors_row_count',
        python_callable=test_authors_row_count,
    )

    end = EmptyOperator(task_id='end')

    # Dependencias
    start >> extract_authors_task >> transform_authors_task >> validate_authors_task >> load_authors_task >> test_authors_task >> end
