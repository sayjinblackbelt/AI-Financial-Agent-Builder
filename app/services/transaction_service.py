from database.connection import get_connection
from datetime import date

def add_transaction(description, amount, transaction_type, category_name=None, transaction_date=None):
    description = str(description or "").strip()
    amount = float(amount)
    if not description:
        raise ValueError("description is required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    if transaction_type not in {"income", "expense"}:
        raise ValueError("transaction_type must be income or expense")

    connection = get_connection()
    cursor = connection.cursor()
    category_id = None

    if category_name:
        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        row = cursor.fetchone()
        if row:
            category_id = row["id"]
        else:
            cursor.execute(
                "INSERT INTO categories (name, category_type) VALUES (?, ?)",
                (category_name, transaction_type)
            )
            category_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO transactions
        (transaction_date, description, category_id, amount, transaction_type)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction_date or date.today().isoformat(),
        description,
        category_id,
        float(amount),
        transaction_type
    ))
    transaction_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return transaction_id

def get_monthly_summary():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            transaction_type,
            COALESCE(SUM(amount), 0) AS total
        FROM transactions
        WHERE strftime('%Y-%m', transaction_date) = strftime('%Y-%m', 'now', 'localtime')
        GROUP BY transaction_type
    """)
    rows = {row["transaction_type"]: row["total"] for row in cursor.fetchall()}
    connection.close()

    income = rows.get("income", 0)
    expenses = rows.get("expense", 0)
    return {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses
    }
