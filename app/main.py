from onboarding.profile_builder import build_financial_profile
from database.connection import initialize_database
from agent.config_builder import build_agent_config
import json

def main():
    print("=" * 55)
    print("AI FINANCIAL AGENT BUILDER")
    print("Guided Financial Profile Setup")
    print("=" * 55)

    profile = build_financial_profile()
    initialize_database(profile)
    config = build_agent_config(profile)

    with open("financial_profile.json", "w", encoding="utf-8") as file:
        json.dump(profile, file, ensure_ascii=False, indent=2)

    with open("agent_config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)

    print("\nSetup completed successfully.")
    print("Files generated:")
    print("- financial_profile.json")
    print("- agent_config.json")
    print("- financial_agent.db")

if __name__ == "__main__":
    main()
