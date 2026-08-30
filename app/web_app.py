from flask import Flask, jsonify, request, send_from_directory
from database.connection import initialize_database
from agent.config_builder import build_agent_config
from agent.prompt_builder import build_agent_prompt
from services.financial_profile_service import calculate_initial_snapshot
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

application = Flask(__name__, static_folder=WEB_DIR)

@application.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@application.get("/web/<path:filename>")
def web_files(filename):
    return send_from_directory(WEB_DIR, filename)

@application.post("/api/build-profile")
def build_profile():
    data = request.get_json(silent=True) or {}

    profile = {
        "profile": {
            "name": data.get("name", "User"),
            "currency": data.get("currency", "BRL"),
            "review_frequency": data.get("frequency", "Monthly")
        },
        "income": {
            "monthly_average": float(data.get("income", 0)),
            "type": data.get("incomeType", "Fixed"),
            "additional_monthly_average": float(data.get("extra", 0))
        },
        "expenses": {
            "fixed_monthly_average": float(data.get("fixed", 0)),
            "variable_monthly_average": float(data.get("variable", 0)),
            "categories": data.get("categories", ["Housing", "Food", "Transport"])
        },
        "debts": {
            "has_debt": float(data.get("debt", 0)) > 0,
            "monthly_commitment": float(data.get("debt", 0))
        },
        "goals": [data.get("goals", "Financial organization")],
        "preferences": {
            "communication_style": data.get("style", "Simple"),
            "detail_level": "Basic",
            "budget_alerts": data.get("alerts", False)
        }
    }

    snapshot = calculate_initial_snapshot(profile)
    profile["initial_snapshot"] = snapshot

    initialize_database(profile)
    config = build_agent_config(profile)
    prompt = build_agent_prompt(profile, config)

    return jsonify({
        "profile": profile,
        "snapshot": snapshot,
        "agent_config": config,
        "agent_instructions": prompt
    })

if __name__ == "__main__":
    application.run(debug=True)
