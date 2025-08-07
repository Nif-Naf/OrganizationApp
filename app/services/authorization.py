from fastapi import Header

from app.services.errors import UnauthorizedError
from app.settings import get_current_config


async def authorized_by_api_token(x_api_key: str = Header(...)):
    config = get_current_config()
    if x_api_key != config.AUTH_TOKEN:
        raise UnauthorizedError
    return x_api_key
