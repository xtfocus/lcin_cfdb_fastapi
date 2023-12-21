from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_vi_term_not_found():
    response = client.get("/concept/vi/ten vi khong ton tai")
    assert response.status_code == 404


def test_vi_term_found():
    response = client.get("/concept/vi/cao huyết áp")
    assert response.status_code == 200
