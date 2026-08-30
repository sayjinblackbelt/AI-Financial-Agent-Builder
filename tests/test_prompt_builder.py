from agent.prompt_builder import build_agent_prompt
from agent.config_builder import build_agent_config

sample_profile = {
    "profile": {"name": "Test User", "currency": "BRL", "review_frequency": "Monthly"},
    "income": {"monthly_average": 5000, "type": "Fixed", "additional_monthly_average": 500},
    "expenses": {
        "fixed_monthly_average": 1800,
        "variable_monthly_average": 1200,
        "categories": ["Housing", "Food", "Transport"]
    },
    "debts": {"has_debt": False, "monthly_commitment": 0},
    "goals": ["Emergency reserve", "Savings"],
    "preferences": {
        "communication_style": "Simple",
        "detail_level": "Basic",
        "budget_alerts": True
    }
}

config = build_agent_config(sample_profile)
prompt = build_agent_prompt(sample_profile, config)

assert "Test User" in prompt
assert "5000" in prompt
assert "Emergency reserve" in prompt
assert "Do not execute financial transactions" in prompt

print("Prompt builder test passed.")
