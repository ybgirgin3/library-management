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
    is_super: Mapped[bool] = mapped_column(Boolean, default=False)

    class Config:
        orm_mode = True

    def to_dict(self):
        """
        Convert SQLAlchemy model instance to a dictionary.
        """
        model_dict = {}
        for column in self.__table__.columns:
            model_dict[column.name] = getattr(self, column.name)
        return model_dict
