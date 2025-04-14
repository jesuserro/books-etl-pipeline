# ============================
# Load environment variables
# ============================
include .env
export $(shell sed 's/=.*//' .env)

# ============================
# Variables
# ============================
AIRFLOW_CMD := $(VIRTUAL_ENV)/bin/airflow
DAG_ID := setup_database_dag

# ============================
# Docker Management
# ============================

up:
	@echo "🚀 [UP-CONTAINERS] Levantando todos los contenedores de Docker..."
	docker compose up -d
	@echo "✅ Contenedores levantados correctamente."

stop:
	@echo "🛑 [STOP-CONTAINERS] Apagando todos los contenedores de Docker..."
	@if [ -n "$$(docker ps -q)" ]; then \
		docker stop $$(docker ps -q); \
		echo "✅ Contenedores detenidos."; \
	else \
		echo "ℹ️  No hay contenedores en ejecución."; \
	fi

clean:
	@echo "🧹 [CLEAN] Limpiando la caché de construcción de Docker..."
	docker builder prune -af
	@echo "🗑️  [CLEAN] Eliminando imágenes dangling (sin etiquetas)..."
	docker image prune -af
	@echo "🧨 [CLEAN] Borrando contenedores, red y volúmenes de Docker..."
	docker compose down --volumes

docker-restart:
	@echo "🧨 [RESTART-DB] Borrando contenedores, red y volúmenes de Docker..."
	docker compose down --volumes --remove-orphans
	@echo "🚀 [RESTART-DB] Reconstruyendo e iniciando contenedores..."
	docker compose up --build -d

fix-airflow-perms:
	@echo "🔧 [PERMISSIONS] Corrigiendo permisos de Airflow..."
	sudo chown -R jesus:jesus ./airflow
	sudo chown -R 50000:0 ./airflow/logs

# ============================
# Airflow Management
# ============================

run-dag:
	@echo "🚀 [RUN-DAG] Ejecutando el DAG: $(DAG_ID)"
	$(AIRFLOW_CMD) dags trigger $(DAG_ID)

logs:
	@echo "📜 [LOGS] Mostrando logs para el DAG: $(DAG_ID)"
	$(AIRFLOW_CMD) dags list-runs -d $(DAG_ID) --output table
	@echo "ℹ️  Para ver logs de una tarea específica, usa el comando:"
	@echo "$(AIRFLOW_CMD) tasks logs <task_id> <execution_date>"

restart-airflow:
	@echo "🔄 [RESTART] Reiniciando el servidor de Airflow..."
	pkill -f "airflow webserver" || true
	pkill -f "airflow scheduler" || true
	$(AIRFLOW_CMD) webserver -D
	$(AIRFLOW_CMD) scheduler -D

clear-dag:
	@echo "🗑️  [CLEAR-DAG] Limpiando ejecuciones del DAG: $(DAG_ID)"
	$(AIRFLOW_CMD) dags clear $(DAG_ID) --yes

# ============================
# Grafana Management
# ============================

grafana-recreate:
	@echo "🔄 [RECREATE-GRAFANA] Reinstanciando el contenedor de Grafana..."
	docker compose up -d --force-recreate grafana
	@echo "✅ Contenedor de Grafana reinstanciado correctamente."

grafana-restart:
	@echo "🔄 [RESTART-GRAFANA] Reiniciando el contenedor de Grafana..."
	docker restart grafana
	@echo "✅ Contenedor de Grafana reiniciado correctamente."

# ============================
# Help
# ============================

help:
	@echo "📖 [HELP] Comandos disponibles:"
	@echo "  🧹 make clean             - Limpia caché, imágenes dangling y volúmenes de Docker."
	@echo "  🧨 make restart-db        - Reinicia la base de datos y contenedores Docker."
	@echo "  🔧 make fix-airflow-perms - Corrige permisos de los directorios de Airflow."
	@echo "  🚀 make run-dag           - Ejecuta manualmente el DAG configurado."
	@echo "  📜 make logs              - Muestra logs del DAG en tiempo real."
	@echo "  🔄 make restart-airflow   - Reinicia el servidor de Airflow."
	@echo "  🗑️  make clear-dag         - Limpia las ejecuciones del DAG configurado."