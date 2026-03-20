import sys
from fastapi.testclient import TestClient
from printing_api.main import app

client = TestClient(app)

passed = True

print('Running smoke tests...')

# Create order
payload = {
    "customer_name": "Alice",
    "items": [
        {"name": "Business Cards", "quantity": 100, "unit_price": 0.05},
        {"name": "Poster", "quantity": 2, "unit_price": 10.0},
    ],
}
resp = client.post('/orders', json=payload)
if resp.status_code != 201:
    print('FAILED: POST /orders returned', resp.status_code, resp.text)
    passed = False
else:
    data = resp.json()
    expected_total = round(100 * 0.05 + 2 * 10.0, 2)
    if round(data.get('total', 0), 2) != expected_total:
        print('FAILED: total mismatch', data.get('total'))
        passed = False
    else:
        oid = data.get('id')
        r2 = client.get(f'/orders/{oid}')
        if r2.status_code != 200:
            print('FAILED: GET /orders/{id} returned', r2.status_code)
            passed = False

if passed:
    print('SMOKE TESTS PASSED')
    sys.exit(0)
else:
    print('SMOKE TESTS FAILED')
    sys.exit(2)
