from tests.main import client


def test_vi_concept_not_found():
    response = client.get("/concept/vi/ten vi khong ton tai")
    assert response.status_code == 404


def test_vi_concept_found():
    response1 = client.get("/concept/vi/cao huyết áp")
    response2 = client.get("/concept/vi/tăng huyết áp")
    assert (response1.status_code == 200) & (response2.status_code == 200)
