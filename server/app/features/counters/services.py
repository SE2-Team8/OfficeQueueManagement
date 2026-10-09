from fastapi import HTTPException

from app.features.counters import schemas
from app.features.tickets import services as tickets_services

COUNTERS_DATA = {
    1: {"services": ["SHIPPING", "ACCOUNTS"]},
    2: {"services": ["DEPOSIT", "SHIPPING"]},
    3: {"services": ["ACCOUNTS"]},
}

def get_counters() -> list[dict]:
    return [
        {"id": counter_id, "services": counter["services"]}
        for counter_id, counter in COUNTERS_DATA.items()
    ]

def call_next(counter_id: int) -> schemas.NextCustomerResponse | None:
    counter = COUNTERS_DATA.get(counter_id)
    if counter is None:
        raise HTTPException(status_code=404, detail="Counter not found")

    queues = tickets_services.QUEUES
    services_data = tickets_services.SERVICES_DATA

    # only non-empty queues between those served in this counter
    candidates = [tag for tag in counter["services"] if queues[tag]]
    if not candidates:
        return None

    tag = min(
        candidates,
        key=lambda t: (-len(queues[t]), services_data[t]["service_time"]),
    )

    ticket = queues[tag].popleft()  #ticket picked from the queue
    ticket.status = "CALLED"

    return schemas.NextCustomerResponse(
        ticket_code=ticket.code,
        service_type=tag,
        counter_id=counter_id,
        queue_length=len(queues[tag])
    )