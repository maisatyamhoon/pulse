from pydantic import BaseModel
from datetime import datetime

class TransactionOut(BaseModel):
    date: datetime
    amount: float
    type: str
    raw_description: str
    source: str

    class Config:
        from_attributes = True