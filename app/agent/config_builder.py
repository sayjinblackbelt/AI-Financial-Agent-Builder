def build_agent_config(profile):
    preferences = profile["preferences"]

    return {
        "agent_name": "Personal Financial Assistant",
        "mode": "local-first",
        "financial_profile": profile["profile"],
        "goals": profile["goals"],
        "categories": profile["expenses"]["categories"],
        "monitoring": {
            "review_frequency": profile["profile"]["review_frequency"],
            "budget_alerts_enabled": preferences["budget_alerts"],
            "budget_warning_percent": 80,
            "monthly_comparison": True,
            "trend_detection": True
        },
        "communication": {
            "style": preferences["communication_style"],
            "detail_level": preferences["detail_level"]
        },
        "restrictions": [
            "Do not execute financial transactions",
            "Do not request banking credentials",
            "Do not make autonomous investment decisions",
            "Ask for clarification when financial data is incomplete"
        ]
    }
