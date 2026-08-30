def calculate_initial_snapshot(profile):
    income = (
        profile["income"]["monthly_average"]
        + profile["income"]["additional_monthly_average"]
    )
    expenses = (
        profile["expenses"]["fixed_monthly_average"]
        + profile["expenses"]["variable_monthly_average"]
        + profile["debts"]["monthly_commitment"]
    )

    return {
        "monthly_income_estimate": income,
        "monthly_expense_estimate": expenses,
        "estimated_balance": income - expenses,
        "expense_commitment_percent": round((expenses / income * 100), 2) if income else None
    }