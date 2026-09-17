import unittest


class FinancialFlowTests(unittest.TestCase):
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
        with self.assertRaises(ValueError):
            add_transaction("Invalid", 10, "transfer")
        with self.assertRaises(ValueError):
            add_transaction("Invalid", 10, "expense", transaction_date="2026-02-30")

    def test_reinitializing_profile_preserves_transactions_and_budgets(self):
        from database.connection import initialize_database, get_connection
        from services.transaction_service import add_transaction, get_monthly_summary
        from services.budget_service import set_budget

        add_transaction("Salary", 5000, "income")
        add_transaction("Market", 500, "expense", "Food")
        set_budget("Food", 800)

        updated_profile = {
            "profile": {"name": "Updated", "currency": "BRL", "review_frequency": "Weekly"},
            "income": {"monthly_average": 5500, "type": "Fixed", "additional_monthly_average": 0},
            "expenses": {
                "fixed_monthly_average": 2000,
                "variable_monthly_average": 1200,
                "categories": ["Food", "Transport", "Education"],
            },
            "debts": {"has_debt": False, "monthly_commitment": 0},
            "goals": ["Savings"],
            "preferences": {
                "communication_style": "Objective",
                "detail_level": "Intermediate",
                "budget_alerts": False,
            },
            "initial_snapshot": {
                "monthly_income_estimate": 5500,
                "monthly_expense_estimate": 3200,
                "estimated_balance": 2300,
                "expense_commitment_percent": 58.2,
            },
        }
        initialize_database(updated_profile)

        summary = get_monthly_summary()
        self.assertEqual(summary["income"], 5000)
        self.assertEqual(summary["expenses"], 500)

        connection = get_connection()
        try:
            transaction_count = connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            budget_count = connection.execute("SELECT COUNT(*) FROM budgets").fetchone()[0]
            profile_name = connection.execute("SELECT name FROM profile WHERE id = 1").fetchone()[0]
        finally:
            connection.close()

        self.assertEqual(transaction_count, 2)
        self.assertEqual(budget_count, 1)
        self.assertEqual(profile_name, "Updated")
