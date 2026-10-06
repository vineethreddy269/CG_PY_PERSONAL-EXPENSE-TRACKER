import os

from models.expense import Expense

from services.expense_service import ExpenseService

from repositories.json_expense_repository import JsonExpenseRepository

from utils.constants import CURRENCY_SYMBOL, CATEGORIES

from utils.validators import (
    validate_amount,
    validate_category,
    validate_description,
    validate_date,
    validate_date_range,
    validate_month
)

from utils.helpers import (
    print_line,
    print_header,
    print_table,
    pause,
    generate_expense_id,
    get_today_date,
    normalize_month,
    format_currency
)


# ==================================================
#                  APPLICATION SETUP
# ==================================================

# Paths are built from the location of this file, so the
# program works no matter which folder you start it from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "data", "expenses.json")

EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")

repository = JsonExpenseRepository(DATA_FILE)

service = ExpenseService(repository, EXPORT_FOLDER)


# ==================================================
#                  DISPLAY MENU
# ==================================================

def show_menu():

    print()
    print_line()

    print("             PERSONAL EXPENSE TRACKER")

    print_line()

    print("  [1]  Add New Expense")
    print("  [2]  View All Expenses")
    print("  [3]  Filter Expenses by Category")
    print("  [4]  Filter Expenses by Date Range")
    print("  [5]  View Total Spending")
    print("  [6]  Monthly Summary Report")
    print("  [7]  Edit Expense")
    print("  [8]  Delete Expense")
    print("  [9]  Spending Statistics")
    print("  [10] Export Expenses to CSV")
    print("  [11] Export Monthly Expenses to CSV")
    print("  [0]  Exit Application")

    print_line()


# ==================================================
#            REUSABLE INPUT PROMPTS
# ==================================================
# Used by BOTH "Add Expense" and "Edit Expense".
# When "current" is given, pressing Enter keeps it.

def prompt_amount(current=None):

    while True:

        hint = f" [{current:.2f}]" if current is not None else ""

        raw = input(
            f"Enter Amount ({CURRENCY_SYMBOL}){hint}: "
        ).strip()

        if raw == "" and current is not None:

            return current

        try:

            amount = float(raw)

        except ValueError:

            print("❌ Amount must be a number.")

            continue

        try:

            validate_amount(amount)

        except ValueError as error:

            print(f"❌ {error}")

            continue

        return round(amount, 2)


def prompt_category(current=None):

    print(f"Categories: {', '.join(CATEGORIES)}")

    while True:

        hint = f" [{current}]" if current else ""

        category = input(
            f"Enter Category{hint}: "
        ).strip()

        if category == "" and current:

            return current

        try:

            validate_category(category)

            return category.title()

        except ValueError as error:

            print(f"❌ {error}")


def prompt_description(current=None):

    while True:

        hint = f" [{current}]" if current else ""

        description = input(
            f"Enter Description{hint}: "
        ).strip()

        if description == "" and current:

            return current

        try:

            validate_description(description)

            return description

        except ValueError as error:

            print(f"❌ {error}")


def prompt_date(default):

    while True:

        date = input(
            f"Enter Date DD-MM-YYYY "
            f"(Press Enter for {default}): "
        ).strip()

        if date == "":

            date = default

        try:

            validate_date(date)

            return date

        except ValueError as error:

            print(f"❌ {error}")


# ==================================================
#                  ADD EXPENSE
# ==================================================

def add_expense():

    print_header("ADD NEW EXPENSE")

    amount = prompt_amount()

    category = prompt_category()

    description = prompt_description()

    date = prompt_date(get_today_date())

    expense_id = generate_expense_id()

    expense = Expense(
        expense_id,
        amount,
        category,
        description,
        date
    )

    service.add_expense(expense)

    print()

    print(
        f"✅ Expense added successfully! "
        f"[ID: {expense_id}]"
    )

    pause()


# ==================================================
#                  VIEW ALL EXPENSES
# ==================================================

def view_all_expenses():

    print_header("ALL EXPENSES")

    expenses = service.get_sorted_expenses()

    if not expenses:

        print("\nNo expenses found.")

        pause()

        return

    print_table(expenses)

    total = service.get_total_spending()

    print(
        f" Total Count: {len(expenses)} item(s)"
    )

    print(
        f" Overall Spending: {format_currency(total)}"
    )

    pause()


