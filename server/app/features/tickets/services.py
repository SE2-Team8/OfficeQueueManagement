from fastapi import HTTPException
from app.features.tickets import schemas
import datetime

SERVICES_DATA = {
    "SHIPPING": {"tag_name": "SHIPPING", "code": "S", "service_time": 10, "count": 0},
    "ACCOUNTS": {"tag_name": "ACCOUNTS", "code": "A", "service_time": 10, "count": 0},
    "DEPOSIT": {"tag_name": "DEPOSIT", "code": "D", "service_time": 10, "count": 0}
}

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

    return schemas.TicketResponse(
        id=service["count"],
        code=ticket_code,
        service_type=ticket_in.service_tag,
        issued_at=datetime.datetime.utcnow(),
        status="WAITING"
    )