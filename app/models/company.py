from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.abc import BaseModel
from app.models.many_to_many import company_activities


class Company(BaseModel):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))

    # Relations.
    address: Mapped["Address"] = relationship(back_populates="companies")
    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary=company_activities,
        back_populates="companies",
    )

    def __str__(self):
        return f"Company: {self.name}, id: {self.id}"
