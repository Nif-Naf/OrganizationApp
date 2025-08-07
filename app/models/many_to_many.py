from sqlalchemy import Column, ForeignKey, Table

from app.models.abc import BaseModel

company_activities = Table(  # Company ↔ Activity
    "company_activities",
    BaseModel.metadata,
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)
