from datetime import datetime
import uuid

from utils.constants import CURRENCY_SYMBOL, DATE_FORMAT, MONTH_FORMAT


# ==================================================
#                  DISPLAY LINE
# ==================================================

def print_line(length=50):
    print("=" * length)


# ==================================================
#                  DISPLAY HEADER
# ==================================================

def print_header(title):

    print()
    print_line()
    print(title.center(50))
    print_line()


# ==================================================
#                  PAUSE PROGRAM
# ==================================================

def pause():

    input("\nPress Enter to return to main menu...")


# ==================================================
#               GENERATE EXPENSE ID
# ==================================================

def generate_expense_id():

    return str(uuid.uuid4())[:8]


# ==================================================
#                  TODAY'S DATE
# ==================================================

def get_today_date():

    return datetime.now().strftime(DATE_FORMAT)


# ==================================================
#                 NORMALISE MONTH
# ==================================================

def normalize_month(month):

    # "1-2026" becomes "01-2026" so it matches stored dates
    return datetime.strptime(
        month,
        MONTH_FORMAT
    ).strftime(MONTH_FORMAT)


# ==================================================
#              FORMAT CURRENCY
# ==================================================

def format_currency(amount):

    return f"{CURRENCY_SYMBOL}{amount:.2f}"


# ==================================================
#             FORMAT EXPENSE FOR TABLE
# ==================================================

def format_expense(expense):

    return (
        f"{expense.id:<10} | "
        f"{expense.date:<12} | "
        f"{expense.category:<18} | "
        f"{expense.amount:<12.2f} | "
        f"{expense.description}"
    )


# ==================================================
#                  PRINT TABLE
# ==================================================
# One function used by every screen that lists expenses.

def print_table(expenses):

    amount_title = f"Amount ({CURRENCY_SYMBOL})"

    print()

    print(
        f"{'ID':<10} | "
        f"{'Date':<12} | "
        f"{'Category':<18} | "
        f"{amount_title:<12} | "
        f"Description"
    )

    print("-" * 80)

    for expense in expenses:

        print(format_expense(expense))

    print("-" * 80)
