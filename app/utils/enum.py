from enum import StrEnum


class MainCategories(StrEnum):
    FOOD = "Еда"
    VEHICLE = "Автомобили"


class ChildrenCategories(StrEnum):
    # MainCategories.FOOD
    MEAT_ACTIVITY = "Мясная продукция"
    MILK_ACTIVITY = "Молочная продукция"

    # MainCategories.VEHICLE
    WASHING_VEHICLE_ACTIVITY = "Мойка"
    PARTS_VEHICLE_ACTIVITY = "Запчасти"
    ACCESSORIES_VEHICLE_ACTIVITY = "Аксессуары"
