from account import Account
from constants import *
from input_validator import *


class Interface:
    # Creates a new user account
    def new_account(self, user_table_manager):
        while True:
            user_name = validate_user_name()
            password = validate_password()
            email = validate_email()
            first_name = validate_first_name()
            last_name = validate_last_name()
            user = Account(user_name, password, email, first_name, last_name)

            if user_table_manager.add_user(user):
                return user

    # Handles login functionality if user selected option 2 to log in at initial UI prompt
    def login(self, user_table_manager):
        while True:
            user_name = validate_user_name()
            password = validate_password()
            if user_name == "admin" and password == "admin":
                return Account("admin", "admin", None,None,None)
            account = user_table_manager.authenticate_user(user_name, password)
            if account:
                break
            else:
                print("Access denied. Please try again.")
        return account

    # Displays the interface for a signed in user of non-admin account
    def display_user_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("1) Display all user information")
        print("2) Edit user profile")
        print("3) Generate income tax estimate")
        print("4) Exit\n")
        choice = input("Please enter your choice: ")
        return choice

    # Handles functionality for the interface for a signed in user of non-admin account
    def manage_user_interface(self, account, user_table_manager, tax_table_manager):
        choice = 0
        while choice != 4:
            choice = self.display_user_interface()
            match choice:
                # 1) Display all user information
                case "1":
                    account.display_user_info()
                    account_records = tax_table_manager.get_tax_records(account.get_user_name())
                    for record in account_records:
                        record.display_tax_info()
                # 2) Edit user profile
                case "2":
                    while True:
                        print("\nSelect an attribute to edit:")
                        print("1. Password")
                        print("2. Email")
                        print("3. First Name")
                        print("4. Last Name")
                        print("5. Submit changes")
                        choice = input("Enter your choice: \n")

                        if choice == "1":
                            account.set_password(validate_password())
                        elif choice == "2":
                            account.set_email(validate_email(account.get_user_name()))
                        elif choice == "3":

                            account.set_first_name(validate_first_name())
                        elif choice == "4":
                            account.set_last_name(validate_last_name())

                        elif choice == "5":
                            user_table_manager.update_user(account)
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1 and 5.")
                # 3) Generate income tax estimate
                case "3":
                    year = validate_year(account.get_user_name())
                    status = validate_status()
                    total_income = validate_total_income()

                    if status == 'M' and total_income > 22500:
                        adjusted_income = total_income - MARRIED_DEDUCTIBLE
                        income_tax = adjusted_income * INCOME_TAX
                    elif status == 'S' and total_income > 12750:
                        adjusted_income = total_income - SINGLE_DEDUCTIBLE
                        income_tax = adjusted_income * INCOME_TAX
                    else:
                        adjusted_income = total_income
                        income_tax = 0

                    tax_table_manager.add_tax_info(account.user_name, year, status, adjusted_income, income_tax)
                # 4) Exit
                case "4":
                    break
                # Default value
                case _:
                    print("\nCHOICE NOT IN SELECTION")

    # Displays the interface for a signed in user of admin type
    def display_admin_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("ADMIN OPTIONS")
        print("1) Display all user data")
        print("2) Display user information by user name")
        print("3) Delete user by user name")
        print("4) Display tax table")
        print("5) Exit")
        choice = input("Please enter your choice: ")

        return choice

    # Handles the functionality for the interface for a signed in user of admin type
    def manage_admin_interface(self, user_table_manager, tax_table_manager):
        choice = 0
        while choice != "5":
            choice = self.display_admin_interface()
            match choice:
                # 1) Display all user data
                case "1":
                    user_table_manager.display_table()
                    tax_table_manager.display_table()
                # 2) Display user information by user name
                case "2":
                    user_name = validate_user_name()
                    if user_table_manager.get_account_by_user_name(user_name):
                        account = user_table_manager.get_account_by_user_name(user_name)
                        account.display_user_info()
                        account_records = tax_table_manager.get_tax_records(user_name)
                        for record in account_records:
                            record.display_tax_info()
                    else:
                        print("Error: Unable to find a matching username.")

                # 3) Delete user by user name
                case "3":
                    user_name = validate_user_name()
                    user_table_manager.delete_user(user_name)
                    # tax_table_manager.delete_user(user_id)
                # 4) Display tax table
                case "4":
                    tax_table_manager.display_table()
                # 5) Exit
                case "5":
                    break
                # Default value
                case _:
                    print("\nCHOICE NOT IN SELECTION")
