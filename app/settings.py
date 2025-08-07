import logging
import os
from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Final = Path(__file__).resolve().parent.parent


# Project settings.
class DevConfig(BaseSettings):
    AUTH_TOKEN: str
    DB: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    SYNC_DB_DRIVER: str = "postgresql+psycopg2://"
    ASYNC_DB_DRIVER: str = "postgresql+asyncpg://"
    LOG_LEVEL: int = logging.INFO
    DATABASE_SETTINGS: dict = {
        "echo": False,
        "pool_size": 5,
        "max_overflow": 10,
    }
    SESSION_SETTINGS: dict = {
        "autocommit": False,
        "autoflush": False,
        "expire_on_commit": False,
    }

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    @property
    def database_url(self) -> str:
        return f"{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB}"


class TestConfig(BaseSettings):
    AUTH_TOKEN: str = "qwerty"
    SYNC_DB_DRIVER: str = "sqlite:///"
    ASYNC_DB_DRIVER: str = "sqlite+aiosqlite:///"
    LOG_LEVEL: int = logging.DEBUG
    DATABASE_SETTINGS: dict = {
        "echo": False,
    }
    SESSION_SETTINGS: dict = {
        "autocommit": False,
        "autoflush": False,
        "expire_on_commit": False,
    }

    @property
    def database_url(self) -> str:
        return f"/{BASE_DIR}/tests/integration/test.db"


def get_current_config():
    if os.getenv("ENV") == "test":
        return TestConfig()
    return DevConfig()


# Logger settings.
COLOR_RESET = "\033[0m"
COLOR_LEVELS = {
    "INFO": ("\033[97m", "\033[97m"),  # белый
    "WARNING": ("\033[93m", "\033[93m"),  # жёлтый
    "ERROR": ("\033[91m", "\033[91m"),  # красный
    "CRITICAL": ("\033[91m", "\033[91m"),  # красный
    "DEBUG": ("\033[90m", "\033[90m"),  # серый
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level_color, message_color = COLOR_LEVELS.get(
            record.levelname, ("", "")
        )
        record.levelname = f"{level_color}{record.levelname}{COLOR_RESET}"
        record.msg = f"{message_color}{record.getMessage()}{COLOR_RESET}"
        formatted = super().format(record)
        return formatted


def setup_logger() -> logging.Logger:
    config = get_current_config()
    logger = logging.getLogger(__name__)
    logger.setLevel(config.LOG_LEVEL)
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        fmt="%(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
