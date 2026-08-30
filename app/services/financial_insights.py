from services.financial_analyzer import analyze_finances

def build_financial_insights():
    analysis = analyze_finances()
    summary = analysis["summary"]
    insights = []

    if summary["income"] == 0 and summary["expenses"] == 0:
        insights.append({
            "priority": "info",
            "title": "Start tracking your finances",
            "message": "No transactions have been registered yet. Add income and expenses to begin building your financial picture."
        })
    elif summary["income"] == 0 and summary["expenses"] > 0:
        insights.append({
            "priority": "high",
            "title": "Income has not been registered",
            "message": "Expenses exist for the current month, but no income was registered. Add your income for a more accurate balance."
        })
    elif summary["balance"] < 0:
        insights.append({
            "priority": "high",
            "title": "Negative monthly balance",
            "message": f"Registered expenses are currently higher than income by {abs(summary['balance']):.2f}."
        })
    elif summary["expenses"] / summary["income"] >= 0.8:
        insights.append({
            "priority": "medium",
            "title": "High expense commitment",
            "message": "A large part of your registered income has already been committed to expenses this month."
        })
    else:
        insights.append({
            "priority": "positive",
            "title": "Current balance is positive",
            "message": "Registered income is currently higher than registered expenses."
        })

    for alert in analysis["alerts"]:
        insights.append({
            "priority": "high" if alert["level"] == "critical" else "medium",
            "title": "Financial alert",
            "message": alert["message"]
        })

    if analysis["top_expense_categories"]:
        top = analysis["top_expense_categories"][0]
        insights.append({
            "priority": "info",
            "title": "Largest expense category",
            "message": f"{top['category']} is currently your largest recorded expense category, totaling {top['total']:.2f} this month."
        })

    for trend in analysis["trends"]:
        if trend["type"] == "expenses":
            direction = "increased" if trend["direction"] == "increased" else "decreased"
            insights.append({
                "priority": "medium",
                "title": "Expense trend",
                "message": f"Monthly expenses {direction} by {abs(trend['absolute']):.2f} compared with the previous month."
            })
        if trend["type"] == "balance":
            direction = "improved" if trend["direction"] == "improved" else "worsened"
            insights.append({
                "priority": "positive" if direction == "improved" else "medium",
                "title": "Balance trend",
                "message": f"Your monthly balance {direction} by {abs(trend['absolute']):.2f} compared with the previous month."
            })

    return {"summary": summary, "insights": insights, "analysis": analysis}

def build_financial_narrative():
    data = build_financial_insights()
    messages = [item["message"] for item in data["insights"]]
    return " ".join(messages)
