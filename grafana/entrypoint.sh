#!/bin/bash

# Leer secrets como root
export GOODREADS_DB_NAME=$(cat /run/secrets/goodreads_db_name)
export GOODREADS_DB_USER=$(cat /run/secrets/goodreads_db_user)
export GOODREADS_DB_PASSWORD=$(cat /run/secrets/goodreads_db_password)

# Validación básica
if [[ -z "$GOODREADS_DB_NAME" || -z "$GOODREADS_DB_USER" || -z "$GOODREADS_DB_PASSWORD" ]]; then
  echo "❌ ERROR: Uno o más secrets están vacíos o inaccesibles"
  ls -l /run/secrets
  exit 1
fi

echo "✅ Secrets cargados correctamente, lanzando Grafana como usuario grafana (UID 472)..."

# Ejecutar Grafana como usuario grafana sin tini
exec su -s /bin/sh -c "/run.sh" grafana
