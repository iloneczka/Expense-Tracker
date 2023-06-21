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

import csv
import pickle
from typing import List

import click

CSV_FILENAME = '/Users/ilo/Desktop/PYTHON/Praktyczny_Python/M07/expenses.csv'

class TodoItem:
    def __init__(self, id, description, amount):
        self.id= id
        self.description= description
        self.amount= amount

    def __eq__(self, other):
        return self.id == other.id and self.description == other.description and self.amount == other.amount
    
    def __repr__ (self):
        return f'TodoItem(id={self.id!r}, description={self.descriptiom!r}, amount={self.amount!r}'
    

# def read_expenses_from_csv (CSV_FILENAME):
#     try:
#         with open(CSV_FILENAME, 'rb') as stream:  
#             todos= pickle.load(stream)
#     except FileExistsError:
#         todos= []
#     print(todos)
#     return todos

def read_expenses_from_csv(csv_filename):
    todos = []
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader, start=1):
            description = row['description']
            amount = float(row['amount'])
            todo_item = TodoItem(index, description, amount)
            todos.append(todo_item)
    return todos


def display_expenses(todos: List[TodoItem]):
    print("=ID= =AMOUNT= =BIG?= =DESCRIPTION=")
    for todo in todos:
        if todo.amount >= 1000:
            big = "(!)"
        else:
            big = ""
        print(f'{todo.id:4} {todo.amount:^5} {big:^5} {todo.description}')      

def sum_expenses(todos: List[TodoItem]):
    total = sum(todo.amount for todo in todos)
    return total


def main():
    expenses = read_expenses_from_csv(CSV_FILENAME)
    display_expenses(expenses)


if __name__ == "__main__":
    main()

