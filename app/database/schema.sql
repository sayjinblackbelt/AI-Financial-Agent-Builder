CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    currency TEXT NOT NULL,
    review_frequency TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category_type TEXT DEFAULT 'expense'
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income','expense')),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL UNIQUE,
    monthly_limit REAL NOT NULL CHECK(monthly_limit > 0),
    active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS financial_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target_amount REAL,
    current_amount REAL DEFAULT 0,
    target_date TEXT,
    active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS agent_settings (
    id INTEGER PRIMARY KEY,
    communication_style TEXT NOT NULL,
    detail_level TEXT NOT NULL,
    budget_alerts INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS financial_snapshot (
    id INTEGER PRIMARY KEY,
    monthly_income REAL,
    monthly_expenses REAL,
    estimated_balance REAL,
    expense_commitment_percent REAL
);
