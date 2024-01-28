from typing import Optional

from pydantic import BaseModel


class PatronModel(BaseModel):
    name: str
    email: str
    is_active: Optional[bool]
    is_super: Optional[bool]
