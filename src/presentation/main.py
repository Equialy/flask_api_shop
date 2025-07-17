import logging
from flask import Flask

from src.presentation.views import index_app
from src.presentation.api.api_v1 import product_api
from src.presentation.dependencies.product_di.product import get_background_loader_service
from src.infrastructure.database.init_db import init_database, check_database_connection
from src.settings import config_logging, settings


def create_app():
    """Создание Flask приложения"""
    config_logging()
    try:
        if check_database_connection():
            init_database()
            logging.info("База данных запущена")
        else:
            logging.error("Не удалось подключиться к базе данных")
    except Exception as e:
        logging.error(f"Ошибка при запуске базы данных: {e}")
    
    app = Flask(__name__)
    
    app.register_blueprint(index_app)
    app.register_blueprint(product_api)
    try:
        background_loader = get_background_loader_service()
        background_loader.start()
    except Exception as e:
        logging.error(f"Ошибка при запуске фоновой загрузки: {e}")
    return app


def main():
    app = create_app()
    port = settings.port
    debug = settings.debug
    app.run(host=settings.host, port=port, debug=debug)


if __name__ == "__main__":
    main()