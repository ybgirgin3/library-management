from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CheckoutModel(BaseModel):
    patron_id: int
    book_id: int
    checkout_date: Optional[datetime] = None
    refund_date: Optional[datetime] = None
    is_active: bool = True
