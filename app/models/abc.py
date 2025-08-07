from datetime import UTC, datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
    )
