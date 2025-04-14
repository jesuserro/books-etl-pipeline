import sys
import os
import pandas as pd
import logging
from dotenv import load_dotenv

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from airflow.providers.mysql.hooks.mysql import MySqlHook

# Cargar variables de entorno desde el .env
load_dotenv()

log = logging.getLogger(__name__)

def insert_authors_from_rows():
    log.info("📥 Cargando datos desde CSV intermedio...")

    # Directorio de archivos intermedios configurable por .env
    intermediate_dir = os.getenv("TMP_DIR", "/tmp")
    file_path = os.path.join(intermediate_dir, "authors_validated.csv")

    if not os.path.exists(file_path):
        log.error(f"❌ El archivo {file_path} no existe.")
        raise FileNotFoundError(f"No se encontró el archivo de datos validados: {file_path}")

    df = pd.read_csv(file_path)

    rows = df.values.tolist()
    rows = [[None if pd.isna(value) else value for value in row] for row in rows]

    if not rows:
        log.warning("⚠️ No hay filas para insertar.")
        return

    log.info(f"🔗 Insertando datos en la tabla 'authors' usando la conexión 'goodreads_localhost'...")

    hook = MySqlHook(mysql_conn_id='goodreads_localhost')

    try:
        hook.insert_rows(table='authors', rows=rows, replace=True, commit_every=1000)
        log.info(f"✅ Insertados {len(rows)} registros en la tabla 'authors'.")
    except Exception as e:
        log.exception("❌ Error al insertar los datos en MySQL:")
        raise
