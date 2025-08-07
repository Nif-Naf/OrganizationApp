import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient

from app.connectors.sql import get_sync_session_factory
from app.main import app
from app.settings import BASE_DIR, get_current_config
from app.test_data import load_test_data


@pytest.fixture(scope="session")
async def client():
    config = get_current_config()
    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
        headers={"x-api-key": config.AUTH_TOKEN},
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def lifespan_for_tests():
    # Make migration.
    alembic_cfg = Config(BASE_DIR / "alembic.ini")
    alembic_cfg.set_main_option(
        "script_location", f"{BASE_DIR}/app/migrations"
    )
    command.upgrade(alembic_cfg, "head")
    # Upload data.
    with get_sync_session_factory() as session:
        load_test_data(session)
