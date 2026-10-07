from fastapi import APIRouter
from typing import List
from app.features.tickets import schemas, services

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/services", response_model=List[schemas.ServiceBase])
def get_services():
    # Return the list of services (hard coded at the moment)
    return services.get_available_services()

@router.post("/", response_model=schemas.TicketResponse)
def create_ticket(ticket_in: schemas.TicketCreate):
    # Create a new ticket for the selected service
    return services.create_ticket(ticket_in)