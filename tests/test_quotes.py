def test_quote_without_discount(client):
    response = client.post("/quotes", json={"lines": [{"sku": "A", "price": 10.0, "qty": 2}]})
    assert response.status_code == 200
    assert response.json()["total"] == 20.0


def test_quote_with_discount(client):
    response = client.post("/quotes", json={"lines": [{"sku": "A", "price": 50.0, "qty": 2}], "discount_percent": 10})
    assert response.status_code == 200
    assert response.json()["total"] == 90.0
