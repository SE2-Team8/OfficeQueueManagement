import datetime
import pytest
from fastapi import HTTPException

from app.features.counters import services as counters_services
from app.features.tickets import schemas as tickets_schemas
from app.features.tickets import services as tickets_services


@pytest.fixture
def counters(monkeypatch):
    """Configuration: 2 counters for tests"""
    config = {
        1: {"services": ["SHIPPING", "ACCOUNTS"]},
        2: {"services": ["DEPOSIT"]},
    }
    monkeypatch.setattr(counters_services, "COUNTERS_DATA", config)
    return config


def add_ticket(tag, number):
    """Insert a ticket directly in QUEUES"""
    ticket = tickets_schemas.TicketResponse(
        id=number,
        code=f"{tickets_services.SERVICES_DATA[tag]['code']}{number}",
        service_type=tag,
        issued_at=datetime.datetime.now(datetime.timezone.utc),
        status="WAITING",
    )
    tickets_services.QUEUES[tag].append(ticket)
    return ticket


# ---------- non-existing counter ----------

def test_unknown_counter_raises_404(counters):
    with pytest.raises(HTTPException) as exc:
        counters_services.call_next(999)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Counter not found"


def test_unknown_counter_does_not_touch_queues(counters):
    add_ticket("SHIPPING", 1)
    with pytest.raises(HTTPException):
        counters_services.call_next(999)
    assert len(tickets_services.QUEUES["SHIPPING"]) == 1


# ---------- empty queue ----------

def test_all_queues_empty_returns_none(counters):
    assert counters_services.call_next(1) is None


def test_queue_not_served_by_counter_is_ignored(counters):
    add_ticket("DEPOSIT", 1)   # counter 1 does not provide DEPOSIT

    assert counters_services.call_next(1) is None
    assert len(tickets_services.QUEUES["DEPOSIT"]) == 1   


# ---------- queue selection ----------

def test_single_candidate_is_selected(counters):
    add_ticket("ACCOUNTS", 1)

    result = counters_services.call_next(1)

    assert result.service_type == "ACCOUNTS"
    assert result.ticket_code == "A1"


def test_longest_queue_wins_even_if_not_first_in_config(counters):
    add_ticket("SHIPPING", 1)
    add_ticket("ACCOUNTS", 1)
    add_ticket("ACCOUNTS", 2)

    result = counters_services.call_next(1)

    assert result.service_type == "ACCOUNTS"


def test_tie_on_length_lowest_service_time_wins(counters, monkeypatch):
    monkeypatch.setitem(tickets_services.SERVICES_DATA["ACCOUNTS"], "service_time", 5)
    monkeypatch.setitem(tickets_services.SERVICES_DATA["SHIPPING"], "service_time", 10)
    add_ticket("SHIPPING", 1)
    add_ticket("ACCOUNTS", 1)

    assert counters_services.call_next(1).service_type == "ACCOUNTS"


def test_tie_on_length_service_time_checked_both_ways(counters, monkeypatch):
    # inverted times: should matter times before queue
    monkeypatch.setitem(tickets_services.SERVICES_DATA["ACCOUNTS"], "service_time", 10)
    monkeypatch.setitem(tickets_services.SERVICES_DATA["SHIPPING"], "service_time", 5)
    add_ticket("SHIPPING", 1)
    add_ticket("ACCOUNTS", 1)

    assert counters_services.call_next(1).service_type == "SHIPPING"


def test_full_tie_picks_first_in_counter_config(counters, monkeypatch):
    for tag in ("SHIPPING", "ACCOUNTS"):
        monkeypatch.setitem(tickets_services.SERVICES_DATA[tag], "service_time", 10)
    add_ticket("SHIPPING", 1)
    add_ticket("ACCOUNTS", 1)
    assert counters_services.call_next(1).service_type == "SHIPPING"


def test_full_tie_follows_config_order_when_reversed(counters, monkeypatch):
    for tag in ("SHIPPING", "ACCOUNTS"):
        monkeypatch.setitem(tickets_services.SERVICES_DATA[tag], "service_time", 10)
    counters[1]["services"] = ["ACCOUNTS", "SHIPPING"]
    add_ticket("SHIPPING", 1)
    add_ticket("ACCOUNTS", 1)
    assert counters_services.call_next(1).service_type == "ACCOUNTS"


def test_length_has_priority_over_service_time(counters, monkeypatch):
    # SHIPPING is slower but longer: should win
    monkeypatch.setitem(tickets_services.SERVICES_DATA["SHIPPING"], "service_time", 99)
    monkeypatch.setitem(tickets_services.SERVICES_DATA["ACCOUNTS"], "service_time", 1)
    add_ticket("SHIPPING", 1)
    add_ticket("SHIPPING", 2)
    add_ticket("ACCOUNTS", 1)

    assert counters_services.call_next(1).service_type == "SHIPPING"


# ---------- queues effects ----------

def test_popleft_removes_first_ticket_fifo(counters):
    add_ticket("SHIPPING", 1)
    add_ticket("SHIPPING", 2)

    result = counters_services.call_next(1)

    assert result.ticket_code == "S1"
    remaining = [t.code for t in tickets_services.QUEUES["SHIPPING"]]
    assert remaining == ["S2"]


def test_served_ticket_status_becomes_served(counters):
    ticket = add_ticket("SHIPPING", 1)
    assert ticket.status == "WAITING"

    counters_services.call_next(1)

    assert ticket.status == "CALLED"


def test_queue_length_is_remaining_after_pop(counters):
    for n in (1, 2, 3):
        add_ticket("SHIPPING", n)

    result = counters_services.call_next(1)

    assert result.queue_length == 2
    assert len(tickets_services.QUEUES["SHIPPING"]) == 2


def test_only_selected_queue_is_modified(counters):
    add_ticket("SHIPPING", 1)
    add_ticket("SHIPPING", 2)
    add_ticket("ACCOUNTS", 1)

    counters_services.call_next(1)   # chooses SHIPPING

    assert len(tickets_services.QUEUES["SHIPPING"]) == 1
    assert len(tickets_services.QUEUES["ACCOUNTS"]) == 1


def test_response_contains_counter_id(counters):
    add_ticket("DEPOSIT", 1)
    assert counters_services.call_next(2).counter_id == 2


def test_call_next_returns_none_without_modifying_queues(counters):
    add_ticket("DEPOSIT", 1)
    counters_services.call_next(1)   # counter 1 does not provide DEPOSIT
    assert [t.code for t in tickets_services.QUEUES["DEPOSIT"]] == ["D1"]


# ---------- get_counters ----------

def test_get_counters_maps_config(counters):
    assert counters_services.get_counters() == [
        {"id": 1, "services": ["SHIPPING", "ACCOUNTS"]},
        {"id": 2, "services": ["DEPOSIT"]},
    ]


def test_get_counters_empty_config(monkeypatch):
    monkeypatch.setattr(counters_services, "COUNTERS_DATA", {})
    assert counters_services.get_counters() == []


# ---------- others ----------

def test_real_config_counter_services_exist_in_queues():
    for counter in counters_services.COUNTERS_DATA.values():
        for tag in counter["services"]:
            assert tag in tickets_services.QUEUES
            assert tag in tickets_services.SERVICES_DATA