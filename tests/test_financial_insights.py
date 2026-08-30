from services.financial_insights import build_financial_insights, build_financial_narrative

data = build_financial_insights()
assert "summary" in data
assert "insights" in data
assert isinstance(data["insights"], list)

narrative = build_financial_narrative()
assert isinstance(narrative, str)
print("Financial insights test passed.")
