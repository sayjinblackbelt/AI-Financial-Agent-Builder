from database.connection import get_connection
from services.transaction_service import get_monthly_summary

def get_category_expenses():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT c.name, ROUND(SUM(t.amount), 2) AS total
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.transaction_type = 'expense'
          AND strftime('%Y-%m', t.transaction_date) = strftime('%Y-%m', 'now')
        GROUP BY c.name
        ORDER BY total DESC
    """)
    data = [{"category": row["name"] or "Uncategorized", "total": row["total"]} for row in cursor.fetchall()]
    connection.close()
    return data

def get_budget_status():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT c.name, b.monthly_limit,
               COALESCE(SUM(t.amount), 0) AS spent
        FROM budgets b
        JOIN categories c ON c.id = b.category_id
        LEFT JOIN transactions t ON t.category_id = c.id
            AND t.transaction_type = 'expense'
            AND strftime('%Y-%m', t.transaction_date) = strftime('%Y-%m', 'now')
        WHERE b.active = 1
        GROUP BY b.id
    """)
    results = []
    for row in cursor.fetchall():
        limit, spent = row["monthly_limit"], row["spent"]
        percent = (spent / limit * 100) if limit > 0 else 0
        results.append({
            "category": row["name"], "limit": limit, "spent": spent,
            "percent": round(percent, 1),
            "status": "exceeded" if percent >= 100 else "warning" if percent >= 80 else "ok"
        })
    connection.close()
    return results

def analyze_finances():
    summary = get_monthly_summary()
    alerts = []
    if summary["balance"] < 0:
        alerts.append({"level": "critical", "message": "Monthly registered expenses exceed registered income."})
    elif summary["income"] > 0 and summary["expenses"] / summary["income"] >= 0.9:
        alerts.append({"level": "warning", "message": "Expenses already represent 90% or more of registered income."})

    budgets = get_budget_status()
    for budget in budgets:
        if budget["status"] == "exceeded":
            alerts.append({"level": "critical", "message": f"{budget['category']} exceeded its monthly budget."})
        elif budget["status"] == "warning":
            alerts.append({"level": "warning", "message": f"{budget['category']} reached {budget['percent']}% of its monthly budget."})

    top_categories = get_category_expenses()[:3]
    return {"summary": summary, "alerts": alerts, "budget_status": budgets, "top_expense_categories": top_categories}
