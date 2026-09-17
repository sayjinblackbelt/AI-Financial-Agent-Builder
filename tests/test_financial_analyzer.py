def test_financial_analyzer_contract():
    from services.financial_analyzer import analyze_finances

    result = analyze_finances()
    assert "summary" in result
    assert "alerts" in result
    assert "top_expense_categories" in result
    assert "budget_status" in result
    assert "comparison" in result
    assert "trends" in result
