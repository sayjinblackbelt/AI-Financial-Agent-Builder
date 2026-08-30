def ask_text(question, default=None):
    suffix = f" [{default}]" if default else ""
    value = input(f"{question}{suffix}: ").strip()
    return value or default or ""

def ask_number(question, default=0):
    while True:
        value = input(f"{question} [{default}]: ").strip().replace(",", ".")
        if not value:
            return default
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")

def choose_option(question, options):
    print(f"\n{question}")
    for index, option in enumerate(options, 1):
        print(f"{index}. {option}")

    while True:
        choice = input("Choose an option: ").strip()
        try:
            position = int(choice) - 1
            if 0 <= position < len(options):
                return options[position]
        except ValueError:
            pass
        print("Invalid option. Try again.")
