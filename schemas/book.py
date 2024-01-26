import datetime

from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    short_description: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    available: Mapped[bool] = mapped_column(Boolean)
    checkout_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    class Config:
        orm_mode = True
