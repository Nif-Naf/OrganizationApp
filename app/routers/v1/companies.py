from logging import getLogger

from fastapi import APIRouter, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.depends.services import get_find_service
from app.schemas.companies import Companies, Company, SearchCompaniesByGeo
from app.services.search_service import SearchService

logger = getLogger("build-system")

company_router = APIRouter(prefix="/companies", tags=["companies"])


responses = {
    HTTP_200_OK: {"description": "Успешный ответ с отсортированными задачами"},
    HTTP_400_BAD_REQUEST: {"description": "Некорректный запрос"},
    HTTP_404_NOT_FOUND: {"description": "Компания не найдена"},
    HTTP_401_UNAUTHORIZED: {"description": "Запрос не авторизован"},
    HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации входных данных"
    },
    HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Критическая ошибка логики проекта"
    },
}


@company_router.get(
    path="/{pk}",
    response_model=Company,
    summary="Получить компанию по индификатору",
    description="Принимает индификатор компании, возвращает компанию",
    responses=responses,
)
async def get_company_by_id(
    pk: int, service: SearchService = Depends(get_find_service)
):
    return await service.find_company_by_id(pk)


@company_router.get(
    path="/search/by/name/{name}",
    response_model=Company,
    summary="Получить компанию по имени",
    description="Принимает имя компании, возвращает компанию",
    responses=responses,
)
async def get_company_by_name(
    name: str, service: SearchService = Depends(get_find_service)
):
    return await service.find_company_by_name(name)


@company_router.get(
    path="/search/by/activity/{activity}",
    response_model=Companies,
    summary="Получить компании c определенным видом деятельности",
    description="Принимает вид деятельности и возвращает все компании",
    responses=responses,
)
async def get_companies_by_activity(
    activity: str, service: SearchService = Depends(get_find_service)
):
    return await service.find_company_by_activity(activity)


@company_router.get(
    path="/search/by/address/{address}",
    response_model=Companies,
    summary="Получить все компании по адресу",
    description="Принимает адрес, возвращает все компании по адресу",
    responses=responses,
)
async def get_companies_by_address(
    address: str, service: SearchService = Depends(get_find_service)
):
    return await service.find_companies_by_address(address)


@company_router.post(
    path="/search/by/geo/",
    response_model=Companies,
    summary="Получить ближайшие компании от координаты в радиусе x км.",
    description="Принимает координаты, возвращает все компании в радиусе x км",
    responses=responses,
)
async def get_companies_by_geo(
    data: SearchCompaniesByGeo,
    service: SearchService = Depends(get_find_service),
):
    return await service.find_companies_by_geo(
        data.latitude, data.longitude, data.radius
    )
