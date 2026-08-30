from services.financial_analyzer import get_month_comparison, analyze_finances

comparison = get_month_comparison()
assert "current" in comparison
assert "previous" in comparison
assert "expense_change" in comparison

analysis = analyze_finances()
assert "comparison" in analysis
assert "trends" in analysis

print("Historical financial analysis test passed.")
