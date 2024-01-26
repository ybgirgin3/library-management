from pydantic import BaseModel
from models import BookModel
from typing import Optional, List


class PatronModel(BaseModel):
    name: str
    email: str
    # checked_out_books: Optional[List[int]] = None
