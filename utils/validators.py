import math
from datetime import datetime

from utils.constants import CATEGORIES, DATE_FORMAT, MONTH_FORMAT


# ==================================================
#                  VALIDATE AMOUNT
# ==================================================

def validate_amount(amount):

    # nan and inf are valid floats in Python, but not valid money
    if not math.isfinite(amount):

        raise ValueError("Amount must be a real number.")

    if amount <= 0:

        raise ValueError("Amount must be greater than zero.")


# ==================================================
#                 VALIDATE CATEGORY
# ==================================================

def validate_category(category):

    if category.title() not in CATEGORIES:

        raise ValueError(
            "Invalid category. Choose from "
            + ", ".join(CATEGORIES[:-1])
            + ", or "
            + CATEGORIES[-1]
            + "."
        )


# ==================================================
#                 VALIDATE DESCRIPTION
# ==================================================

def validate_description(description):

    if not description.strip():

        raise ValueError(
            "Description cannot be empty."
        )


# ==================================================
#                    VALIDATE DATE
# ==================================================

def validate_date(date):

    try:

        datetime.strptime(
            date,
            DATE_FORMAT
        )

    except ValueError:

        raise ValueError(
            "Date must be in DD-MM-YYYY format."
        )


# ==================================================
#               VALIDATE DATE RANGE
# ==================================================

def validate_date_range(start_date, end_date):

    validate_date(start_date)
    validate_date(end_date)

    start = datetime.strptime(
        start_date,
        DATE_FORMAT
    )

    end = datetime.strptime(
        end_date,
        DATE_FORMAT
    )

    if start > end:

        raise ValueError(
            "Start date cannot be after end date."
        )


# ==================================================
#                  VALIDATE MONTH
# ==================================================

def validate_month(month):

    try:

        datetime.strptime(
            month,
            MONTH_FORMAT
        )

    except ValueError:

        raise ValueError(
            "Month must be in MM-YYYY format."
        )
