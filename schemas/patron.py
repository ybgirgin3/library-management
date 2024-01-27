from __future__ import annotations

import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


class Patron(Base):
    __tablename__ = 'patron'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String)
    # checked_out_books: Mapped[List[BookSchema]] = mapped_column(Integer, nullable=True)
    # checked_out_books = relationship("Book", secondary="Checkout", back_populates="borrowed_by")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(),
    )
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True)

    class Config:
        orm_mode = True
