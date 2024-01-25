from pydantic import BaseModel

class Patron(BaseModel):
    name: str
    email: str
