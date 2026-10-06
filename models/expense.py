class Expense:

    def __init__(self, expense_id, amount, category, description, date):
        self.id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date