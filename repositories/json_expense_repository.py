import json
import os
import shutil
from datetime import datetime

from repositories.expense_repository import ExpenseRepository
from models.expense import Expense


class JsonExpenseRepository(ExpenseRepository):

    def __init__(self, file_path):

        self.file_path = file_path

        # Set by load() when a damaged file had to be backed up.
        # main.py shows this message to the user.
        self.last_warning = None


    # ==================================================
    #                      SAVE
    # ==================================================

    def save(self, expenses):

        data = []

        for expense in expenses:

            data.append({
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date
            })

        folder = os.path.dirname(self.file_path)

        if folder:

            os.makedirs(folder, exist_ok=True)

        # Safe save: write a temporary file first, then swap it in.
        # If the program stops half-way, the old file stays intact.
        temp_path = self.file_path + ".tmp"

        with open(temp_path, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4)

        os.replace(temp_path, self.file_path)


    # ==================================================
    #                      LOAD
    # ==================================================

    def load(self):

        self.last_warning = None

        # First run: no file yet, so start with an empty list
        if not os.path.exists(self.file_path):

            return []

        try:

            with open(self.file_path, "r", encoding="utf-8") as file:

                content = file.read()

            # An empty file is not damaged, it is just empty
            if not content.strip():

                return []

            data = json.loads(content)

            expenses = []

            for item in data:

                expense = Expense(
                    item["id"],
                    item["amount"],
                    item["category"],
                    item["description"],
                    item["date"]
                )

                expenses.append(expense)

            return expenses

        except (ValueError, KeyError, TypeError):

            # Damaged file: keep a copy BEFORE anything can overwrite it
            backup_path = self._backup_damaged_file()

            self.last_warning = (
                "The data file could not be read. "
                f"A backup copy was saved as: {backup_path}"
            )

            return []


    # ==================================================
    #              BACKUP DAMAGED FILE
    # ==================================================

    def _backup_damaged_file(self):

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_path = f"{self.file_path}.damaged_{stamp}.bak"

        shutil.copy2(self.file_path, backup_path)

        return backup_path
