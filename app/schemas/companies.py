from pydantic import BaseModel, Field


class Company(BaseModel):
    id: int
    name: str
    address: str
    phone_numbers: list[str]
    latitude: float
    longitude: float
    activities: list[str]


class Companies(BaseModel):
    companies: list[Company]


class SearchCompaniesByGeo(BaseModel):
    latitude: float = Field(ge=-90, le=90, description="Широта от -90 до 90")
    longitude: float = Field(
        ge=-180,
        le=180,
        description="Долгота от -180 до 180",
    )
    radius: int = Field(
        ge=1,
        le=100,
        description="Радиус поиска от 1 до 100 км",
    )
