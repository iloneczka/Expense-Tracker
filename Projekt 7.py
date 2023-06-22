# python 3 "/Users/ilo/Desktop/PYTHON/Praktyczny_python_M07/Projekt 7.py" <command>

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
    try:
        with open(DB_FILENAME, 'rb') as stream:
            expenses = pickle.load(stream)
    except FileNotFoundError:
        expenses = []
    return expenses

def save_db(expenses: List[Expense]):
    with open(DB_FILENAME, 'wb') as stream:
        pickle.dump(expenses, stream)

def find_new_id(expenses: List[Expense]) -> int:
    ids = {expense.id for expense in expenses}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def display_expenses(expenses: List[Expense]) -> None:
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
    total_expenses = sum(expense.amount for expense in expenses)
    print("TOTAL: ", total_expenses)

def add_expense(description:str, amount: int, expenses: List[Expense]) ->None:
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
    expenses = read_db_or_init()
    display_expenses(expenses)
    sum_expenses_and_report(expenses)

@cli.command()
def delete():
    expenses = read_db_or_init()
    delete_last_expense(expenses)
    save_db(expenses)
    print("Last expense deleted successfully.")

@cli.command()
@click.argument('csv_file')
def import_csv(csv_file):
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
    expenses = read_db_or_init()
    for expense in expenses:
        print(expense)

if __name__ == "__main__":
    cli()