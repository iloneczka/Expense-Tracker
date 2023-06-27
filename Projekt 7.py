"""
A program that helps millions of Poles track their expenses and analyze them. The program allows for easy addition of new expenses and generation of reports. The application also works between runs by storing all data in a file. Each expense has an ID, description, and amount.

Usage: python3 <filename> <command>

Commands:
  add <amount> <description>    Add a new expense
  report                        Display all expenses and total
  export-python                 Export expenses as Python objects
  import-csv <csv_file>         Import expenses from a CSV file

"""

# python3 "/Users/ilo/Desktop/PYTHON/Praktyczny_python_M07/Projekt 7.py" <command>

import csv
import pickle
import sys
from typing import List
import click

DB_FILENAME = "budget.db"

class Expense:
    def __init__(self, id, description, amount):
        self.id = id
        self.description = description
        self.amount = amount

    def __eq__(self, other):
        return self.id == other.id and self.description == other.description and self.amount == other.amount
    
    def __repr__(self):
        return f'Expense(id={self.id!r}, description={self.description!r}, amount={self.amount!r})'

def read_db_or_init():
    """
    Read the expenses from the database file or initialize an empty list if the file doesn't exist.

    Returns:
        List[Expense]: List of expenses read from the database.
    """
    try:
        with open(DB_FILENAME, 'rb') as stream:
            expenses = pickle.load(stream)
    except FileNotFoundError:
        expenses = []
    return expenses

def save_db(expenses: List[Expense]):
    """
    Save the expenses to the database file.

    Args:
        expenses (List[Expense]): List of expenses to be saved.
    """
    with open(DB_FILENAME, 'wb') as stream:
        pickle.dump(expenses, stream)

def find_new_id(expenses: List[Expense]) -> int:
    """
    Find a new unique ID for an expense.

    Args:
        expenses (List[Expense]): List of existing expenses.

    Returns:
        int: New unique ID for an expense.
    """
    ids = {expense.id for expense in expenses}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def display_expenses(expenses: List[Expense]) -> None:
    """
    Display the list of expenses.

    Args:
        expenses (List[Expense]): List of expenses to be displayed.
    """
    if expenses:
        print("     MY LIST OF EXPENSES")
        print("----------------------------------")
        print("=ID= =AMOUNT= =BIG?= =DESCRIPTION=")
        for expense in expenses:
            if expense.amount >= 1000:
                big = "(!)"
            else:
                big = ""
            print(f'{expense.id:4} {expense.amount:^8} {big:^6} {expense.description}') 
    else:
        print("The list of expenses is empty")     

def sum_expenses_and_report(expenses: List[Expense]) -> None:
    """
    Calculate the total expenses and print a report.

    Args:
        expenses (List[Expense]): List of expenses to be summed and reported.
    """
    total_expenses = sum(expense.amount for expense in expenses)
    print("TOTAL: ", total_expenses)

def add_expense(description:str, amount: int, expenses: List[Expense]) ->None:
    """
    Add a new expense to the list.

    Args:
        description (str): Description of the expense.
        amount (int): Amount of the expense.
        expenses (List[Expense]): List of expenses to add the new expense to.

    Raises:
        ValueError: If the description is empty or the amount is not a positive number.
    """
    if not description:
        raise ValueError("Description can't be empty")
    if amount <= 0:
        raise ValueError("Amount must be a positive number")
    expense = Expense(
        id = find_new_id(expenses),
        description = description,
        amount = amount
    )
    expenses.append(expense)

def delete_last_expense(expenses: List[Expense]) -> None:
    """
    Delete the last expense from the list.

    Args:
        expenses (List[Expense]): List of expenses to delete the last expense from.
    """
    if not expenses:
        print("No expenses to delete.")
        return
    expenses.pop()

@click.group()
def cli():
    pass

@cli.command()
@click.argument('amount', type=int)
@click.argument('description')
def add(amount, description):
    """
    Add a new expense.

    Args:
        amount (int): Amount of the expense.
        description (str): Description of the expense.
    """
    expenses = read_db_or_init()
    try:
        add_expense(description, amount, expenses)
    except ValueError as e:
        print(f':-( Error: {e.args[0]}')
        sys.exit(1)
    save_db(expenses)
    print("Expense added successfully.")

@cli.command()
def report():
    """
    Display the list of expenses and sum the total.
    """
    expenses = read_db_or_init()
    display_expenses(expenses)
    sum_expenses_and_report(expenses)

@cli.command()
def delete():
    """
    Delete the last expense from the list.
    """
    expenses = read_db_or_init()
    delete_last_expense(expenses)
    save_db(expenses)
    print("Last expense deleted successfully.")

@cli.command()
@click.argument('csv_file')
def import_csv(csv_file):
    """
    Import expenses from a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
    """
    expenses = read_db_or_init()
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                description = row['description']
                amount = float(row['amount'])
                expense = Expense(find_new_id(expenses), description, amount)
                expenses.append(expense)
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    save_db(expenses)
    print("Data imported successfully.")

@cli.command()
def export_python():
    """
    Export expenses as Python objects.
    """
    expenses = read_db_or_init()
    for expense in expenses:
        print(expense)

if __name__ == "__main__":
    cli()