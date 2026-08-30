# AI Financial Agent Builder

> A guided application that transforms a user's financial preferences into a personalized, local-first financial assistant configuration.

## 🎯 Project purpose

AI Financial Agent Builder is not initially designed as a banking application or investment platform.

The MVP focuses on a guided onboarding process that:

1. Collects basic financial preferences.
2. Creates a structured financial profile.
3. Initializes a local SQLite database.
4. Defines categories, budgets and goals.
5. Generates agent rules and configuration parameters.
6. Prepares the foundation for a future conversational AI financial assistant.

## 🔄 Core flow

```
Guided Questions
      ↓
Financial Profile
      ↓
Structured JSON
      ↓
Local SQLite Database
      ↓
Agent Configuration
      ↓
Future AI Financial Assistant
```

## 🧭 MVP onboarding

### 1. Basic profile
- Preferred name
- Currency
- Financial control frequency

### 2. Income
- Monthly income
- Income type: fixed, variable or mixed
- Additional income sources

### 3. Expenses
- Main fixed expenses
- Main variable expenses
- Categories to track

### 4. Debts and commitments
- Has debts?
- Monthly debt commitments
- Priority for debt monitoring

### 5. Goals
- Emergency reserve
- Debt reduction
- Savings goal
- Purchase goal
- Other custom goal

### 6. Agent behavior
- Communication style
- Detail level
- Alert preferences
- Budget monitoring
- Monthly comparison
- Trend detection

## 🗄️ Initial data model

```
profile
categories
transactions
budgets
financial_goals
agent_settings
financial_snapshot
```

## 🤖 Agent configuration

The builder will generate a structured configuration containing:

- User financial profile
- Categories
- Goals
- Monitoring rules
- Alert thresholds
- Communication preferences
- Agent restrictions

Example:

```json
{
  "agent_name": "Personal Financial Assistant",
  "mode": "local-first",
  "goals": [
    "control expenses",
    "monitor budget",
    "identify spending trends"
  ],
  "alerts": {
    "budget_warning_percent": 80
  },
  "restrictions": [
    "Do not execute financial transactions",
    "Do not request banking credentials",
    "Do not make autonomous investment decisions"
  ]
}
```

## 🛠️ Proposed architecture

```
app/
├── main.py
├── onboarding/
│   ├── questions.py
│   └── profile_builder.py
├── database/
│   ├── connection.py
│   ├── schema.sql
│   └── repositories.py
├── agent/
│   ├── config_builder.py
│   └── prompt_builder.py
├── services/
│   └── financial_profile_service.py
└── models/
    └── financial_profile.py
```

## 🚀 Development roadmap

### Version 0.1 — Builder MVP
- Guided questions
- Financial profile
- JSON export
- SQLite initialization
- Agent configuration generation

### Version 0.2 — Financial control
- Income and expense records
- Categories
- Budgets
- Monthly summaries

### Version 0.3 — Intelligence layer
- Data interpretation
- Trend detection
- Budget alerts
- Personalized recommendations

### Version 0.4 — AI agent
- Conversational interface
- Natural language transaction input
- Context-aware analysis
- Agent configuration integration

## 🔒 Privacy principles

- Local-first by default
- No banking credentials
- No automatic financial transactions
- User controls stored data
- AI integration should be optional

## Status

🟢 MVP in active development — onboarding, local SQLite persistence, transactions, budgets, alerts, insights and monthly trend analysis are implemented.


## 🌐 Web + Python integration

The project now has a Flask API layer connecting the browser onboarding to the Python application logic.

```
Web Interface
     ↓ POST /api/build-profile
Flask API
     ↓
Financial Profile Service
     ↓
SQLite
     ↓
Agent Configuration
     ↓
Prompt Builder
```

### Run locally

```bash
pip install -r requirements.txt
cd app
python web_app.py
```

Then open the local address shown by Flask.

> The browser prototype can still run independently as a static demonstration. The Flask version is the path for persistence and full backend integration.
