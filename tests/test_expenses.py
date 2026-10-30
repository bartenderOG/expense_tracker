from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_expense():
    response = client.post(
        "/expense",
        json={
            "amount": 700,
            "category": "food",
            "description": "Lunch",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["amount"] == 700
    assert data["category"] == "food"
    assert data["description"] == "Lunch"


def test_get_expenses():
    response = client.get("/expenses")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0