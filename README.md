# Expense Tracker 

## Table of Contents
- [General Info](#general-info)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Testing](#testing)
- [Solutions](#solutions)
- [Future Plans](#future-plans)
- [Inspirations and Acknowledgments](#inspirations-and-acknowledgments)

## General Info
This is a Python program that helps track expenses and analyze them. The program allows for easy addition of new expenses and generation of reports. The application also works between runs by storing all data in a file. Each expense has an ID, description, and amount.

## Features
- Add new expenses with an amount and description.
- Display all expenses and the total.
- Delete the last expense from the list.
- Import expenses from a CSV file.
- Export expenses as Python objects.

## Technologies Used
The program is written in Python.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


## Prerequisites
Before running the program, make sure you have Python 3.11.2 installed on your system and the required libraries.  
If you haven't installed the click library yet, you can do so by running:
,,,
pip install click
,,,

## Setup
To run the project locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. To execute the program, use the following command:
,,,
python3 expense_tracker.py <command>
,,,

### Usage
The program can be used with the following commands:

1. `add <amount> <description>`: Add a new expense. 
Example: `python3 expense_tracker.py add 50 "Groceries"`
2. `report`: Display all expenses and the total. 
Example: `python3 expense_tracker.py report`
3. `delete`: Delete the last expense from the list. 
Example: `python3 expense_tracker.py delete`
4. `import-csv <csv_file>`: Import expenses from a CSV file. 
Example: `python3 expense_tracker.py import-csv expenses.csv`
5. `export-python`: Export expenses as Python objects. 
Example: `python3 expense_tracker.py export-python`

## Testing

TODO

## Solutions
The program uses a list of `Expense` objects to store the expenses. Expenses are saved in a file named `budget.db` using the `pickle` module, which allows data to be stored between runs.

## Future Plans
The program currently provides basic functionality for expense tracking. Future plans may include adding more advanced features such as data visualization, filtering expenses by date or category, and adding user authentication.

## Inspirations and Acknowledgments
This project was inspired by the "Praktyczny Python" training course and was adapted from the original version for educational purposes.
