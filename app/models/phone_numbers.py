from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.abc import BaseModel


class PhoneNumber(BaseModel):
    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    # Relations.
    company: Mapped["Company"] = relationship(back_populates="phone_numbers")
