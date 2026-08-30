import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

class FinancialFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        import database.connection as db
        db.DATABASE_NAME = os.path.join(self.tmpdir.name, "test.db")

        self.profile = {
            "profile": {"name": "Test", "currency": "BRL", "review_frequency": "Monthly"},
            "income": {"monthly_average": 5000, "type": "Fixed", "additional_monthly_average": 0},
            "expenses": {"fixed_monthly_average": 2000, "variable_monthly_average": 1000, "categories": ["Food", "Transport"]},
            "debts": {"has_debt": False, "monthly_commitment": 0},
            "goals": ["Emergency reserve"],
            "preferences": {"communication_style": "Simple", "detail_level": "Basic", "budget_alerts": True},
            "initial_snapshot": {"monthly_income_estimate": 5000, "monthly_expense_estimate": 3000, "estimated_balance": 2000, "expense_commitment_percent": 60}
        }
        db.initialize_database(self.profile)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_transaction_summary_and_budget(self):
        from services.transaction_service import add_transaction, get_monthly_summary
        from services.budget_service import set_budget
        from services.financial_analyzer import analyze_finances

        add_transaction("Salary", 5000, "income")
        add_transaction("Market", 850, "expense", "Food")
        set_budget("Food", 800)

        summary = get_monthly_summary()
        self.assertEqual(summary["income"], 5000)
        self.assertEqual(summary["expenses"], 850)
        self.assertEqual(summary["balance"], 4150)

        analysis = analyze_finances()
        self.assertEqual(analysis["budget_status"][0]["status"], "exceeded")
        self.assertTrue(any(item["level"] == "critical" for item in analysis["alerts"]))

    def test_validation_rejects_invalid_transaction(self):
        from services.transaction_service import add_transaction
        with self.assertRaises(ValueError):
            add_transaction("", 10, "expense")
        with self.assertRaises(ValueError):
            add_transaction("Invalid", 0, "expense")

if __name__ == "__main__":
    unittest.main()
