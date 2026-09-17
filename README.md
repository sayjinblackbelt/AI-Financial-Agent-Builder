# AI Financial Agent Builder

> A local-first application that turns a user's financial profile and registered transactions into structured financial analysis and a foundation for a future conversational AI assistant.

## 🎯 Project purpose

AI Financial Agent Builder is a portfolio project focused on **financial organization, data analysis and agent architecture**. It is not a banking application, investment platform or automatic transaction system.

The current MVP provides:

1. Guided financial onboarding.
2. Structured financial profile generation.
3. Local SQLite persistence.
4. Transaction and category management.
5. Category budgets and alerts.
6. Monthly summaries and month-over-month comparison.
7. Rule-based financial insights and narrative.
8. Agent configuration and prompt generation.
9. Flask API + browser dashboard.

## 🔄 Core flow

```text
Guided Onboarding
      ↓
Financial Profile
      ↓
Flask API
      ↓
SQLite
      ↓
Financial Analyzer
      ↓
Insights / Alerts / Trends
      ↓
Agent Configuration + Prompt
      ↓
Future Conversational AI
```

## 🧱 Architecture

```text
app/
├── agent/
│   ├── config_builder.py
│   └── prompt_builder.py
├── database/
│   ├── connection.py
│   ├── schema.sql
│   └── financial_agent.db
├── models/
│   └── financial_profile.py
├── onboarding/
│   ├── questions.py
│   └── profile_builder.py
├── services/
│   ├── budget_service.py
│   ├── financial_analyzer.py
│   ├── financial_insights.py
│   ├── financial_profile_service.py
│   └── transaction_service.py
├── main.py
└── web_app.py

web/
├── app.js
└── styles.css

index.html
requirements.txt
tests/
```

### Data model

```text
profile
categories
transactions
budgets
financial_goals
agent_settings
financial_snapshot
```

The database is **local-first**. Re-running the profile builder updates configuration while preserving registered transactions and budgets.

## 🧠 Intelligence layer

The analyzer currently works deterministically from SQLite data. It calculates:

- current-month income, expenses and balance;
- top expense categories;
- budget utilization and alerts;
- current vs. previous month;
- expense and balance trends;
- rule-based financial insights.

The future AI layer should interpret these structured results rather than replacing deterministic financial calculations.

## 🤖 Agent configuration

The builder generates:

- user financial context;
- categories and goals;
- monitoring rules;
- alert thresholds;
- communication preferences;
- explicit safety restrictions.

Current restrictions include:

- no financial transaction execution;
- no banking credentials;
- no autonomous investment decisions;
- clarification when financial data is incomplete.

## 🧪 Testing

The repository includes automated tests for database flows, transactions, budgets, monthly history, analyzer contracts, insights, prompt generation and Flask API integration.

Run locally with:

```bash
pip install -r requirements.txt
pip install pytest ruff
PYTHONPATH=app pytest -q
```

Quality checks used by CI:

```bash
python -m compileall -q app tests
ruff check app tests --ignore DTZ011
PYTHONPATH=app pytest -q
```

## 🚀 Run locally

```bash
pip install -r requirements.txt
cd app
python web_app.py
```

Then open the local address shown by Flask.

> The current application requires the Flask backend for the complete experience, because onboarding, persistence and analysis use the Python API and SQLite database.

## 🗺️ Roadmap

### v0.1 — Builder
- Guided questions
- Financial profile
- Agent configuration

### v0.2 — Financial control
- Transactions
- Categories
- Budgets
- Monthly summaries

### v0.3 — Intelligence layer **← current MVP**
- Financial analysis
- Alerts
- Month comparison
- Trend detection
- Rule-based insights
- Flask dashboard
- Automated tests

### v0.4 — Conversational agent
- Natural-language questions
- Context-aware analysis
- Natural-language transaction input
- Agent configuration integration

### v1.0 — Demonstrable portfolio product
- Import/export
- Reports
- Deployment
- Documentation and product demonstration

## 🔒 Privacy principles

- Local-first by default.
- No banking credentials.
- No automatic financial transactions.
- No autonomous investment decisions.
- AI integration should be optional.

## Status

🟡 **MVP v0.3 — technical validation in progress.**

The core application, persistence layer, analysis layer, dashboard and automated test suite are implemented. The next validation step is executing the complete suite and browser/API flow in a real development environment.

## 👤 Author

**Filipe G Morais**

GitHub: https://github.com/sayjinblackbelt  
Repository: https://github.com/sayjinblackbelt/AI-Financial-Agent-Builder
