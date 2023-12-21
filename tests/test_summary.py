from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_table_summary():
    response = client.get("table/summary/CID_LCIN_EN_UMLS")
    assert response.status_code == 200
