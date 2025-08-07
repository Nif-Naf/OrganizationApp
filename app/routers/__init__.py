from fastapi import APIRouter, Depends

from .v1 import v1_router
from app.services.authorization import authorized_by_api_token

api_router = APIRouter(
    prefix="/api",
    dependencies=[
        Depends(authorized_by_api_token),
    ],
)
api_router.include_router(v1_router)
