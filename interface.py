from account import Account
from constants import *
from input_validator import *


class Interface:
    # Creates a new user account
    def new_account(self, user_table_manager):
        while True:
            user_name = input("Enter User Name: ")
            password = input("Enter Password: ")
            email = input("Enter Email: ")
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            user = Account(user_name, password, email, first_name, last_name)

            if user_table_manager.add_user(user):
                return user

    # Handles login functionality if user selected option 2 to log in at initial UI prompt
    def login(self, user_table_manager):
        while True:
            user_name = input("Enter your user name: ")
            password = input("Enter your password: ")
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
                        print("Select an attribute to edit:")
                        print("1. Password")
                        print("2. Email")
                        print("3. First Name")
                        print("4. Last Name")
                        # Status editing has not been inplemented yet
                        # print("5. Status")
                        print("6. Exit")
                        choice = input("Enter your choice: \n")

                        if choice == "1":
                            new_password = input("Enter new password: ")
                            account.set_password(new_password)
                        elif choice == "2":
                            new_email = input("Enter new email: ")
                            account.set_email(new_email)
                        elif choice == "3":
                            new_first_name = input("Enter new first name: ")
                            account.set_first_name(new_first_name)
                        elif choice == "4":
                            new_last_name = input("Enter new last name: ")
                            account.set_last_name(new_last_name)
                        # elif choice == "5":
                        #     new_status = input("Enter new status: ")
                        #     account.set_status(new_status)
                        elif choice == "6":
                            user_table_manager.update_user(account)
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1 and 6.")
                # 3) Generate income tax estimate
                case "3":
                    year = validate_year()
                    status = validate_marital_status()
                    total_income = validate_total_income()

                    if status == 'M' and total_income > 22500:
                        total_income -= MARRIED_DEDUCTIBLE
                        income_tax = total_income * INCOME_TAX
                    elif status == 'S' and total_income > 12750:
                        total_income -= SINGLE_DEDUCTIBLE
                        income_tax = total_income * INCOME_TAX
                    else:
                        print("Your income is below the taxable amount!")
                        income_tax = 0


                    tax_table_manager.add_tax_info(account.user_name, year, status, total_income, income_tax)
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
                    user_name = (input("Enter User Name to search: "))
                    account = user_table_manager.get_account_by_user_name(user_name)
                    account.display_user_info()
                    account_records = tax_table_manager.get_tax_records(user_name)
                    for record in account_records:
                        record.display_tax_info()

                # 3) Delete user by user name
                case "3":
                    user_id = input("Enter user name of user to delete: ")
                    user_table_manager.delete_user(user_id)
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
