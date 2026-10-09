import datetime
import pytest
from pydantic import ValidationError

from app.features.tickets import schemas


def test_ticket_create_requires_service_tag():
    with pytest.raises(ValidationError):
        schemas.TicketCreate()


def test_ticket_create_rejects_non_string_tag():
    with pytest.raises(ValidationError):
        schemas.TicketCreate(service_tag=123)


def test_ticket_response_accepts_valid_data():
    t = schemas.TicketResponse(
        id=1,
        code="S1",
        service_type="SHIPPING",
        issued_at=datetime.datetime.now(datetime.timezone.utc),
        status="WAITING",
    )
    assert t.code == "S1"


def test_service_base_requires_both_fields():
    with pytest.raises(ValidationError):
        schemas.ServiceBase(tag_name="SHIPPING")