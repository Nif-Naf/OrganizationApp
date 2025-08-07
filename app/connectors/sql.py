import logging
from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from app.settings import get_current_config

logger = logging.getLogger("build-system")

__all__ = (
    "get_sync_session_factory",
    "get_async_session_factory",
)


class AbstractDatabaseConnector(ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def session_factory(self):
        raise NotImplementedError


class AsyncDatabaseConnector(AbstractDatabaseConnector):
    def __init__(self, **kwargs):
        self.engine = create_async_engine(**kwargs)

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(self.engine)


class SyncDatabaseConnector(AbstractDatabaseConnector):
    def __init__(self, **kwargs):
        self.engine = create_engine(**kwargs)

    @property
    def session_factory(self) -> sessionmaker[Session]:
        return sessionmaker(self.engine)


def get_sync_session_factory() -> Session:
    config = get_current_config()
    connector = SyncDatabaseConnector(
        url=f"{config.SYNC_DB_DRIVER}{config.database_url}",
        **config.DATABASE_SETTINGS,
    )
    return connector.session_factory(**config.SESSION_SETTINGS)


def get_async_session_factory() -> AsyncSession:
    config = get_current_config()
    connector = AsyncDatabaseConnector(
        url=f"{config.ASYNC_DB_DRIVER}{config.database_url}",
        **config.DATABASE_SETTINGS,
    )
    return connector.session_factory(**config.SESSION_SETTINGS)
