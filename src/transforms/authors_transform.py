import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()
TMP_DIR = os.getenv("TMP_DIR", "/tmp")

log = logging.getLogger(__name__)

def order_columns(df):
    """Preparar las columnas del DataFrame."""
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()
    df.rename(columns={'authorid': 'author_id'}, inplace=True)
    df.rename(columns={'gender': 'sex'}, inplace=True)

    columns_order = [
        'author_id', 'name', 'sex', 'born', 'died', 'age', 'original_hometown',
        'country', 'latitude', 'longitude', 'image_url', 'website', 'twitter',
        'workcount', 'influence', 'genre', 'average_rate', 'rating_count',
        'review_count', 'fan_count', 'about'
    ]

    # Añadir columnas faltantes con valores NaN
    for col in columns_order:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[columns_order]
    print("CSV leído y DataFrame preparado.")
    return df

def format_sex(df):
    """Normalizar valores de la columna 'sex'."""
    df['sex'] = df['sex'].str.lower().map({'male': 'M', 'female': 'F'})
    return df

def calculate_age(df):
    """Calcular edad en años con precisión decimal."""
    df['born'] = pd.to_datetime(df['born'], errors='coerce')
    df['died'] = pd.to_datetime(df['died'], errors='coerce')
    df['age'] = (df['died'] - df['born']).dt.total_seconds() / (365.25 * 24 * 60 * 60)
    df['age'] = df['age'].fillna(pd.NA).astype(float).round(4)
    print("Edad calculada.")
    return df

def extract_authors(csv_path: str, **kwargs):
    log.info("✨ Leyendo CSV original de autores...")
    df = pd.read_csv(csv_path)

    os.makedirs(TMP_DIR, exist_ok=True)
    raw_path = os.path.join(TMP_DIR, "authors_raw.csv")
    df.to_csv(raw_path, index=False)

    kwargs['ti'].xcom_push(key='raw_csv_path', value=raw_path)
    log.info(f"📁 Archivo intermedio guardado en {raw_path}")

def transform_authors(**kwargs):
    raw_path = kwargs['ti'].xcom_pull(task_ids='extract_authors', key='raw_csv_path')
    df = pd.read_csv(raw_path)

    log.info("🧹 Aplicando transformaciones...")
    df = order_columns(df)
    df = format_sex(df)
    df = calculate_age(df)

    df['born'] = df['born'].apply(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)
    df['died'] = df['died'].apply(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)

    transformed_path = os.path.join(TMP_DIR, "authors_transformed.csv")
    df.to_csv(transformed_path, index=False)

    kwargs['ti'].xcom_push(key='transformed_csv_path', value=transformed_path)
    log.info(f"📁 Archivo transformado guardado en {transformed_path}")

def validate_authors(**kwargs):
    transformed_path = kwargs['ti'].xcom_pull(task_ids='transform_authors', key='transformed_csv_path')
    df = pd.read_csv(transformed_path)

    log.info("🔍 Validando datos de autores...")
    if df['name'].isnull().any():
        log.warning("⚠️ Hay valores nulos en la columna 'name'.")
    if df['author_id'].isnull().any():
        log.warning("⚠️ Hay valores nulos en la columna 'author_id'.")
    if df['author_id'].duplicated().any():
        log.warning("⚠️ Hay valores duplicados en la columna 'author_id'.")

    validated_path = os.path.join(TMP_DIR, "authors_validated.csv")
    df.to_csv(validated_path, index=False)

    kwargs['ti'].xcom_push(key='validated_csv_path', value=validated_path)
    log.info(f"📁 Archivo validado guardado en {validated_path}")
