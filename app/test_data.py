from sqlalchemy import delete, text
from sqlalchemy.orm import Session

from app.models import (
    Activity,
    Address,
    Company,
    PhoneNumber,
    company_activities,
)
from app.utils.enum import ChildrenCategories, MainCategories


def load_test_data(session: Session) -> None:
    session.execute(delete(PhoneNumber))
    session.execute(delete(company_activities))
    session.execute(delete(Company))
    session.execute(delete(Activity))
    session.execute(delete(Address))

    if session.get_bind().dialect.name != "sqlite":
        session.execute(
            text("ALTER SEQUENCE phone_numbers_id_seq RESTART WITH 1")
        )
        session.execute(text("ALTER SEQUENCE companies_id_seq RESTART WITH 1"))
        session.execute(
            text("ALTER SEQUENCE activities_id_seq RESTART WITH 1")
        )
        session.execute(text("ALTER SEQUENCE addresses_id_seq RESTART WITH 1"))

    address1 = Address(
        address="г. Москва, ул. Ленина 1", latitude=55.7558, longitude=37.6173
    )
    address2 = Address(
        address="г. Новосибирск, ул. Блюхера 32/1",
        latitude=55.0302,
        longitude=82.9204,
    )
    address3 = Address(
        address="г. Санкт-Петербург, Невский проспект 52",
        latitude=59.934530,
        longitude=30.336068,
    )
    address4 = Address(
        address="г. Санкт-Петербург, Невский проспект 35В",
        latitude=59.933371,
        longitude=30.332397,
    )
    address5 = Address(
        address="г. Санкт-Петербург, Итальянская улица 7",
        latitude=59.935183,
        longitude=30.330026,
    )
    session.add_all(
        (
            address1,
            address2,
            address3,
            address4,
            address5,
        )
    )
    session.flush()

    activity_food = Activity(name=MainCategories.FOOD)
    activity_meat = Activity(
        name=ChildrenCategories.MEAT_ACTIVITY, parent=activity_food
    )
    activity_milk = Activity(
        name=ChildrenCategories.MILK_ACTIVITY, parent=activity_food
    )

    activity_vehicle = Activity(name=MainCategories.VEHICLE)
    activity_washing_vehicle = Activity(
        name=ChildrenCategories.WASHING_VEHICLE_ACTIVITY,
        parent=activity_vehicle,
    )
    activity_vehicle_parts = Activity(
        name=ChildrenCategories.PARTS_VEHICLE_ACTIVITY, parent=activity_vehicle
    )
    activity_vehicle_accessories = Activity(
        name=ChildrenCategories.ACCESSORIES_VEHICLE_ACTIVITY,
        parent=activity_vehicle,
    )
    session.add_all(
        (
            activity_food,
            activity_meat,
            activity_milk,
            activity_vehicle,
            activity_vehicle_parts,
            activity_washing_vehicle,
            activity_vehicle_accessories,
        )
    )
    session.flush()

    company1 = Company(
        name="ООО Рога и Копыта",
        address_id=address1.id,
        activities=[activity_meat, activity_milk],
    )
    company2 = Company(
        name="ЗАО Мясокомбинат",
        address_id=address2.id,
        activities=[activity_meat],
    )
    company3 = Company(
        name="Кореана",
        address_id=address3.id,
        activities=[activity_vehicle_accessories, activity_vehicle_parts],
    )
    company4 = Company(
        name="Гидро",
        address_id=address4.id,
        activities=[activity_washing_vehicle],
    )
    company5 = Company(
        name="Автостиль",
        address_id=address5.id,
        activities=[activity_vehicle_accessories],
    )
    session.add_all(
        (
            company1,
            company2,
            company3,
            company4,
            company5,
        )
    )
    session.flush()

    phones = (
        PhoneNumber(number="2-222-222", company_id=company1.id),
        PhoneNumber(number="3-333-333", company_id=company1.id),
        PhoneNumber(number="8-923-666-13-13", company_id=company1.id),
        PhoneNumber(number="8-800-555-35-35", company_id=company2.id),
        PhoneNumber(number="8-800-355-35-55", company_id=company3.id),
        PhoneNumber(number="8-800-222-35-35", company_id=company4.id),
        PhoneNumber(number="8-800-111-35-35", company_id=company5.id),
    )
    session.add_all(phones)
    session.commit()
