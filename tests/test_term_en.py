from tests.main import client


def test_en_term_not_found():
    response = client.get("/term/en/ten en khong ton tai")
    assert (response.status_code == 200) & (response.content == b"false")


def test_en_term_found():
    response1 = client.get("/term/en/high blood pressure")
    response2 = client.get("/term/en/hypertension")
    assert (
        (response1.status_code == 200)
        & (response2.status_code == 200)
        & (response1.content == b"true")
        & (response2.content == b"true")
    )
