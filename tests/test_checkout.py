def test_checkout_with_coupon(client):
    response = client.post("/checkout", json={"cart_total": 100.0, "coupons": ["WELCOME10"]})
    assert response.status_code == 200
    assert response.json() == {"discount_percent": 10, "payable": 90.0}


def test_invalid_coupon_ignored(client):
    response = client.post("/checkout", json={"cart_total": 100.0, "coupons": ["NOPE"]})
    assert response.status_code == 200
