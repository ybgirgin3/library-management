from pydantic import BaseModel
from datetime import datetime


class BookModel(BaseModel):
    title: str
    short_description: str
    author: str
    created_at: datetime
    updated_at: datetime
