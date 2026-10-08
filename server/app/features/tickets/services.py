from fastapi import HTTPException
from app.features.tickets import schemas
import datetime
from collections import deque

SERVICES_DATA = {
    "SHIPPING": {"tag_name": "SHIPPING", "code": "S", "service_time": 10, "count": 0},
    "ACCOUNTS": {"tag_name": "ACCOUNTS", "code": "A", "service_time": 10, "count": 0},
    "DEPOSIT": {"tag_name": "DEPOSIT", "code": "D", "service_time": 10, "count": 0}
}

COUNTERS_DATA = {
    1: {"services": ["SHIPPING", "ACCOUNTS"]},
    2: {"services": ["DEPOSIT", "SHIPPING"]},
    3: {"services": ["ACCOUNTS"]},
}

QUEUES = {tag: deque() for tag in SERVICES_DATA}

def get_available_services():
    return [
        {"tag_name": data["tag_name"], "service_time": data["service_time"]}
        for data in SERVICES_DATA.values()
    ]

def create_ticket(ticket_in: schemas.TicketCreate) -> schemas.TicketResponse:
    # find the service
    service = SERVICES_DATA.get(ticket_in.service_tag)

    if not service:
        return HTTPException(status_code=404, detail="Service not found")

    service["count"] += 1
    ticket_code = f"{service['code']}{service['count']}"
    ticket = schemas.TicketResponse(
        id=service["count"],
        code=ticket_code,
        service_type=ticket_in.service_tag,
        issued_at=datetime.datetime.utcnow(),
        status="WAITING"
    )

    QUEUES[ticket_in.service_tag].append(ticket)

    return ticket

def call_next(counter_id: int) -> schemas.NextCustomerResponse | None:
    counter = COUNTERS_DATA.get(counter_id)
    if counter is None:
        raise HTTPException(status_code=404, detail="Counter not found")

    # only non-empty queues between those served in this counter
    candidates = [tag for tag in counter["services"] if QUEUES[tag]]
    if not candidates:
        return None

    tag = min(
        candidates,
        key=lambda t: (-len(QUEUES[t]), SERVICES_DATA[t]["service_time"]),
    )

    ticket = QUEUES[tag].popleft()  #ticket picked from the queue
    ticket.status = "SERVED"

    return schemas.NextCustomerResponse(
        ticket_code=ticket.code,
        service_type=tag,
        counter_id=counter_id,
        queue_length=len(QUEUES[tag])
    )