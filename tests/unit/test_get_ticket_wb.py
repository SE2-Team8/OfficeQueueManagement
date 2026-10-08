import pytest
from fastapi import HTTPException
from app.features.tickets import schemas
from app.features.tickets.services import get_available_services, create_ticket, QUEUES, SERVICES_DATA

#pytestmark=pytest.mark.whitebox

def test_all_services_are_returned():
    assert len(get_available_services()) == len(SERVICES_DATA.keys())


#test below failed because an exception should be raised instead of being returned.
def test_create_ticket_for_a_wrong_service():
    with pytest.raises(HTTPException):
        create_ticket(schemas.TicketCreate(service_tag="WRONG STRING"))

def test_create_valid_ticket():
    ticket = create_ticket(schemas.TicketCreate(service_tag="SHIPPING"))
    assert ticket in QUEUES["SHIPPING"]


    
