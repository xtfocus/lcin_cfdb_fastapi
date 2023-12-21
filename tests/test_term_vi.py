from tests.main import client


def test_vi_term_not_found():
    response = client.get("/term/vi/ten vi khong ton tai")
    assert (response.status_code == 200) & (response.content == b"false")


def test_vi_term_found():
    response1 = client.get("/term/vi/cao huyết áp")
    response2 = client.get("/term/vi/tăng huyết áp")
    assert (
        (response1.status_code == 200)
        & (response2.status_code == 200)
        & (response1.content == b"true")
        & (response2.content == b"true")
    )
