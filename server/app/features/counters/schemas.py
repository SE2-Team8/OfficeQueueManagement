from pydantic import BaseModel
from typing import List

class CounterResponse(BaseModel):
    id: int
    services: List[str]

class NextCustomerResponse(BaseModel):
    ticket_code: str
    service_type: str
    counter_id: int
    queue_length: int