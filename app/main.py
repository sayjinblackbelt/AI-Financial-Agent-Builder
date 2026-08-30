from onboarding.profile_builder import build_financial_profile
from database.connection import initialize_database
from agent.config_builder import build_agent_config
from agent.prompt_builder import build_agent_prompt
from services.financial_profile_service import calculate_initial_snapshot
import json

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def main():
    print("=" * 55)
    print("AI FINANCIAL AGENT BUILDER")
    print("Guided Financial Profile Setup")
    print("=" * 55)

    profile = build_financial_profile()
    snapshot = calculate_initial_snapshot(profile)

    profile["initial_snapshot"] = snapshot

    initialize_database(profile)
    config = build_agent_config(profile)
    prompt = build_agent_prompt(profile, config)

    save_json("financial_profile.json", profile)
    save_json("agent_config.json", config)

    with open("agent_instructions.md", "w", encoding="utf-8") as file:
        file.write(prompt)

    print("\nSetup completed successfully.")
    print("\nInitial financial snapshot:")
    print(f"Estimated monthly income: {snapshot['monthly_income_estimate']:.2f}")
    print(f"Estimated monthly expenses: {snapshot['monthly_expense_estimate']:.2f}")
    print(f"Estimated balance: {snapshot['estimated_balance']:.2f}")

    if snapshot["expense_commitment_percent"] is not None:
        print(f"Expense commitment: {snapshot['expense_commitment_percent']:.2f}%")

    print("\nFiles generated:")
    print("- financial_profile.json")
    print("- agent_config.json")
    print("- agent_instructions.md")
    print("- financial_agent.db")

if __name__ == "__main__":
    main()
