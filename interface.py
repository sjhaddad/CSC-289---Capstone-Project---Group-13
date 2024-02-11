from user import User
from sqlite import add_user, update_user, display_user_info_by_name, display_table, is_user_valid
from constants import *


class Interface:
    def display_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("1) Enter new user information")
        print("2) Edit user income by name")
        print("3) Display all user information")
        print("4) Display user information by name")
        print("5) Exit")
        choice = input("Please enter your choice: ")
        return choice

    # 1
    def new_user(self):
        # Take and validate input for user's first name
        first_name = input("Enter first name: ").capitalize().strip()
        while not first_name.isalpha():
            print("Only letters are allowed.\n")
            first_name = input("Enter first name: ").capitalize().strip()

        # Take and validate input for user's last name
        last_name = input("Enter last name: ").capitalize().strip()
        while not last_name.isalpha():
            print("Only letters are allowed.\n")
            last_name = input("Enter last name: ").capitalize().strip()

        # Take and validate input for user's marital status
        marital_status = input("Single or Married (S/M): ").capitalize().strip()
        while marital_status not in ["S", "M"]:
            print("\nInvalid input, please type either S or M")
            marital_status = input("Single or Married (S/M): ").capitalize().strip()

        # Take and validate input for total income
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
        
        # Validate that income is not below taxable amount
        if marital_status.capitalize() == "S" and total_income <= SINGLE_DEDUCTIBLE:
            print("Your income is below the taxable amount")
        if marital_status.capitalize() == "M" and total_income <= MARRIED_DEDUCTIBLE:
            print("Your income is below the taxable amount")
        else:
            user1 = User(first_name, last_name, marital_status, total_income)
            add_user(user1)
            print("New user added")

    # 2
    def edit_income(self):
        first_name = input("Enter first name: ").capitalize()
        last_name = input("Enter last name: ").capitalize()

        if not is_user_valid(first_name, last_name):
            print("User not found in the database. Please check the entered first and last name.")
            return

        status = input("Single or married (S/M): ")
        total_income = float(input("Enter updated total income: "))
        user_to_update = User(first_name, last_name, status, total_income)
        update_user(user_to_update)
        print("Income has been edited")


    # 3
    def display_info(self):
        display_table()

    # 4
    def display_by_name(self):
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        display_user_info_by_name(first_name, last_name)
