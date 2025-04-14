from airflow.providers.mysql.hooks.mysql import MySqlHook

def create_schema(sql_path: str):
    # Leer el archivo SQL
    with open(sql_path, 'r') as f:
        sql = f.read()

    # Usar el hook para conectarse a la base de datos
    hook = MySqlHook(mysql_conn_id='goodreads_localhost')
    connection = hook.get_conn()
    cursor = connection.cursor()

    # Ejecutar cada sentencia SQL separada por ';'
    for statement in sql.split(';'):
        if statement.strip():
            cursor.execute(statement)

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    cursor.close()
    connection.close()
