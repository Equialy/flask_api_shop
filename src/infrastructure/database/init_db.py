import logging
from sqlalchemy import text
from datetime import datetime

from src.infrastructure.database.engine import engine, Base

logger = logging.getLogger(__name__)


def init_database():
    """Инициализация базы данных - создание таблиц"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы базы данных успешно созданы")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных успешно")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise


def check_database_connection():
    """Проверка подключения к базе данных"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных успешно")
            return True
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return False


def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, "%a, %d %b %Y %H:%M:%S %Z")
    except Exception:
        return None
