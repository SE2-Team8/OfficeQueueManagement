from pydantic import BaseModel
from datetime import datetime

class ServiceBase(BaseModel):
    tag_name: str       # tag for the service
    service_time: int   # estimated waiting time in minutes

class TicketCreate(BaseModel):
    service_tag: str

class TicketResponse(BaseModel):
    id: int
    code: str
    service_type: str
    issued_at: datetime
    status: str

    class Config:
        from_attribute = True

class NextCustomerResponse(BaseModel):
    ticket_code: str
    service_type: str
    counter_id: int
    queue_length: int  