#!/bin/bash
set -e

# Depuración: Imprimir las variables de entorno
echo "AIRFLOW_USERNAME=${AIRFLOW_USERNAME}"
echo "AIRFLOW_PASSWORD=${AIRFLOW_PASSWORD}"

# Verificar si este contenedor es 'airflow-init'
if [[ "$1" == "airflow" && "$2" == "db" && "$3" == "check" ]]; then
  # Verificar si la base de datos ya está inicializada
  if airflow db check; then
    echo "La base de datos ya está inicializada. Ejecutando 'airflow db upgrade' para garantizar la consistencia."
    airflow db upgrade
  else
    echo "Inicializando la base de datos de Airflow..."
    airflow db init
  fi

  # Crear el usuario de Airflow solo si no existe
  if ! airflow users list | grep -q "${AIRFLOW_USERNAME}"; then
    echo "Creando el usuario de Airflow..."
    airflow users create \
      --username "${AIRFLOW_USERNAME}" \
      --firstname "Jesús" \
      --lastname "Admin" \
      --role "Admin" \
      --email "${AIRFLOW_USERNAME}@example.com" \
      --password "${AIRFLOW_PASSWORD}" || echo "⚠️ El usuario ya existe, omitiendo error."
  else
    echo "El usuario ${AIRFLOW_USERNAME} ya existe. Saltando creación de usuario."
  fi
fi

# Ejecutar el comando principal
exec "$@"