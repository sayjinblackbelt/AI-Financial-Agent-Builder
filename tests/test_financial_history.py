def test_historical_financial_analysis_contract():
    from services.financial_analyzer import analyze_finances, get_month_comparison

    comparison = get_month_comparison()
    assert comparison["current"] == {"income": 0, "expenses": 0, "balance": 0}
    assert comparison["previous"] == {"income": 0, "expenses": 0, "balance": 0}
    assert comparison["expense_change"]["absolute"] == 0
    assert comparison["expense_change"]["percent"] is None

    analysis = analyze_finances()
    assert "comparison" in analysis
    assert "trends" in analysis
