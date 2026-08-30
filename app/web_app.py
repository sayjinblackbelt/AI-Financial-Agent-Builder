from flask import Flask, jsonify, request, send_from_directory
from database.connection import initialize_database
from agent.config_builder import build_agent_config
from agent.prompt_builder import build_agent_prompt
from services.financial_profile_service import calculate_initial_snapshot
from services.transaction_service import add_transaction, get_monthly_summary
from services.financial_analyzer import analyze_finances
from services.budget_service import set_budget
from services.financial_insights import build_financial_insights, build_financial_narrative
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")
application = Flask(__name__)

def to_number(value):
    try:
        return float(str(value or 0).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0

@application.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@application.get("/web/<path:filename>")
def web_files(filename):
    return send_from_directory(WEB_DIR, filename)

@application.post("/api/build-profile")
def build_profile():
    data = request.get_json(silent=True) or {}
    currency = str(data.get("currency", "BRL"))[:3].upper()
    profile = {
        "profile":{"name":str(data.get("name") or "User").strip()[:100],"currency":currency if currency in {"BRL","USD","EUR"} else "BRL","review_frequency":str(data.get("frequency") or "Monthly")},
        "income":{"monthly_average":to_number(data.get("income")),"type":str(data.get("incomeType") or "Fixed"),"additional_monthly_average":to_number(data.get("extra"))},
        "expenses":{"fixed_monthly_average":to_number(data.get("fixed")),"variable_monthly_average":to_number(data.get("variable")),"categories":data.get("categories") or ["Housing","Food","Transport","Health","Education","Leisure"]},
        "debts":{"has_debt":to_number(data.get("debt"))>0,"monthly_commitment":to_number(data.get("debt"))},
        "goals":data.get("goals") if isinstance(data.get("goals"),list) else [str(data.get("goals") or "Financial organization")],
        "preferences":{"communication_style":str(data.get("style") or "Simple"),"detail_level":"Basic","budget_alerts":bool(data.get("alerts",False))}
    }
    snapshot=calculate_initial_snapshot(profile)
    profile["initial_snapshot"]=snapshot
    initialize_database(profile)
    config=build_agent_config(profile)
    return jsonify({"profile":profile,"snapshot":snapshot,"agent_config":config,"agent_instructions":build_agent_prompt(profile,config)})

@application.post("/api/transactions")
def create_transaction():
    data=request.get_json(silent=True) or {}
    description=str(data.get("description") or "").strip()
    amount=to_number(data.get("amount"))
    transaction_type=data.get("transaction_type")
    if not description or amount<=0 or transaction_type not in {"income","expense"}:
        return jsonify({"error":"Valid description, positive amount and transaction type are required."}),400
    transaction_id=add_transaction(description,amount,transaction_type,data.get("category"))
    return jsonify({"id":transaction_id,"summary":get_monthly_summary()}),201

@application.get("/api/summary")
def summary():
    return jsonify(get_monthly_summary())

@application.get("/api/analysis")
def analysis():
    return jsonify(analyze_finances())

@application.get("/api/insights")
def insights():
    return jsonify(build_financial_insights())

@application.get("/api/narrative")
def narrative():
    return jsonify({"narrative": build_financial_narrative()})

@application.post("/api/budgets")
def create_budget():
    data = request.get_json(silent=True) or {}
    category = str(data.get("category") or "").strip()
    limit = to_number(data.get("monthly_limit"))
    if not category or limit <= 0:
        return jsonify({"error": "Category and positive monthly limit are required."}), 400
    set_budget(category, limit)
    return jsonify({"message": "Budget saved.", "analysis": analyze_finances()}), 201

if __name__=="__main__":
    application.run(debug=True)
