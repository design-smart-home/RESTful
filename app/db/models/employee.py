from app.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date, UUID
from datetime import date

import uuid


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    login: Mapped[str] = mapped_column(String(60), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_promotion: Mapped[date] = mapped_column(Date)
