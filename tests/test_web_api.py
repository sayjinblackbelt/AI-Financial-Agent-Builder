import pytest


@pytest.fixture
def client():
    from web_app import application

    application.config.update(TESTING=True)
    with application.test_client() as test_client:
        yield test_client


def test_web_smoke(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AI Financial Agent Builder" in response.data


def test_build_profile_and_transaction_flow(client):
    profile_response = client.post(
        "/api/build-profile",
        json={
            "name": "API Test",
            "currency": "BRL",
            "frequency": "Monthly",
            "income": "5000",
            "incomeType": "Fixed",
            "extra": "0",
            "fixed": "2000",
            "variable": "1000",
            "categories": ["Food", "Transport"],
            "debt": "0",
            "goals": ["Savings"],
            "style": "Simple",
            "alerts": True,
        },
    )
    assert profile_response.status_code == 200
    assert profile_response.json["snapshot"]["estimated_balance"] == 2000

    transaction_response = client.post(
        "/api/transactions",
        json={
            "description": "Salary",
            "amount": 5000,
            "transaction_type": "income",
        },
    )
    assert transaction_response.status_code == 201
    assert transaction_response.json["summary"]["income"] == 5000

    expense_response = client.post(
        "/api/transactions",
        json={
            "description": "Market",
            "amount": 500,
            "transaction_type": "expense",
            "category": "Food",
        },
    )
    assert expense_response.status_code == 201
    assert expense_response.json["summary"]["expenses"] == 500

    analysis_response = client.get("/api/analysis")
    assert analysis_response.status_code == 200
    assert analysis_response.json["summary"]["balance"] == 4500


def test_build_profile_again_does_not_erase_transactions(client):
    first = client.post(
        "/api/build-profile",
        json={"name": "First", "currency": "BRL", "income": 4000, "fixed": 1000, "variable": 500},
    )
    assert first.status_code == 200

    created = client.post(
        "/api/transactions",
        json={"description": "Salary", "amount": 4000, "transaction_type": "income"},
    )
    assert created.status_code == 201

    second = client.post(
        "/api/build-profile",
        json={"name": "Updated", "currency": "BRL", "income": 4500, "fixed": 1200, "variable": 600},
    )
    assert second.status_code == 200

    summary = client.get("/api/summary")
    assert summary.status_code == 200
    assert summary.json["income"] == 4000
