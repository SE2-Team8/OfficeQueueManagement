import pytest
from app.features.tickets import services


@pytest.fixture(autouse=True)
def reset_state():
    """SERVICES_DATA is a global state: reset counters before and after each test."""
    def _reset():
        for data in services.SERVICES_DATA.values():
            data["count"] = 0
        for q in services.QUEUES.values():
            q.clear()
    _reset()
    yield
    _reset()