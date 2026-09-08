# AI Financial Agent Builder

> A guided, local-first application that transforms financial preferences into a structured configuration for a future personal financial assistant.

## Overview

The MVP collects financial preferences, builds a structured profile, persists data locally with SQLite, and generates agent configuration and prompt parameters.

## Core flow

`Guided Questions → Financial Profile → SQLite → Agent Configuration → Future AI Assistant`

## Features

- Guided financial onboarding
- Structured financial profile
- Local SQLite persistence
- Income, expense, budget and goal foundations
- Agent rules and prompt generation
- Budget alerts and financial insights
- Monthly trend analysis
- Flask API and browser interface
- Privacy-first, local-first design

## Privacy and safety

This project is not a banking or investment execution platform. It does not request banking credentials, execute financial transactions, or make autonomous investment decisions. AI integration is optional.

## Run locally

```bash
pip install -r requirements.txt
cd app
python web_app.py
```

Then open the local address shown by Flask.

## Tests

```bash
pytest
```

## CI

GitHub Actions validates Python syntax, Ruff quality checks, the automated test suite, and a Flask smoke test on pushes and pull requests to `main`.

## Roadmap

- **0.1** Builder MVP
- **0.2** Financial control
- **0.3** Intelligence layer
- **0.4** Conversational AI agent

## Author

**Filipe G Morais**

GitHub: https://github.com/sayjinblackbelt  
Repository: https://github.com/sayjinblackbelt/AI-Financial-Agent-Builder
