import sqlite3

DATABASE_NAME = "financial_agent.db"

def initialize_database(profile):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            currency TEXT,
            review_frequency TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_settings (
            id INTEGER PRIMARY KEY,
            communication_style TEXT,
            detail_level TEXT,
            budget_alerts INTEGER
        )
    """)

    cursor.execute("DELETE FROM profile")
    cursor.execute(
        "INSERT INTO profile VALUES (1, ?, ?, ?)",
        (
            profile["profile"]["name"],
            profile["profile"]["currency"],
            profile["profile"]["review_frequency"]
        )
    )

    cursor.execute("DELETE FROM categories")
    for category in profile["expenses"]["categories"]:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (category,)
        )

    cursor.execute("DELETE FROM agent_settings")
    preferences = profile["preferences"]
    cursor.execute(
        "INSERT INTO agent_settings VALUES (1, ?, ?, ?)",
        (
            preferences["communication_style"],
            preferences["detail_level"],
            int(preferences["budget_alerts"])
        )
    )

    connection.commit()
    connection.close()
