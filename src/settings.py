import os
from pathlib import Path


from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

BASE_DIR = Path(__file__).resolve().parent.parent


class Db(BaseModel):
    """
    Настройки для подключения к базе данных.
    """
    host: str
    port: int
    user: str
    password: str
    name: str
    scheme: str = 'public'
    interval_upload: int

    provider: str = 'postgresql+asyncpg'

    @property
    def url_db(self) -> str:
        return f'{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class ApiV1Prefix(BaseModel):
    prefix: str = "/api/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class TestDb(BaseModel):
    """
    Настройки для подключения к тестовой базе данных.
    """

    test_host: str
    test_port: int
    test_user: str
    test_password: str
    test_name: str
    scheme: str = 'public'

    test_provider: str = 'postgresql+asyncpg'

    @property
    def url_db_test(self) -> str:
        return f'{self.test_provider}://{self.test_user}:{self.test_password}@{self.test_host}:{self.test_port}/{self.test_name}'



class Settings(BaseSettings):
    """
    Настройки модели.
    """
    base_url: str
    api: ApiPrefix = ApiPrefix()

    cors_origins: list[str]
    test: int
    test_db: TestDb
    debug: bool
    port: int
    host: str

    db: Db
    base_api: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
    )


def get_settings():
    return Settings()


def config_logging(level=logging.INFO):
    log_dir = "logs"
    if not os.path.exists(BASE_DIR / log_dir):
        os.makedirs(BASE_DIR / log_dir)
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)7s:%(lineno)-3d %(levelname)-7s - %(message)s",
        handlers=[
            logging.FileHandler(BASE_DIR / "logs/logs.log"),
            logging.StreamHandler()
        ]

    )


settings = get_settings()

