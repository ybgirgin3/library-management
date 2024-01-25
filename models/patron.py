from pydantic import BaseModel
from datetime import datetime

class PatronModel(BaseModel):
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
