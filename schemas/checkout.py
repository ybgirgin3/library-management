import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# from .book import Book
# from .patron import Patron

Base = declarative_base()



class CheckoutSchema(Base):
    __tablename__ = 'checkout'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patron_id: Mapped[int] = mapped_column(Integer)
    book_id: Mapped[int] = mapped_column(Integer)
    checkout_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow(),
    )
    refund_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=(
            datetime.datetime.utcnow() +
            datetime.timedelta(days=10)
        ),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

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
