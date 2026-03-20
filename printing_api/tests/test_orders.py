from fastapi.testclient import TestClient
from printing_api.main import app

client = TestClient(app)


def test_create_and_get_order():
    payload = {
        "customer_name": "Alice",
        "items": [
            {"name": "Business Cards", "quantity": 100, "unit_price": 0.05},
            {"name": "Poster", "quantity": 2, "unit_price": 10.0},
        ],
    }
    resp = client.post("/orders", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["customer_name"] == "Alice"
    assert "id" in data
    # total should be computed accurately
    expected_total = round(100 * 0.05 + 2 * 10.0, 2)
    assert round(data["total"], 2) == expected_total

    oid = data["id"]
    r2 = client.get(f"/orders/{oid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == oid
