from pydantic import BaseModel

class Book(BaseModel):
    title: str
    short_description: str
    author: str

