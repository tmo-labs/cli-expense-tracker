import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_expenses(expenses: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(expenses, indent=2), encoding="utf-8")


def add_expense(expenses: list[dict]) -> None:
    item = input("Item description: ").strip()
    if not item:
        print("Description cannot be empty.")
        return

    category = input("Category (Food/Transport/Data/Other): ").strip().title() or "Other"
    try:
        amount = float(input("Amount (KES): "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid number. Expense not saved.")
        return

    expenses.append({
        "item": item,
        "category": category,
        "amount": round(amount, 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_expenses(expenses)
    print(f"Saved: {item} ({category}) - KES {amount:,.2f}")


def show_summary(expenses: list[dict]) -> None:
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"\n--- Expense Summary ({len(expenses)} items) ---")
    for idx, e in enumerate(expenses, start=1):
        print(f"{idx}. [{e['date']}] {e['item']} ({e['category']}) -> KES {e['amount']:,.2f}")

    # Group totals by category
    categories = sorted({e["category"] for e in expenses})
    print("\n--- By Category ---")
    for cat in categories:
        cat_total = sum(e["amount"] for e in expenses if e["category"] == cat)
        print(f"• {cat}: KES {cat_total:,.2f}")

    print(f"\nTOTAL SPENT: KES {total:,.2f}\n")


def main() -> None:
    expenses = load_expenses()
    while True:
        print("\n=== tmo-labs Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Exit")
        choice = input("Choose (1-3): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_summary(expenses)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
                                                                           
