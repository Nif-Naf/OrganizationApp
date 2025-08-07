from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.abc import BaseModel


class Address(BaseModel):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    # Relations.
    companies: Mapped[list["Company"]] = relationship(back_populates="address")
