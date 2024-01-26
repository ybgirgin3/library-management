from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BookModel(BaseModel):
    title: str
    short_description: str
    author: str
    available: bool
    # checkout_date: Optional[datetime] = None