# ==================================================
#              FILTER BY CATEGORY
# ==================================================

def filter_by_category():

    print_header("FILTER BY CATEGORY")

    category = input(
        "Enter category: "
    ).strip()

    expenses = service.filter_by_category(
        category
    )

    if not expenses:

        print(
            f"\n❌ No expenses found for "
            f"'{category}'."
        )

        pause()

        return

    print_table(expenses)

    total = sum(expense.amount for expense in expenses)

    print(
        f" Category: {category.title()}"
    )

    print(
        f" Total Spending: {format_currency(total)}"
    )

    pause()


# ==================================================
#              FILTER BY DATE RANGE
# ==================================================

def filter_by_date_range():

    print_header("FILTER BY DATE RANGE")

    start_date = input(
        "Enter Start Date (DD-MM-YYYY): "
    ).strip()

    end_date = input(
        "Enter End Date   (DD-MM-YYYY): "
    ).strip()

    try:

        validate_date_range(start_date, end_date)

    except ValueError as error:

        print(f"\n❌ {error}")

        pause()

        return

    expenses = service.filter_by_date_range(
        start_date,
        end_date
    )

    if not expenses:

        print(
            f"\n❌ No expenses found between "
            f"{start_date} and {end_date}."
        )

        pause()

        return

    print_table(expenses)

    total = sum(expense.amount for expense in expenses)

    print(
        f" Period: {start_date} to {end_date}"
    )

    print(
        f" Total Expenses: {len(expenses)}"
    )

    print(
        f" Total Spending: {format_currency(total)}"
    )

    pause()


# ==================================================
#                TOTAL SPENDING
# ==================================================

def view_total_spending():

    print_header("TOTAL SPENDING")

    total = service.get_total_spending()

    print()

    print(
        f"💰 Overall Spending: "
        f"{format_currency(total)}"
    )

    pause()


# ==================================================
#                MONTHLY SUMMARY
# ==================================================

def monthly_summary():

    print_header("MONTHLY SUMMARY REPORT")

    month = input(
        "Enter Month (MM-YYYY): "
    ).strip()

    try:

        validate_month(month)

    except ValueError as error:

        print(f"\n❌ {error}")

        pause()

        return

    month = normalize_month(month)

    expenses = service.get_monthly_expenses(
        month
    )

    if not expenses:

        print(
            f"\n❌ No expenses found for "
            f"{month}."
        )

        pause()

        return

    print_table(expenses)

    total = service.get_monthly_total(
        month
    )

    print(
        f" Month: {month}"
    )

    print(
        f" Total Expenses: {len(expenses)}"
    )

    print(
        f" Total Spending: "
        f"{format_currency(total)}"
    )

    pause()


# ==================================================
#                  EDIT EXPENSE
# ==================================================

def edit_expense():

    print_header("EDIT EXPENSE")

    expense_id = input(
        "Enter Expense ID: "
    ).strip()

    expense = service.get_expense_by_id(
        expense_id
    )

    if expense is None:

        print(
            "\n❌ Expense not found."
        )

        pause()

        return

    print("\nCurrent details:")

    print_table([expense])

    print(
        "Press Enter to keep the current value.\n"
    )

    amount = prompt_amount(expense.amount)

    category = prompt_category(expense.category)

    description = prompt_description(expense.description)

    date = prompt_date(expense.date)

    service.update_expense(
        expense_id,
        amount,
        category,
        description,
        date
    )

    print(
        "\n✅ Expense updated successfully!"
    )

    pause()


# ==================================================
#                  DELETE EXPENSE
# ==================================================

def delete_expense():

    print_header("DELETE EXPENSE")

    expense_id = input(
        "Enter Expense ID: "
    ).strip()

    expense = service.get_expense_by_id(
        expense_id
    )

    if expense is None:

        print(
            "\n❌ Expense not found."
        )

        pause()

        return

    print()

    print(
        f"ID:          {expense.id}"
    )

    print(
        f"Date:        {expense.date}"
    )

    print(
        f"Category:    {expense.category}"
    )

    print(
        f"Amount:      {format_currency(expense.amount)}"
    )

    print(
        f"Description: {expense.description}"
    )

    print()

    confirmation = input(
        "Are you sure you want to delete "
        "this expense? (y/n): "
    ).strip().lower()

    if confirmation == "y":

        success = service.delete_expense(
            expense_id
        )

        if success:

            print(
                "\n✅ Expense deleted successfully!"
            )

        else:

            print(
                "\n❌ Unable to delete expense."
            )

    else:

        print(
            "\nDelete operation cancelled."
        )

    pause()


