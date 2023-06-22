# Napisz program, który ułatwi milionom Polaków śledzenie własnych wydatków oraz ich analizę. Program pozwala na łatwe dodawanie nowych wydatków i generowanie raportów. Aplikacja działa także pomiędzy uruchomieniami, przechowując wszystkie dane w pliku. Każdy wydatek ma id, opis oraz wielkość kwoty.

# 1. Program posiada podkomendy add, report, export-python oraz import-csv. 

# 2. Podkomenda add pozwala na dodanie nowego wydatku. Należy wówczas podać jako kolejne argumenty wiersza poleceń wielkość wydatku (jako int) oraz jego opis (w cudzysłowach). Na przykład:
# $ python budget.py add 100 "stówa na zakupy". 
# Jako id wybierz pierwszy wolny id - np. jeśli masz już wydatki z id = 1, 2, 4, 5, wówczas wybierz id = 3.

# 3. Podkomenda report wyświetla wszystkie wydatki w tabeli. W tabeli znajduje się także kolumna "big?", w której znajduje się ptaszek, gdy wydatek jest duży, tzn. co najmniej 1000. Dodatkowo, na samym końcu wyświetlona jest suma wszystkich wydatów.

# 4. Podkomenda export-python wyświetla listę wszystkich wydatków jako obiekt (hint: zaimplementuj poprawnie metodę __repr__ w klasie reprezentującej pojedynczy wydatek).

# 5. Podkomenda import-csv importuję listę wydatków z pliku CSV.

# 6. Program przechowuje pomiędzy uruchomieniami bazę wszystkich wydatków w pliku budget.db. Zapisuj i wczytuj stan używając modułu pickle. Jeżeli plik nie istnieje, to automatycznie stwórz nową, pustą bazę. Zauważ, że nie potrzebujemy podpolecenia init.

# 7. Wielkość wydatku musi być dodatnią liczbą. Gdzie umieścisz kod sprawdzający, czy jest to spełnione? W jaki sposób zgłosisz, że warunek nie jest spełniony?

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
    try:
        with open(DB_FILENAME, 'rb') as stream:
            expenses = pickle.load(stream)
    except FileNotFoundError:
        expenses = []
    return expenses

def save_db(expenses: List[Expense]):
    with open(DB_FILENAME, 'wb') as stream:
        pickle.dump(expenses, stream)

def find_new_id(expenses):
    ids = {expense.id for expense in expenses}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def display_expenses(expenses: List[Expense]):
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

def sum_expenses_and_report(expenses: List[Expense]):
    total_expenses = sum(expense.amount for expense in expenses)
    print("TOTAL: ", total_expenses)

def add_expense(description:str, amount: int, expenses: List[Expense]) ->None:
    if not description:
        raise ValueError("Description can't be empty")
    if amount <= 0:
        raise ValueError("Amount must be a positive number")
    expense = Expense(
        id=find_new_id(expenses),
        description=description,
        amount=amount,
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
        print(f':-( Błąd: {e.args[0]}')
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