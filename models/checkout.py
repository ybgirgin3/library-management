from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CheckoutModel(BaseModel):
    patron_id: int
    book_id: int
    checkout_date: Optional[datetime] = None
