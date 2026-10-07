import pytest
from fastapi import HTTPException

from server.app.features.tickets import schemas, services


# ---------- get_available_services ----------

def test_get_available_services_returns_list_of_dicts():
    result = services.get_available_services()
    assert isinstance(result, list)
    assert len(result) == 3


def test_get_available_services_exposes_only_tag_and_time():
    for item in services.get_available_services():
        assert set(item.keys()) == {"tag_name", "service_time"}


def test_get_available_services_tags_are_unique():  #BUG: ACCOUNTS e DEPOSIT have tag_name 'SHIPPING'
    tags = [s["tag_name"] for s in services.get_available_services()]
    assert len(tags) == len(set(tags))


# ---------- create_ticket ----------

def test_create_ticket_builds_code_from_prefix_and_counter():
    ticket = services.create_ticket(schemas.TicketCreate(service_tag="DEPOSIT"))
    assert ticket.code == "D1"
    assert ticket.id == 1
    assert ticket.service_type == "DEPOSIT"
    assert ticket.status == "WAITING"


def test_create_ticket_increments_per_service():
    c1 = services.create_ticket(schemas.TicketCreate(service_tag="SHIPPING")).code
    c2 = services.create_ticket(schemas.TicketCreate(service_tag="SHIPPING")).code
    other = services.create_ticket(schemas.TicketCreate(service_tag="ACCOUNTS")).code
    assert (c1, c2, other) == ("S1", "S2", "A1")


def test_create_ticket_sets_issued_at():
    ticket = services.create_ticket(schemas.TicketCreate(service_tag="ACCOUNTS"))
    assert ticket.issued_at is not None


def test_create_ticket_unknown_service_raises_404():   
    with pytest.raises(HTTPException) as exc:
        services.create_ticket(schemas.TicketCreate(service_tag="NOPE"))
    assert exc.value.status_code == 404


def test_create_ticket_unknown_service_does_not_consume_a_number():
    services.create_ticket(schemas.TicketCreate(service_tag="NOPE"))
    ticket = services.create_ticket(schemas.TicketCreate(service_tag="SHIPPING"))
    assert ticket.code == "S1"