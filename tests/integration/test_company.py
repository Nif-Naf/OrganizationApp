from urllib.parse import quote

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.utils.enum import ChildrenCategories, MainCategories


async def test_get_success_company_by_id(client: AsyncClient):
    response = await client.get(url="/api/v1/companies/1")
    assert response.status_code == 200
    company = response.json()
    assert company["id"] == 1


async def test_get_failed_company_by_id(client: AsyncClient):
    response = await client.get("/api/v1/companies/10")
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.parametrize("name", ("ООО Рога и Копыта", "Рога", "Копыта"))
async def test_get_success_company_by_name(name: str, client: AsyncClient):
    response = await client.get(
        f"/api/v1/companies/search/by/name/{quote(name)}",
    )
    assert response.status_code == HTTP_200_OK
    company = response.json()
    assert "ООО Рога и Копыта" == company["name"]


async def test_get_failed_company_by_name(client: AsyncClient):
    response = await client.get(
        f"/api/v1/companies/search/by/name/{quote('SomeAnotherCompany')}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "address",
    (
        "Невский",
        "проспект",
        "Санкт-Петербург",
        "Невский проспект",
        "г. Москва, ул. Ленина 1",
        "г. Санкт-Петербург, Итальянская улица 7",
    ),
)
async def test_get_success_companies_by_address(
    address: str,
    client: AsyncClient,
):
    response = await client.get(
        f"/api/v1/companies/search/by/address/{quote(address)}"
    )
    assert response.status_code == 200
    companies = response.json()
    assert any(
        address in company["address"] for company in companies["companies"]
    )


@pytest.mark.parametrize(
    ("main_activity", "result"),
    (
        (
            MainCategories.FOOD,
            (
                ChildrenCategories.MILK_ACTIVITY,
                ChildrenCategories.MEAT_ACTIVITY,
            ),
        ),
        (
            MainCategories.VEHICLE,
            (
                ChildrenCategories.WASHING_VEHICLE_ACTIVITY,
                ChildrenCategories.PARTS_VEHICLE_ACTIVITY,
                ChildrenCategories.ACCESSORIES_VEHICLE_ACTIVITY,
            ),
        ),
    ),
)
async def test_get_success_companies_by_activity(
    main_activity: str,
    result: str,
    client: AsyncClient,
):
    response = await client.get(
        f"/api/v1/companies/search/by/activity/{quote(main_activity)}",
    )
    assert response.status_code == 200
    companies = response.json()
    for company in companies["companies"]:
        for activity in company["activities"]:
            assert activity in result


async def test_get_success_companies_by_geo(client: AsyncClient):
    latitude, longitude = 59.934190, 30.332707  # Невский 35
    response = await client.post(
        url="/api/v1/companies/search/by/geo/",
        json={"latitude": latitude, "longitude": longitude, "radius": 1},
    )
    assert response.status_code == 200
    companies = response.json()
    assert len(companies["companies"]) == 3
