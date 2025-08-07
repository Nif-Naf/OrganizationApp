from logging import getLogger

from sqlalchemy import ScalarResult, Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.constants import EARTH_RADIUS
from app.models import Activity, company_activities
from app.models.address import Address
from app.models.company import Company
from app.schemas.companies import Companies as CompaniesSchema
from app.schemas.companies import Company as CompanySchema
from app.services.errors import CompanyNotFoundError, UnexpectedError

logger = getLogger("build-system")


class SearchService:

    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def __execute(self, stmt: Select) -> ScalarResult:
        async with self.session_factory as session:
            try:
                result = await session.execute(stmt)
            except Exception as e:
                logger.exception(e)
                await session.rollback()
                raise UnexpectedError
            else:
                await session.commit()
                return result.scalars()

    async def find_company_by_id(self, pk: int) -> CompanySchema:
        logger.info(f"Attempt find company by id: {pk}")
        stmt = (
            select(Company)
            .filter_by(id=pk)
            .options(
                selectinload(Company.address),
                selectinload(Company.phone_numbers),
                selectinload(Company.activities),
            )
        )
        scalar_result = await self.__execute(stmt)
        company = scalar_result.first()
        if not company:
            raise CompanyNotFoundError
        logger.info(f"Search result: {company}")
        return CompanySchema(
            id=company.id,
            name=company.name,
            address=company.address.address,
            phone_numbers=[i.number for i in company.phone_numbers],
            latitude=company.address.latitude,
            longitude=company.address.longitude,
            activities=[i.name for i in company.activities],
        )

    async def find_company_by_name(self, name: str) -> CompanySchema:
        logger.info(f"Attempt find company by name: {name}")
        stmt = (
            select(Company)
            .where(
                or_(
                    Company.name == name,
                    Company.name.ilike(f"%{name}%"),
                )
            )
            .options(
                selectinload(Company.address),
                selectinload(Company.phone_numbers),
                selectinload(Company.activities),
            )
        )
        scalar_result = await self.__execute(stmt)
        company = scalar_result.first()
        logger.info(f"Search result: {company}")
        if not company:
            raise CompanyNotFoundError
        return CompanySchema(
            id=company.id,
            name=company.name,
            address=company.address.address,
            phone_numbers=[i.number for i in company.phone_numbers],
            latitude=company.address.latitude,
            longitude=company.address.longitude,
            activities=[i.name for i in company.activities],
        )

    async def find_company_by_activity(self, activity: str) -> CompaniesSchema:
        logger.info(f"Attempt find company by activity: {activity}")
        first_stmt = select(Activity).where(Activity.name == activity)
        scalar_first_result = await self.__execute(first_stmt)
        root_activity = scalar_first_result.first()
        if not root_activity:
            raise CompanyNotFoundError

        all_ids = await self.__collect_activity_ids(root_activity.id, level=3)
        second_stmt = (
            select(Company)
            .join(company_activities)
            .where(company_activities.c.activity_id.in_(all_ids))
            .options(
                selectinload(Company.address),
                selectinload(Company.phone_numbers),
                selectinload(Company.activities),
            )
        )
        scalar_second_result = await self.__execute(second_stmt)
        companies = scalar_second_result.unique().all()
        return CompaniesSchema(
            companies=[
                CompanySchema(
                    id=i.id,
                    name=i.name,
                    address=i.address.address,
                    phone_numbers=[i.number for i in i.phone_numbers],
                    latitude=i.address.latitude,
                    longitude=i.address.longitude,
                    activities=[i.name for i in i.activities],
                )
                for i in companies
            ],
        )

    async def __collect_activity_ids(
        self,
        root_id: int,
        level: int = 3,
    ) -> set[int]:
        to_check = [root_id]
        all_ids = set(to_check)
        current_level = 0

        while to_check and current_level < level:
            stmt = select(Activity.id).where(Activity.parent_id.in_(to_check))
            result = await self.__execute(stmt)
            children = result.all()
            to_check = children
            all_ids.update(children)
            current_level += 1
        return all_ids

    async def find_companies_by_address(self, address: str) -> CompaniesSchema:
        logger.info(f"Attempt find companies by address: {address}")
        stmt = (
            select(Company)
            .join(Address)
            .where(
                or_(
                    Address.address == address,
                    Address.address.ilike(f"%{address}%"),
                )
            )
            .options(
                selectinload(Company.address),
                selectinload(Company.phone_numbers),
                selectinload(Company.activities),
            )
        )
        scalar_result = await self.__execute(stmt)
        companies = scalar_result.all()
        logger.info(f"Search result: {companies}")
        if not companies:
            raise CompanyNotFoundError
        return CompaniesSchema(
            companies=[
                CompanySchema(
                    id=i.id,
                    name=i.name,
                    address=i.address.address,
                    phone_numbers=[i.number for i in i.phone_numbers],
                    latitude=i.address.latitude,
                    longitude=i.address.longitude,
                    activities=[i.name for i in i.activities],
                )
                for i in companies
            ],
        )

    async def find_companies_by_geo(
        self,
        lat: float,
        long: float,
        radius_km: int,
    ) -> CompaniesSchema:

        stmt = (
            select(Company)
            .join(Address)
            .where(
                EARTH_RADIUS
                * func.acos(
                    func.cos(func.radians(lat))
                    * func.cos(func.radians(Address.latitude))
                    * func.cos(
                        func.radians(Address.longitude) - func.radians(long)
                    )
                    + func.sin(func.radians(lat))
                    * func.sin(func.radians(Address.latitude))
                )
                <= radius_km
            )
            .options(
                selectinload(Company.address),
                selectinload(Company.phone_numbers),
                selectinload(Company.activities),
            )
        )
        scalar_result = await self.__execute(stmt)
        companies = scalar_result.all()
        logger.info(f"Search result: {companies}")
        if not companies:
            raise CompanyNotFoundError
        return CompaniesSchema(
            companies=[
                CompanySchema(
                    id=i.id,
                    name=i.name,
                    address=i.address.address,
                    phone_numbers=[i.number for i in i.phone_numbers],
                    latitude=i.address.latitude,
                    longitude=i.address.longitude,
                    activities=[i.name for i in i.activities],
                )
                for i in companies
            ],
        )
