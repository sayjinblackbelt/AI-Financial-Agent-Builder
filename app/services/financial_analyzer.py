from datetime import date, timedelta

from database.connection import get_connection
from services.transaction_service import get_monthly_summary


def get_category_expenses():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT c.name, ROUND(SUM(t.amount), 2) AS total
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.transaction_type = 'expense'
          AND strftime('%Y-%m', t.transaction_date) = strftime('%Y-%m', 'now', 'localtime')
        GROUP BY c.name
        ORDER BY total DESC
        """
    )
    data = [
        {"category": row["name"] or "Uncategorized", "total": row["total"]}
        for row in cursor.fetchall()
    ]
    connection.close()
    return data


def get_budget_status():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT c.name, b.monthly_limit,
               COALESCE(SUM(t.amount), 0) AS spent
        FROM budgets b
        JOIN categories c ON c.id = b.category_id
        LEFT JOIN transactions t ON t.category_id = c.id
            AND t.transaction_type = 'expense'
            AND strftime('%Y-%m', t.transaction_date) = strftime('%Y-%m', 'now', 'localtime')
        WHERE b.active = 1
        GROUP BY b.id, c.name, b.monthly_limit
        ORDER BY c.name
        """
    )
    results = []
    for row in cursor.fetchall():
        limit, spent = row["monthly_limit"], row["spent"]
        percent = (spent / limit * 100) if limit > 0 else 0
        results.append(
            {
                "category": row["name"],
                "limit": limit,
                "spent": spent,
                "percent": round(percent, 1),
                "status": "exceeded"
                if percent >= 100
                else "warning"
                if percent >= 80
                else "ok",
            }
        )
    connection.close()
    return results


def get_month_comparison():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        WITH monthly AS (
            SELECT strftime('%Y-%m', transaction_date) AS month,
                   transaction_type,
                   SUM(amount) AS total
            FROM transactions
            WHERE transaction_date >= date('now', 'localtime', 'start of month', '-1 month')
            GROUP BY month, transaction_type
        )
        SELECT month, transaction_type, total
        FROM monthly
        ORDER BY month
        """
    )
    rows = cursor.fetchall()
    connection.close()

    today = date.today()
    first_day = today.replace(day=1)
    current_key = first_day.strftime("%Y-%m")
    previous_key = (first_day - timedelta(days=1)).strftime("%Y-%m")

    current_month = {}
    previous_month = {}
    for row in rows:
        if row["month"] == current_key:
            current_month[row["transaction_type"]] = row["total"]
        elif row["month"] == previous_key:
            previous_month[row["transaction_type"]] = row["total"]

    def values(data):
        income = data.get("income", 0)
        expenses = data.get("expense", 0)
        return {"income": income, "expenses": expenses, "balance": income - expenses}

    current = values(current_month)
    previous = values(previous_month)

    def change(now, before):
        absolute = now - before
        percent = (absolute / before * 100) if before else None
        return {
            "absolute": round(absolute, 2),
            "percent": round(percent, 1) if percent is not None else None,
        }

    return {
        "current": current,
        "previous": previous,
        "income_change": change(current["income"], previous["income"]),
        "expense_change": change(current["expenses"], previous["expenses"]),
        "balance_change": change(current["balance"], previous["balance"]),
    }


def analyze_finances():
    summary = get_monthly_summary()
    alerts = []
    if summary["balance"] < 0:
        alerts.append(
            {"level": "critical", "message": "Monthly registered expenses exceed registered income."}
        )
    elif summary["income"] > 0 and summary["expenses"] / summary["income"] >= 0.9:
        alerts.append(
            {"level": "warning", "message": "Expenses already represent 90% or more of registered income."}
        )

    budgets = get_budget_status()
    for budget in budgets:
        if budget["status"] == "exceeded":
            alerts.append(
                {"level": "critical", "message": f"{budget['category']} exceeded its monthly budget."}
            )
        elif budget["status"] == "warning":
            alerts.append(
                {
                    "level": "warning",
                    "message": f"{budget['category']} reached {budget['percent']}% of its monthly budget.",
                }
            )

    top_categories = get_category_expenses()[:3]
    comparison = get_month_comparison()

    trends = []
    expense_change = comparison["expense_change"]
    balance_change = comparison["balance_change"]

    if expense_change["percent"] is not None and abs(expense_change["percent"]) >= 5:
        trends.append(
            {
                "type": "expenses",
                "direction": "increased" if expense_change["absolute"] > 0 else "decreased",
                "absolute": expense_change["absolute"],
                "percent": expense_change["percent"],
            }
        )

    if balance_change["absolute"] != 0:
        trends.append(
            {
                "type": "balance",
                "direction": "improved" if balance_change["absolute"] > 0 else "worsened",
                "absolute": balance_change["absolute"],
                "percent": balance_change["percent"],
            }
        )

    return {
        "summary": summary,
        "alerts": alerts,
        "budget_status": budgets,
        "top_expense_categories": top_categories,
        "comparison": comparison,
        "trends": trends,
    }
