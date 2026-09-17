import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "financial_agent.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(profile):
    """Create the schema and persist configuration without deleting financial data."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            cursor.executescript(schema_file.read())

        profile_data = profile["profile"]
        cursor.execute(
            """
            INSERT INTO profile (id, name, currency, review_frequency)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                currency = excluded.currency,
                review_frequency = excluded.review_frequency
            """,
            (
                profile_data["name"],
                profile_data["currency"],
                profile_data["review_frequency"],
            ),
        )

        default_categories = [
            ("Housing", "expense"),
            ("Food", "expense"),
            ("Transport", "expense"),
            ("Health", "expense"),
            ("Education", "expense"),
            ("Leisure", "expense"),
            ("Other", "expense"),
        ]
        for category in profile["expenses"].get("categories", []):
            name = str(category).strip()
            if name:
                default_categories.append((name, "expense"))

        for name, category_type in default_categories:
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name, category_type) VALUES (?, ?)",
                (name, category_type),
            )

        preferences = profile["preferences"]
        cursor.execute(
            """
            INSERT INTO agent_settings (id, communication_style, detail_level, budget_alerts)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                communication_style = excluded.communication_style,
                detail_level = excluded.detail_level,
                budget_alerts = excluded.budget_alerts
            """,
            (
                preferences["communication_style"],
                preferences["detail_level"],
                int(preferences["budget_alerts"]),
            ),
        )

        snapshot = profile.get("initial_snapshot")
        if snapshot:
            cursor.execute(
                """
                INSERT INTO financial_snapshot
                    (id, monthly_income, monthly_expenses, estimated_balance, expense_commitment_percent)
                VALUES (1, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    monthly_income = excluded.monthly_income,
                    monthly_expenses = excluded.monthly_expenses,
                    estimated_balance = excluded.estimated_balance,
                    expense_commitment_percent = excluded.expense_commitment_percent
                """,
                (
                    snapshot["monthly_income_estimate"],
                    snapshot["monthly_expense_estimate"],
                    snapshot["estimated_balance"],
                    snapshot["expense_commitment_percent"],
                ),
            )

        cursor.execute("DELETE FROM financial_goals")
        for goal in profile.get("goals", []):
            name = str(goal).strip()
            if name:
                cursor.execute(
                    "INSERT INTO financial_goals (name) VALUES (?)",
                    (name,),
                )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
