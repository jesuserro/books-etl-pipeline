#!/bin/bash

# Directorio donde se almacenarán los secretos
SECRETS_DIR="$HOME/.secrets/goodreads"

# Crear el directorio si no existe
mkdir -p "$SECRETS_DIR"

# Crear los secretos
echo "airflow" > "$SECRETS_DIR/goodreads_db_user"
echo "airflow123" > "$SECRETS_DIR/goodreads_db_password"
echo "goodreads" > "$SECRETS_DIR/goodreads_db_name"
echo "admin" > "$SECRETS_DIR/grafana_admin_user"
echo "admin" > "$SECRETS_DIR/grafana_admin_password"

# Establecer permisos restrictivos
chmod 600 "$SECRETS_DIR"/*
chmod 700 "$SECRETS_DIR"

# Confirmación
echo "Secretos creados en $SECRETS_DIR con permisos seguros."
