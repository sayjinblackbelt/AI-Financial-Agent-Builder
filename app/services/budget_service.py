from database.connection import get_connection

def set_budget(category_name, monthly_limit):
    if float(monthly_limit) <= 0:
        raise ValueError("monthly_limit must be positive")
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO categories (name, category_type) VALUES (?, 'expense')", (category_name,))
        category_id = cursor.lastrowid
    else:
        category_id = row["id"]
    cursor.execute("SELECT id FROM budgets WHERE category_id = ?", (category_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE budgets SET monthly_limit = ?, active = 1 WHERE id = ?", (float(monthly_limit), existing["id"]))
    else:
        cursor.execute("INSERT INTO budgets (category_id, monthly_limit, active) VALUES (?, ?, 1)", (category_id, float(monthly_limit)))
    connection.commit()
    connection.close()
