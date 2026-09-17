def test_financial_database_flow():
    from services.transaction_service import add_transaction, get_monthly_summary

    add_transaction("Salary", 5000, "income")
    add_transaction("Supermarket", 150, "expense", "Food")

    summary = get_monthly_summary()
    assert summary["income"] == 5000
    assert summary["expenses"] == 150
    assert summary["balance"] == 4850
