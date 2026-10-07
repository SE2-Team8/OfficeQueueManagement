from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from html import escape
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

@router.get("/{ticket_code}", response_class=HTMLResponse)
async def read_item(ticket_code: str):
    code = escape(ticket_code)
    return f"""<!DOCTYPE html>
	<html>
	<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1">
	<title>Ticket {code}</title>
	<style>
	body {{
		margin: 0; height: 100vh;
		display: flex; align-items: center; justify-content: center;
		font-family: system-ui, sans-serif; background: #f4f6f8; color: #1f2933;
	}}
	.card {{
		background: #fff; padding: 3rem 4rem; border-radius: 16px;
		box-shadow: 0 10px 30px rgba(0,0,0,.08); text-align: center;
	}}
	.label {{ font-size: 1.25rem; color: #52606d; margin: 0 0 1rem; }}
	.code {{
		font-family: monospace; font-size: 3.5rem; font-weight: 700;
		color: #2563eb; word-break: break-all;
	}}
	</style>
	</head>
	<body>
	<div class="card">
		<p class="label">Your ticket is</p>
		<div class="code">{code}</div>
	</div>
	</body>
	</html>"""