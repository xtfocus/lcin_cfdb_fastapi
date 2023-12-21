from tests.main import client


def test_en_concept_not_found():
    response = client.get("/concept/en/ten en khong ton tai")
    assert response.status_code == 404


def test_en_concept_found():
    response1 = client.get("/concept/en/high blood pressure")
    response2 = client.get("/concept/en/hypertension")
    assert (response1.status_code == 200) & (response2.status_code == 200)
