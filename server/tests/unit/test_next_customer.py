import pytest
from fastapi import HTTPException
import datetime
from collections import deque

from app.features.counters import schemas, services
from app.features.tickets import services as ticket_services

# mock class for ticket
class MockTicket:
    def __init__(self, id, code, service_type):
        self.id = id
        self.code = code
        self.service_type = service_type
        self.issued_at = datetime.datetime.utcnow()
        self.status="WAITING"

### get_counters ###

def test_get_counters_returns_list_of_dicts():
    res = services.get_counters()
    assert isinstance(res, list)
    assert len(res) > 0

def test_get_counters_exposes_only_id_and_services():
    for item in services.get_counters():
        assert set(item.keys()) == {"id", "services"}

def test_get_counters_ids_are_unique():
    ids = [c["id"] for c in services.get_counters()]
    assert len(ids) == len(set(ids))

### call_next ###

def test_call_next_invalid_counter_raises_404():
    with pytest.raises(HTTPException) as exc:
        services.call_next(99)
    assert exc.value.status_code == 404

def test_call_next_empty_queues_returns_none():
    result = services.call_next(1)
    assert result is None

def test_call_next_longest_queue_selected():
    ticket_services.QUEUES["SHIPPING"].extend([MockTicket(1, "S1", "SHIPPING"), MockTicket(2, "S2", "SHIPPING"), MockTicket(3, "S3", "SHIPPING")])
    ticket_services.QUEUES["ACCOUNTS"].append(MockTicket(1, "A1", "ACCOUNTS"))
    
    result = services.call_next(1)
    
    assert result.service_type == "SHIPPING"
    assert result.ticket_code == "S1"

    assert len(ticket_services.QUEUES["SHIPPING"]) == 2

def test_call_next_tie_breaker_lowest_service_time():
    ticket_services.QUEUES["SHIPPING"].append(MockTicket(1, "S1", "SHIPPING"))
    ticket_services.QUEUES["ACCOUNTS"].append(MockTicket(1, "A1", "ACCOUNTS"))
    
    result = services.call_next(1)
    
    assert result.service_type == "SHIPPING"
    assert result.ticket_code == "S1"