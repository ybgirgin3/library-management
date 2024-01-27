from __future__ import annotations

import datetime
from typing import List

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class BookSchema(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    short_description: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    available: Mapped[bool] = mapped_column(Boolean)
    # checkout_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    class Config:
        orm_mode = True


class CheckoutSchema(Base):
    __tablename__ = 'checkout'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patron_id: Mapped[int] = mapped_column(Integer)
    book_id: Mapped[int] = mapped_column(Integer)
    checkout_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow(),
    )
    expiring_data: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=(
            datetime.datetime.utcnow() +
            datetime.timedelta(days=10)
        ),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    class Config:
        orm_mode = True


class PatronSchema(Base):
    __tablename__ = 'patron'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String)
    # checked_out_books: Mapped[List[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    class Config:
        orm_mode = True
