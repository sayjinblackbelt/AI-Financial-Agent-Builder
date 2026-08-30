from dataclasses import dataclass, field

@dataclass
class FinancialProfile:
    name: str
    currency: str = "BRL"
    review_frequency: str = "Monthly"
    monthly_income: float = 0
    income_type: str = "Fixed"
    additional_income: float = 0
    fixed_expenses: float = 0
    variable_expenses: float = 0
    categories: list[str] = field(default_factory=list)
    has_debt: bool = False
    debt_commitment: float = 0
    goals: list[str] = field(default_factory=list)
