from database.connection import initialize_database
from services.financial_profile_service import calculate_initial_snapshot
from services.transaction_service import add_transaction, get_monthly_summary

profile = {
    "profile": {"name": "Test User", "currency": "BRL", "review_frequency": "Monthly"},
    "income": {"monthly_average": 5000, "type": "Fixed", "additional_monthly_average": 0},
    "expenses": {"fixed_monthly_average": 1800, "variable_monthly_average": 1200, "categories": ["Food"]},
    "debts": {"has_debt": False, "monthly_commitment": 0},
    "goals": ["Emergency reserve"],
    "preferences": {"communication_style": "Simple", "detail_level": "Basic", "budget_alerts": True}
}

profile["initial_snapshot"] = calculate_initial_snapshot(profile)
initialize_database(profile)
add_transaction("Salary", 5000, "income")
add_transaction("Supermarket", 150, "expense", "Food")

summary = get_monthly_summary()
assert summary["income"] >= 5000
assert summary["expenses"] >= 150
assert summary["balance"] >= 4850
print("Financial database flow test passed.")
