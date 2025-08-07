from typing import Optional, Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.abc import BaseModel
from app.models.many_to_many import company_activities


class Activity(BaseModel):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )

    # Relations.
    parent: Mapped[Optional[Self]] = relationship(
        "Activity",
        remote_side=[id],
        backref="children",
    )
    companies: Mapped[list["Company"]] = relationship(
        secondary=company_activities,
        back_populates="activities",
    )
