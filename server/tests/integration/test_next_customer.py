import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.features.counters import services

client = TestClient(app)
client_no_raise = TestClient(app, raise_server_exceptions=False)

### GET /counters ###

def test_get_counters_status_and_count():
    resp = client.get("/counters")
    assert resp.status_code == 200
    assert len(resp.json()) > 0

def test_get_counters_right_fields():
    for counter in client.get("/counters").json():
        assert isinstance(counter["id"], int)
        assert isinstance(counter["services"], list)
        assert isinstance(counter["services"][0], str)


### POST /counters/{counter_id}/next

def test_next_customer_success():
    client.post("/tickets/", json={"service_tag": "SHIPPING"})
    resp = client.post("counters/1/next")

    assert resp.status_code == 200
    body = resp.json()
    assert body["ticket_code"] == "S1"
    assert body["service_type"] == "SHIPPING"
    assert body["counter_id"] == 1
    assert body["queue_length"] == 0

def test_next_customer_longest_queue_success():
    client.post("/tickets/", json={"service_tag": "SHIPPING"})
    client.post("/tickets/", json={"service_tag": "ACCOUNTS"})
    client.post("/tickets/", json={"service_tag": "ACCOUNTS"})

    resp = client.post("counters/1/next")
    body = resp.json()

    assert body["service_type"] == "ACCOUNTS"

def test_next_customer_shortest_service_time_success():
    client.post("/tickets/", json={"service_tag": "SHIPPING"})
    client.post("/tickets/", json={"service_tag": "ACCOUNTS"})

    resp = client.post("counters/1/next")
    body = resp.json()
    
    assert body["service_type"] == "SHIPPING"

# errors #

def test_next_customer_wrong_counter_id():
    resp = client.post("/counters/9999/next")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Counter not found"

def test_next_customer_empty_queue():
    resp = client.post("/counters/1/next")

    assert resp.status_code == 204
    assert resp.text == ""

def test_next_customer_not_in_counter_services():
    client.post("/tickets/", json={"service_tag": "DEPOSIT"})

    resp = client.post("/counters/1/next")

    assert resp.status_code == 204
    assert resp.text == ""