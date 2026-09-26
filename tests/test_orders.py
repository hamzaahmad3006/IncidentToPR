def test_page2_starts_after_page1(client):
    response = client.get("/orders?page=2&size=10")
    assert response.status_code == 200
    assert response.json()["items"][0]["id"] == "ORD-0011"


def test_single_order(client):
    response = client.get("/orders/ORD-0010")
    assert response.status_code == 200
    assert response.json()["id"] == "ORD-0010"


def test_unknown_order(client):
    response = client.get("/orders/ORD-9999")
    assert response.status_code == 404
