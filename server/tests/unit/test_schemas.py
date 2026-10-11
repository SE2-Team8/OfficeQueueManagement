import datetime
import pytest
from pydantic import ValidationError

from app.features.tickets import schemas as ticket_schemas
from app.features.counters import schemas as counter_schemas

### Ticket schemas ###

def test_ticket_create_requires_service_tag():
    with pytest.raises(ValidationError):
        ticket_schemas.TicketCreate()


def test_ticket_create_rejects_non_string_tag():
    with pytest.raises(ValidationError):
        ticket_schemas.TicketCreate(service_tag=123)


def test_ticket_response_accepts_valid_data():
    t = ticket_schemas.TicketResponse(
        id=1,
        code="S1",
        service_type="SHIPPING",
        issued_at=datetime.datetime.now(datetime.timezone.utc),
        status="WAITING",
    )
    assert t.code == "S1"


def test_service_base_requires_both_fields():
    with pytest.raises(ValidationError):
        ticket_schemas.ServiceBase(tag_name="SHIPPING")

### Counter schemas ###

def test_counter_response_id_not_number():
    with pytest.raises(ValidationError):
        counter_schemas.CounterResponse(id="abc", services=[])

def test_next_customer_response_valid_data():
    c = counter_schemas.NextCustomerResponse(
        ticket_code="S1",
        service_type="SHIPPING",
        counter_id=1,
        queue_length=1
    )

    assert c.counter_id == 1
    assert c.ticket_code == "S1"
    assert c.service_type == "SHIPPING"
    assert c.queue_length == 1