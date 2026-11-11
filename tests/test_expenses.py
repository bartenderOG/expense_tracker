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
    client.post(
        "/expense",
        json={
            "amount": 300,
            "category": "food",
            "description": "Dinner",
        },
    )

    response = client.get("/expenses")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

def test_delete_nonexistent_expense():
    response = client.delete("/expense/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Expense not found"
    }


def test_delete_expense():
    create_response = client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "test",
            "description": "Expense to delete",
        },
    )

    assert create_response.status_code == 200

    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expense/{expense_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Expense deleted"
    }

def test_create_expense_with_invalid_amount():

    response = client.post(
        "/expense",
        json={
            "amount": 0,
            "category": "food",
            "description": "Invalid expense",
        },
    )

    assert response.status_code == 422

def test_create_expense_with_negative_amount():

    response = client.post(
        "/expense",
        json={
            "amount": -100,
            "category": "food",
            "description": "Negative expense",
        },
    )

    assert response.status_code == 422

def test_create_expense_with_empty_category():

    response = client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "",
            "description": "Test expense",
        },
    )

    assert response.status_code == 422

def test_create_expense_with_empty_description():

    response = client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "food",
            "description": "",
        },
    )

    assert response.status_code == 422

def test_create_expense_with_whitespace_category():

    response = client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "   ",
            "description": "Test expense",
        },
    )

    assert response.status_code == 422

def test_create_expense_with_whitespace_description():

    response = client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "food",
            "description": "   ",
        },
    )

    assert response.status_code == 422

def test_get_expenses_by_category():
    client.post(
        "/expense",
        json={
            "amount": 100,
            "category": "food",
            "description": "Lunch",
        },
    )

    client.post(
        "/expense",
        json={
            "amount": 200,
            "category": "transport",
            "description": "Taxi",
        },
    )

    response = client.get("/expenses?category=food")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "food"
    assert data[0]["amount"] == 100

def test_get_expenses_by_min_amount():
    client.post(
        "/expense",
        json={
            "amount": 100,
            "category": "food",
            "description": "Lunch",
        },
    )
    client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "transport",
            "description": "Taxi",
        },
    )

    response = client.get("/expenses?min_amount=300")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["amount"] == 500

def test_get_expenses_by_max_amount():
    client.post(
        "/expense",
        json={
            "amount": 100,
            "category": "food",
            "description": "Lunch",
        },
    )
    client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "transport",
            "description": "Taxi",
        },
    )

    response = client.get("/expenses?max_amount=300")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["amount"] == 100

def test_get_expenses_by_amount_range():
    client.post(
        "/expense",
        json={
            "amount": 50,
            "category": "food",
            "description": "Breakfast",
        },
    )
    client.post(
        "/expense",
        json={
            "amount": 250,
            "category": "food",
            "description": "Lunch",
        },
    )
    client.post(
        "/expense",
        json={
            "amount": 700,
            "category": "shopping",
            "description": "Clothes",
        },
    )

    response = client.get("/expenses?min_amount=100&max_amount=500")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["amount"] == 250

def test_get_expenses_sorted_ascending():
    client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "food",
            "description": "Lunch",
        },
    )
    client.post(
        "/expense",
        json={
            "amount": 100,
            "category": "transport",
            "description": "Bus",
        },
    )

    response = client.get("/expenses?sort=asc")

    assert response.status_code == 200
    data = response.json()

    assert [item["amount"] for item in data] == [100, 500]


def test_get_expenses_sorted_descending():
    client.post(
        "/expense",
        json={
            "amount": 100,
            "category": "food",
            "description": "Lunch",
        },
    )
    client.post(
        "/expense",
        json={
            "amount": 500,
            "category": "transport",
            "description": "Taxi",
        },
    )

    response = client.get("/expenses?sort=desc")

    assert response.status_code == 200
    data = response.json()

    assert [item["amount"] for item in data] == [500, 100]