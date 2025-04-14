from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
from plugins.utils.goodreads_helpers import create_schema

SQL_FILE_PATH = "/app/db/structure.sql"

with DAG(
    dag_id='setup_database_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["goodreads", "mysql", "db_setup"],
    description='DAG para crear la estructura de la base de datos de Goodreads',
) as dag:

    start = EmptyOperator(task_id='start')

    create_db = PythonOperator(
        task_id='create_db_structure',
        python_callable=create_schema,
        op_kwargs={'sql_path': SQL_FILE_PATH}  # Use the absolute path
    )

    trigger_authors_pipeline = TriggerDagRunOperator(
        task_id='trigger_authors_pipeline',
        trigger_dag_id='authors_data_pipeline',  # Asegúrate de que coincida con el dag_id del segundo DAG
        wait_for_completion=False  # Espera a que el DAG lanzado termine
    )

    end = EmptyOperator(task_id='end')

    start >> create_db >> trigger_authors_pipeline >> end