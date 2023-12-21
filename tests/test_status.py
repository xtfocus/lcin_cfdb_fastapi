from tests.main import client


def test_status_validate():
    response = client.get("status/validate")
    assert response.status_code == 200


def test_status_uncharted():
    response = client.get("/status/uncharted_en_main")
    assert response.status_code == 200
    # For this example database, we have two uncharted en_main
    assert len(response.json()["uncharted_en_mains"]) == 2
