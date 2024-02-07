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
        first_name = input("Enter first name: ").upper().strip() # New addition |
        while not first_name.isalpha():
            print("Only letters are allowed.\n")
            first_name = input("Enter first name: ").upper().strip()

        last_name = input("Enter last name: ").upper().strip()
        while not last_name.isalpha():
            print("Only letters are allowed.\n")
            last_name = input("Enter last name: ").upper().strip()

        marital_status = input("Single or Married: ").upper().strip()
        while not marital_status.isalpha() or marital_status not in ["SINGLE", "MARRIED"]:
            print("\nOnly letters are allowed: ")
            marital_status = input("Single or Married: ").upper().strip()

        while True:
            try:
                total_income = float(input("Enter total income without punctuations: ").strip())
                if total_income >= 0 and total_income.is_integer():
                    break
                elif total_income < 0:
                    print("Debt cannot be entered as income\n")
                else:
                    print("Only whole numbers allowed\n")
            except ValueError:
                print("Please enter a valid number\n")

        if marital_status.capitalize() == "Single" and total_income <= SINGLE_DEDUCTIBLE:
            print("Your income is below the taxable amount")
            return
        if marital_status.capitalize() == "Married" and total_income <= MARRIED_DEDUCTIBLE:
            print("Your income is below the taxable amount")
            return
        else:
            user1 = User(first_name, last_name, marital_status, total_income)
            add_user(user1)
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
