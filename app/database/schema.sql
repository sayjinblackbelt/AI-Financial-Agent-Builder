CREATE TABLE profile (
    id INTEGER PRIMARY KEY,
    name TEXT,
    currency TEXT,
    review_frequency TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT,
    description TEXT,
    category_id INTEGER,
    amount REAL,
    transaction_type TEXT
);

CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    monthly_limit REAL
);

CREATE TABLE financial_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    target_amount REAL,
    target_date TEXT
);

CREATE TABLE agent_settings (
    id INTEGER PRIMARY KEY,
    communication_style TEXT,
    detail_level TEXT,
    budget_alerts INTEGER
);
