import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))


@pytest.fixture
def isolated_database(monkeypatch):
    import database.connection as db

    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(db, "DATABASE_NAME", os.path.join(tmpdir, "test.db"))

        profile = {
            "profile": {"name": "Test", "currency": "BRL", "review_frequency": "Monthly"},
            "income": {"monthly_average": 5000, "type": "Fixed", "additional_monthly_average": 0},
            "expenses": {
                "fixed_monthly_average": 2000,
                "variable_monthly_average": 1000,
                "categories": ["Food", "Transport"],
            },
            "debts": {"has_debt": False, "monthly_commitment": 0},
            "goals": ["Emergency reserve"],
            "preferences": {
                "communication_style": "Simple",
                "detail_level": "Basic",
                "budget_alerts": True,
            },
            "initial_snapshot": {
                "monthly_income_estimate": 5000,
                "monthly_expense_estimate": 3000,
                "estimated_balance": 2000,
                "expense_commitment_percent": 60,
            },
        }
        db.initialize_database(profile)
        yield db
