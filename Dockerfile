FROM apache/airflow:2.8.1-python3.10

USER airflow
RUN pip install --no-cache-dir pymysql

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]