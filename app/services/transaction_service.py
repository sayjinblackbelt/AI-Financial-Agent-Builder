from datetime import date

from database.connection import get_connection


def add_transaction(description, amount, transaction_type, category_name=None, transaction_date=None):
    description = str(description or "").strip()
    amount = float(amount)
    if not description:
        raise ValueError("description is required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    if transaction_type not in {"income", "expense"}:
        raise ValueError("transaction_type must be income or expense")

    if transaction_date is None:
        transaction_date = date.today().isoformat()
    else:
        try:
            transaction_date = date.fromisoformat(str(transaction_date)).isoformat()
        except ValueError as exc:
            raise ValueError("transaction_date must be a valid ISO date (YYYY-MM-DD)") from exc

    connection = get_connection()
    try:
        cursor = connection.cursor()
        category_id = None

        if category_name:
            category_name = str(category_name).strip()
            if category_name:
                cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
                row = cursor.fetchone()
                if row:
                    category_id = row["id"]
                else:
                    cursor.execute(
                        "INSERT INTO categories (name, category_type) VALUES (?, ?)",
                        (category_name, transaction_type),
                    )
                    category_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO transactions
                (transaction_date, description, category_id, amount, transaction_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (transaction_date, description, category_id, amount, transaction_type),
        )
        transaction_id = cursor.lastrowid
        connection.commit()
        return transaction_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def get_monthly_summary():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                transaction_type,
                COALESCE(SUM(amount), 0) AS total
            FROM transactions
            WHERE strftime('%Y-%m', transaction_date) = strftime('%Y-%m', 'now', 'localtime')
            GROUP BY transaction_type
            """
        )
        rows = {row["transaction_type"]: row["total"] for row in cursor.fetchall()}
    finally:
        connection.close()

    income = rows.get("income", 0)
    expenses = rows.get("expense", 0)
    return {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
    }
