from airflow.providers.mysql.hooks.mysql import MySqlHook

def test_authors_row_count():
    # Usamos la conexión definida en Airflow (Conn ID: 'goodreads_localhost')
    hook = MySqlHook(mysql_conn_id='goodreads_localhost')
    
    # Ejecutar la consulta para contar los registros en la tabla 'authors'
    result = hook.get_first("SELECT COUNT(*) FROM authors")
    count = result[0] if result else 0

    # Verificar que el conteo sea el esperado
    assert count == 209517, f"Esperado 209517 autores, pero hay {count}"
