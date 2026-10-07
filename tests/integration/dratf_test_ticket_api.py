import datetime

import pytest
from fastapi.testclient import TestClient

from server.app.main import app
from server.app.features.tickets import services

client = TestClient(app)
# needed for 404, with actual code produces internal error
client_no_raise = TestClient(app, raise_server_exceptions=False)

# ---------- GET /tickets/services ----------

def test_get_services_status_and_count():
    response = client.get("/tickets/services")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_services_have_required_fields():
    for service in client.get("/tickets/services").json():
        assert isinstance(service["tag_name"], str)
        assert isinstance(service["service_time"], int)
        assert service["service_time"] > 0


@pytest.mark.xfail(strict=True, reason="BUG: ACCOUNTS and DEPOSIT have tag_name 'SHIPPING'")
def test_get_services_tags_are_unique():
    tags = [s["tag_name"] for s in client.get("/tickets/services").json()]
    assert len(tags) == len(set(tags))


@pytest.mark.xfail(strict=True, reason="BUG: ACCOUNTS and DEPOSIT have tag_name 'SHIPPING'")
def test_get_services_returns_expected_tags():
    tags = [s["tag_name"] for s in client.get("/tickets/services").json()]
    assert sorted(tags) == ["ACCOUNTS", "DEPOSIT", "SHIPPING"]


# ---------- POST /tickets/ ----------

def test_create_ticket_success():
    response = client.post("/tickets/", json={"service_tag": "SHIPPING"})

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == "S1"
    assert body["id"] == 1
    assert body["service_type"] == "SHIPPING"
    assert body["status"] == "WAITING"


@pytest.mark.parametrize(
    "tag, prefix", [("SHIPPING", "S"), ("ACCOUNTS", "A"), ("DEPOSIT", "D")]
)
def test_create_ticket_code_prefix_per_service(tag, prefix):
    body = client.post("/tickets/", json={"service_tag": tag}).json()
    assert body["code"] == f"{prefix}1"
    assert body["service_type"] == tag


def test_create_ticket_issued_at_is_valid_datetime():
    body = client.post("/tickets/", json={"service_tag": "DEPOSIT"}).json()
    issued_at = datetime.datetime.fromisoformat(body["issued_at"].replace("Z", "+00:00"))
    assert isinstance(issued_at, datetime.datetime)


def test_ticket_numbers_increment_within_same_service():
    codes = [
        client.post("/tickets/", json={"service_tag": "ACCOUNTS"}).json()["code"]
        for _ in range(3)
    ]
    assert codes == ["A1", "A2", "A3"]


def test_each_service_has_independent_counter():
    codes = [
        client.post("/tickets/", json={"service_tag": tag}).json()["code"]
        for tag in ("SHIPPING", "ACCOUNTS", "DEPOSIT", "SHIPPING")
    ]
    assert codes == ["S1", "A1", "D1", "S2"]


def test_ticket_codes_are_unique_across_office():
    codes = [
        client.post("/tickets/", json={"service_tag": tag}).json()["code"]
        for tag in ("SHIPPING", "ACCOUNTS", "DEPOSIT") * 3
    ]
    assert len(codes) == len(set(codes))


# ---------- Errors ----------

@pytest.mark.xfail(strict=True, reason="BUG: 'return HTTPException' instead of 'raise' -> 500 instead of 404")
def test_create_ticket_unknown_service_returns_404():
    response = client_no_raise.post("/tickets/", json={"service_tag": "UNKNOWN"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_unknown_service_does_not_increment_any_counter():
    client_no_raise.post("/tickets/", json={"service_tag": "UNKNOWN"})
    assert all(d["count"] == 0 for d in services.SERVICES_DATA.values())


def test_create_ticket_missing_field_returns_422():
    assert client.post("/tickets/", json={}).status_code == 422


def test_create_ticket_no_body_returns_422():
    assert client.post("/tickets/").status_code == 422


def test_create_ticket_wrong_type_returns_422():
    assert client.post("/tickets/", json={"service_tag": 123}).status_code == 422