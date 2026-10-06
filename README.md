# Personal Expense Tracker

A menu-driven console application written in **pure Python 3** (standard library only).
It records personal expenses, saves them permanently in a JSON file, shows reports and
statistics, and exports data to CSV.

## Requirements

- Python 3.8 or newer
- No extra packages to install

## How to run

Open a terminal in the project folder and run:

```
python main.py
```

(On some systems use `python main.py`.) The program finds its data and export
folders automatically, so it also works if you start it from another folder.

## Menu options

| Option | What it does |
|---|---|
| 1 | Add a new expense (amount, category, description, date) |
| 2 | View all expenses (sorted by date) |
| 3 | Filter expenses by category |
| 4 | Filter expenses by date range (DD-MM-YYYY to DD-MM-YYYY) |
| 5 | View total spending |
| 6 | Monthly summary report (enter MM-YYYY) |
| 7 | Edit an expense (press Enter to keep a value) |
| 8 | Delete an expense (asks for confirmation) |
| 9 | Spending statistics: totals, average, highest, lowest, category breakdown |
| 10 | Export all expenses to `exports/expenses.csv` |
| 11 | Export one month to `exports/expenses_MM_YYYY.csv` |
| 0 | Exit |

Allowed categories: Food, Travel, Shopping, Bills, Entertainment, Health, Education, Other.

## Run the tests

```
python -m unittest discover -s tests -t . -v
```

The tests cover the service layer (add, edit, delete, totals, statistics, monthly and
date-range filters, CSV export), the JSON repository (including damaged-file recovery)
and the validators.

## Project structure

```
PersonalExpenseTracker/
├── main.py                      Menu and user interaction (UI layer)
├── README.md
├── data/expenses.json           Saved expenses
├── exports/                     Generated CSV files
├── models/expense.py            Expense class (one expense)
├── repositories/
│   ├── expense_repository.py        Abstract interface: save() and load()
│   └── json_expense_repository.py   JSON file storage
├── services/expense_service.py  Business logic (totals, filters, exports)
├── tests/                       Automated unit tests
└── utils/
    ├── constants.py             Currency symbol, date format, categories
    ├── helpers.py               Display and formatting helpers
    └── validators.py            Input validation
```

Layers talk only downward: `main.py` -> `ExpenseService` -> `ExpenseRepository` -> JSON file.
Because the service depends only on the repository interface, the JSON storage could be
replaced by a database without changing the service or the menu.

## Data safety

- The data file is saved safely: a temporary file is written first and then swapped in.
- If `expenses.json` is damaged, the program does **not** overwrite it. It saves a copy
  named like `expenses.json.damaged_YYYYMMDD_HHMMSS.bak`, warns you at start-up, and
  starts with an empty list.

## Customising

Edit `utils/constants.py` to change the currency symbol (for example `"Rs."`), the date
format or the list of categories.

## Starting fresh

To remove the sample data, replace the contents of `data/expenses.json` with `[]`.
