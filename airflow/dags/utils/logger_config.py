import logging
import os
import sys

def get_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Nivel configurable vía variable de entorno
        level = os.getenv("LOG_LEVEL", "DEBUG").upper()  # Cambiar a DEBUG por defecto
        logger.setLevel(getattr(logging, level, logging.DEBUG))

        # Formato del log
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler de consola (Airflow captura este handler)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # [Opcional] Para guardar en archivo rotativo
        # from logging.handlers import RotatingFileHandler
        # file_handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=3)
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        logger.propagate = True  # Permitir que Airflow capture los logs

    return logger