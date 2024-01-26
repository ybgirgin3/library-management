from sqlalchemy import DateTime, Integer, String, ForeignKey, LargeBinary, Column
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# from .book import Book
# from .patron import Patron

Base = declarative_base()


class Checkout(Base):
    __tablename__ = "checkout"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patron_id: Mapped[int] = mapped_column(Integer)
    book_id: Mapped[int] = mapped_column(Integer)
    checkout_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow()
    )
