from user import User
from sqlite import Sqlite
from constants import *


class Interface:

    def __init__(self):
        self.sql = Sqlite()

    def display_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("1) Enter new user information")
        print("2) Edit user income by name")
        print("3) Display all user information")
        print("4) Display user information by name")
        print("5) Exit")
        choice = input("Please enter your choice: ")
        return int(choice)

    # 1
    def new_user(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        marital_status = input("Single or married: ")
        total_income = float(input("Enter total income: "))
        if marital_status.capitalize() == "Single" and total_income <= SINGLE_DEDUCTIBLE:
            print("Your income is below the taxable amount")
        if marital_status.capitalize() == "Married" and total_income <= MARRIED_DEDUCTIBLE:  # If we don't include this, users with negative taxes owed would be stored in the database
            print("Your income is below the taxable amount")
        else:
            user1 = User(first_name, last_name, marital_status, total_income)
            self.sql.add_user(user1)
            print("New user added")

    # 2
    def edit_income(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        status = input("Single or married: ")
        total_income = float(input("Enter updated total income: "))
        user_to_update = User(first_name, last_name, status, total_income)
        self.sql.update_user(user_to_update)
        print("Income has been edited")

    # 3
    def display_info(self):
        self.sql.display_table()

    # 4
    def display_by_name(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        self.sql.display_user_info_by_name(first_name, last_name)
