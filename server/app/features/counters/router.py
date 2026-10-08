from fastapi import APIRouter, Response
from app.features.tickets import schemas, services

router = APIRouter(prefix="/counters", tags=["Counters"])

@router.get("/")
def list_counters():
    return services.get_counters()

@router.post(
    "/{counter_id}/next",
    response_model=schemas.NextCustomerResponse,
    responses={204: {"description": "No customers waiting"}},
)
def call_next_customer(counter_id: int):
    result = services.call_next(counter_id)
    if result is None:
        return Response(status_code=204)
    return result