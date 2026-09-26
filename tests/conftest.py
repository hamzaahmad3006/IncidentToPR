import pytest
from fastapi.testclient import TestClient
from app.server import app


@pytest.fixture
def client():
    return TestClient(app)
