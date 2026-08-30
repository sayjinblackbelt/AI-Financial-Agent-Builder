from onboarding.questions import ask_text, ask_number, choose_option

def build_financial_profile():
    print("\nSTEP 1 — BASIC PROFILE")
    name = ask_text("Preferred name")
    currency = choose_option("Currency", ["BRL", "USD", "EUR"])
    frequency = choose_option(
        "How often do you want to review finances?",
        ["Daily", "Weekly", "Monthly"]
    )

    print("\nSTEP 2 — INCOME")
    income = ask_number("Average monthly income")
    income_type = choose_option(
        "Income type",
        ["Fixed", "Variable", "Mixed"]
    )
    additional_income = ask_number("Average additional monthly income", 0)

    print("\nSTEP 3 — EXPENSES")
    fixed_expenses = ask_number("Average fixed monthly expenses", 0)
    variable_expenses = ask_number("Average variable monthly expenses", 0)
    categories = ask_text(
        "Categories to track (separate with commas)",
        "Housing, Food, Transport, Health, Education, Leisure"
    )
    categories = [item.strip() for item in categories.split(",") if item.strip()]

    print("\nSTEP 4 — DEBTS")
    has_debt = choose_option("Do you currently have debts?", ["No", "Yes"])
    debt_commitment = ask_number("Average monthly debt commitment", 0) if has_debt == "Yes" else 0

    print("\nSTEP 5 — GOALS")
    goals = []
    for goal in ["Emergency reserve", "Debt reduction", "Savings", "Planned purchase"]:
        answer = choose_option(f"Include goal: {goal}?", ["No", "Yes"])
        if answer == "Yes":
            goals.append(goal)
    custom_goal = ask_text("Other financial goal (optional)")
    if custom_goal:
        goals.append(custom_goal)

    print("\nSTEP 6 — AGENT PREFERENCES")
    communication_style = choose_option(
        "Communication style",
        ["Simple", "Objective", "Detailed"]
    )
    detail_level = choose_option(
        "Detail level",
        ["Basic", "Intermediate", "Detailed"]
    )
    alerts = choose_option("Enable budget alerts?", ["Yes", "No"])

    return {
        "profile": {
            "name": name,
            "currency": currency,
            "review_frequency": frequency
        },
        "income": {
            "monthly_average": income,
            "type": income_type,
            "additional_monthly_average": additional_income
        },
        "expenses": {
            "fixed_monthly_average": fixed_expenses,
            "variable_monthly_average": variable_expenses,
            "categories": categories
        },
        "debts": {
            "has_debt": has_debt == "Yes",
            "monthly_commitment": debt_commitment
        },
        "goals": goals,
        "preferences": {
            "communication_style": communication_style,
            "detail_level": detail_level,
            "budget_alerts": alerts == "Yes"
        }
    }
