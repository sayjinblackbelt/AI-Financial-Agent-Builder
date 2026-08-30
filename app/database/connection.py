import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "financial_agent.db")

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def initialize_database(profile):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        currency TEXT NOT NULL,
        review_frequency TEXT NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS agent_settings (
        id INTEGER PRIMARY KEY,
        communication_style TEXT NOT NULL,
        detail_level TEXT NOT NULL,
        budget_alerts INTEGER NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS financial_snapshot (
        id INTEGER PRIMARY KEY,
        monthly_income REAL,
        monthly_expenses REAL,
        estimated_balance REAL,
        expense_commitment_percent REAL
    )""")

    cursor.execute("DELETE FROM profile")
    cursor.execute("INSERT INTO profile VALUES (1, ?, ?, ?)", (
        profile["profile"]["name"], profile["profile"]["currency"],
        profile["profile"]["review_frequency"]
    ))

    cursor.execute("DELETE FROM categories")
    for category in profile["expenses"]["categories"]:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))

    preferences = profile["preferences"]
    cursor.execute("DELETE FROM agent_settings")
    cursor.execute("INSERT INTO agent_settings VALUES (1, ?, ?, ?)", (
        preferences["communication_style"], preferences["detail_level"],
        int(preferences["budget_alerts"])
    ))

    snapshot = profile.get("initial_snapshot")
    if snapshot:
        cursor.execute("DELETE FROM financial_snapshot")
        cursor.execute("INSERT INTO financial_snapshot VALUES (1, ?, ?, ?, ?)", (
            snapshot["monthly_income_estimate"],
            snapshot["monthly_expense_estimate"],
            snapshot["estimated_balance"],
            snapshot["expense_commitment_percent"]
        ))

    connection.commit()
    connection.close()
