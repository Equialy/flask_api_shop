import threading
import logging
from typing import Optional
from datetime import datetime

from src.domain.products.use_cases.api_data_loader import ApiDataLoaderService

logger = logging.getLogger(__name__)


class BackgroundDataLoader:
    def __init__(self, api_loader: ApiDataLoaderService, interval_minutes: int):
        self.api_loader = api_loader
        self.interval_minutes = interval_minutes
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.is_running = False
        self.last_run: Optional[datetime] = None
        self.last_error: Optional[str] = None

    def start(self):
        """Запускается фоновая загрузка данных"""
        if self.is_running:
            logger.warning("Фоновая загрузка уже запущена")
            return
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.is_running = True
        logger.info(f"Фоновая загрузка запущена с интервалом {self.interval_minutes} минут")

    def _run_loop(self):
        """Основной цикл фоновой загрузки"""
        while not self.stop_event.is_set():
            try:
                logger.info("Начало фоновой зыгрузки данных из API")
                start_time = datetime.now()
                result = self.api_loader.load_all_data()
                self.last_run = datetime.now()
                self.last_error = None
                duration = (self.last_run - start_time).total_seconds()
                logger.info(f"Фоновая загрузка завершена за {duration:.2f} секунд. "
                            f"Результат: {result}")

            except Exception as e:
                self.last_error = str(e)
                logger.error(f"Ошибка при фоновой загрузке данных: {e}")

            if not self.stop_event.wait(self.interval_minutes * 60):
                continue
