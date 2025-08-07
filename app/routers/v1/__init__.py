from fastapi import APIRouter

from .companies import company_router

v1_router = APIRouter(
    prefix="/v1",
)
v1_router.include_router(company_router)
