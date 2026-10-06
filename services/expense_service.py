import csv
import os
from datetime import datetime

from utils.constants import DATE_FORMAT


class ExpenseService:

    def __init__(self, repository, export_folder="exports"):

        self.repository = repository
        self.export_folder = export_folder
        self.expenses = self.repository.load()


    # ==================================================
    #                  ADD EXPENSE
    # ==================================================

    def add_expense(self, expense):

        self.expenses.append(expense)

        self.repository.save(
            self.expenses
        )


    # ==================================================
    #              GET ALL EXPENSES
    # ==================================================

    def get_all_expenses(self):

        return self.expenses


    # ==================================================
    #           GET EXPENSES SORTED BY DATE
    # ==================================================

    def get_sorted_expenses(self):

        return self._sort_by_date(
            self.expenses
        )


    # ==================================================
    #        SORT ANY LIST OF EXPENSES BY DATE
    # ==================================================
    # Sorts real dates (not text), oldest first.

    def _sort_by_date(self, expenses):

        return sorted(
            expenses,
            key=lambda expense: datetime.strptime(
                expense.date,
                DATE_FORMAT
            )
        )


    # ==================================================
    #              GET EXPENSE BY ID
    # ==================================================

    def get_expense_by_id(self, expense_id):

        for expense in self.expenses:

            if expense.id == expense_id:

                return expense

        return None


    # ==================================================
    #                  DELETE EXPENSE
    # ==================================================

    def delete_expense(self, expense_id):

        expense = self.get_expense_by_id(
            expense_id
        )

        if expense is None:

            return False

        self.expenses.remove(expense)

        self.repository.save(
            self.expenses
        )

        return True


    # ==================================================
    #                  UPDATE EXPENSE
    # ==================================================

    def update_expense(
        self,
        expense_id,
        amount,
        category,
        description,
        date
    ):

        expense = self.get_expense_by_id(
            expense_id
        )

        if expense is None:

            return False

        expense.amount = amount
        expense.category = category
        expense.description = description
        expense.date = date

        self.repository.save(
            self.expenses
        )

        return True


    # ==================================================
    #              FILTER BY CATEGORY
    # ==================================================

    def filter_by_category(self, category):

        result = []

        for expense in self.expenses:

            if (
                expense.category.lower()
                == category.lower()
            ):

                result.append(expense)

        return self._sort_by_date(result)


    # ==================================================
    #              FILTER BY DATE RANGE
    # ==================================================
    # Dates are converted to real date objects before
    # comparing. Comparing the DD-MM-YYYY text directly
    # gives wrong answers across months and years.

    def filter_by_date_range(
        self,
        start_date,
        end_date
    ):

        start = datetime.strptime(
            start_date,
            DATE_FORMAT
        )

        end = datetime.strptime(
            end_date,
            DATE_FORMAT
        )

        result = []

        for expense in self.expenses:

            expense_date = datetime.strptime(
                expense.date,
                DATE_FORMAT
            )

            if start <= expense_date <= end:

                result.append(expense)

        return self._sort_by_date(result)


    # ==================================================
    #                TOTAL SPENDING
    # ==================================================

    def get_total_spending(self):

        total = 0

        for expense in self.expenses:

            total += expense.amount

        return total


    # ==================================================
    #              MONTHLY EXPENSES
    # ==================================================

    def get_monthly_expenses(self, month):

        result = []

        for expense in self.expenses:

            # "02-10-2026"[3:] gives "10-2026"
            if expense.date[3:] == month:

                result.append(expense)

        return self._sort_by_date(result)


    # ==================================================
    #                MONTHLY TOTAL
    # ==================================================

    def get_monthly_total(self, month):

        expenses = self.get_monthly_expenses(
            month
        )

        total = 0

        for expense in expenses:

            total += expense.amount

        return total


    # ==================================================
    #                CATEGORY TOTALS
    # ==================================================

    def get_category_totals(self):

        category_totals = {}

        for expense in self.expenses:

            category = expense.category

            if category not in category_totals:

                category_totals[category] = 0

            category_totals[category] += (
                expense.amount
            )

        return category_totals


    # ==================================================
    #                AVERAGE EXPENSE
    # ==================================================

    def get_average_expense(self):

        if not self.expenses:

            return 0

        return (
            self.get_total_spending()
            / len(self.expenses)
        )


    # ==================================================
    #                HIGHEST EXPENSE
    # ==================================================

    def get_highest_expense(self):

        if not self.expenses:

            return None

        return max(
            self.expenses,
            key=lambda expense: expense.amount
        )


    # ==================================================
    #                LOWEST EXPENSE
    # ==================================================

    def get_lowest_expense(self):

        if not self.expenses:

            return None

        return min(
            self.expenses,
            key=lambda expense: expense.amount
        )


    # ==================================================
    #            WRITE EXPENSES TO A CSV FILE
    # ==================================================
    # Shared by both export methods below.

    def _write_csv(self, file_path, expenses):

        os.makedirs(
            self.export_folder,
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # CSV Header
            writer.writerow([
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date"
            ])

            for expense in expenses:

                writer.writerow([
                    expense.id,
                    expense.amount,
                    expense.category,
                    expense.description,
                    expense.date
                ])


    # ==================================================
    #                EXPORT ALL TO CSV
    # ==================================================

    def export_to_csv(self):

        file_path = os.path.join(
            self.export_folder,
            "expenses.csv"
        )

        self._write_csv(
            file_path,
            self.expenses
        )

        return file_path


    # ==================================================
    #             EXPORT MONTHLY TO CSV
    # ==================================================

    def export_monthly_to_csv(
        self,
        month,
        year
    ):

        file_path = os.path.join(
            self.export_folder,
            f"expenses_{month:02d}_{year}.csv"
        )

        monthly_expenses = []

        # Find expenses for selected month/year
        for expense in self.expenses:

            expense_date = datetime.strptime(
                expense.date,
                DATE_FORMAT
            )

            if (
                expense_date.month == month
                and expense_date.year == year
            ):

                monthly_expenses.append(
                    expense
                )

        self._write_csv(
            file_path,
            monthly_expenses
        )

        return (
            file_path,
            len(monthly_expenses)
        )