# ==================================================
#                  STATISTICS
# ==================================================

def show_statistics():

    print_header("SPENDING STATISTICS")

    expenses = service.get_all_expenses()

    if not expenses:

        print("\nNo expenses found.")

        pause()

        return

    total = service.get_total_spending()

    average = service.get_average_expense()

    highest = service.get_highest_expense()

    lowest = service.get_lowest_expense()

    print()

    print(f" Number of expenses : {len(expenses)}")

    print(f" Total spending     : {format_currency(total)}")

    print(f" Average expense    : {format_currency(average)}")

    print(
        f" Highest expense    : "
        f"{format_currency(highest.amount)} "
        f"({highest.description}, {highest.date})"
    )

    print(
        f" Lowest expense     : "
        f"{format_currency(lowest.amount)} "
        f"({lowest.description}, {lowest.date})"
    )

    print()

    print(" Spending by category")

    print(" " + "-" * 60)

    category_totals = service.get_category_totals()

    # Largest category first
    ordered = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for category, amount in ordered:

        percent = amount / total * 100

        bar = "█" * int(percent / 5)

        print(
            f" {category:<14} "
            f"{format_currency(amount):>11} "
            f"{percent:5.1f}%  {bar}"
        )

    pause()


# ==================================================
#                EXPORT ALL TO CSV
# ==================================================

def export_expenses_to_csv():

    print_header("EXPORT EXPENSES TO CSV")

    try:

        file_path = service.export_to_csv()

        print(
            "\n✅ Expenses exported successfully!"
        )

        print(
            f"CSV file: {file_path}"
        )

    except Exception as error:

        print(
            f"\n❌ Error exporting expenses: {error}"
        )

    pause()


# ==================================================
#             EXPORT MONTHLY TO CSV
# ==================================================

def export_monthly_expenses_to_csv():

    print_header("EXPORT MONTHLY EXPENSES TO CSV")

    try:

        month = int(
            input(
                "Enter month (1-12): "
            ).strip()
        )

        year = int(
            input(
                "Enter year (YYYY): "
            ).strip()
        )

        if month < 1 or month > 12:

            print(
                "\n❌ Invalid month. "
                "Please enter a value between 1 and 12."
            )

            pause()

            return

        file_path, count = (
            service.export_monthly_to_csv(
                month,
                year
            )
        )

        if count == 0:

            print(
                f"\n❌ No expenses found "
                f"for {month:02d}-{year}."
            )

        else:

            print(
                "\n✅ Monthly expenses "
                "exported successfully!"
            )

            print(
                f"Expenses exported: {count}"
            )

            print(
                f"CSV file: {file_path}"
            )

    except ValueError:

        print(
            "\n❌ Please enter a valid "
            "month and year."
        )

    except Exception as error:

        print(
            f"\n❌ Error exporting monthly expenses: "
            f"{error}"
        )

    pause()


# ==================================================
#                  MENU ROUTER
# ==================================================
# A dictionary maps each menu number to a function,
# which is shorter than a long if / elif chain.

ACTIONS = {
    "1": add_expense,
    "2": view_all_expenses,
    "3": filter_by_category,
    "4": filter_by_date_range,
    "5": view_total_spending,
    "6": monthly_summary,
    "7": edit_expense,
    "8": delete_expense,
    "9": show_statistics,
    "10": export_expenses_to_csv,
    "11": export_monthly_expenses_to_csv
}


# ==================================================
#                  MAIN FUNCTION
# ==================================================

def main():

    # Warn the user if the data file was damaged at start-up
    if repository.last_warning:

        print(f"\n⚠️  {repository.last_warning}")

    while True:

        show_menu()

        choice = input(
            "Select an option (0-11): "
        ).strip()

        if choice == "0":

            print()

            print_line()

            print(
                "       Thank you for using "
                "Personal Expense Tracker!"
            )

            print_line()

            break

        action = ACTIONS.get(choice)

        if action is None:

            print(
                "\n❌ Invalid option. "
                "Please select 0-11."
            )

            pause()

        else:

            action()


# ==================================================
#                  START PROGRAM
# ==================================================

if __name__ == "__main__":

    main()
