from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.connectors.sql import get_sync_session_factory
from app.settings import setup_logger
from app.test_data import load_test_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    with get_sync_session_factory() as session:
        load_test_data(session)
    yield
