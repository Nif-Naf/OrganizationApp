from app.connectors.sql import get_async_session_factory
from app.services.search_service import SearchService


def get_find_service() -> SearchService:
    return SearchService(session_factory=get_async_session_factory())
