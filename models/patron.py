from pydantic import BaseModel


class PatronModel(BaseModel):
    name: str
    email: str
