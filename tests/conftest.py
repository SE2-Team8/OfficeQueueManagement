import pytest
from server.app.features.tickets import services


@pytest.fixture(autouse=True)
def reset_state():
    """SERVICES_DATA is a global state: reset counters before and after each test."""
    for data in services.SERVICES_DATA.values():
        data["count"] = 0
    yield
    for data in services.SERVICES_DATA.values():
        data["count"] = 0