from account import Account
from user_table_manager import User_table_manager
from constants import *


class Interface:

    def __init__(self):
        self.user_table_manager = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                                     "mypassword",
                                                     database="Tax_Calculator")

    def new_user(self):
        user_table_functions = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                                  "mypassword",
                                                  database="Tax_Calculator")

        user_name = input("Enter User Name: ")
        password = input("Enter Password: ")
        email = input("Enter Email: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")

        user = Account(user_name, password, email, first_name, last_name)
        user_table_functions.add_user(user)

        return user
    
    def login(self, user_dictionary):
        while True:
            user_name = input("Enter your user name: ")
            password = input("Enter your password: ")

            if user_name in dict.keys(user_dictionary) and user_dictionary[
                user_name].get_password() == password:

                return user_dictionary[
                    user_name]
            else:
                print("Access denied. Please try again.")

    def display_user_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("1) Display all user information")
        print("2) Edit user profile")
        print("3) Generate income tax estimate")
        print("4) Exit\n")
        choice = input("Please enter your choice: ")
        return choice
    
    
    def manage_user_interface(self, user, user_dictionary, tax_dictionary, user_table_functions, tax_table_functions):

        # current_user is user account object
        current_user = user_dictionary[user.get_user_name()]
        choice = 0
        while choice != 4:

            choice = self.display_user_interface()
            match choice:
                case "1":
                    current_user.display_user_info()
                    for tax_object in tax_dictionary.values():
                        if tax_object.user_name == current_user.user_name:
                            print(tax_object.display_tax_info())

                case "2":
                    while True:
                        print("Select an attribute to edit:")
                        print("1. Password")
                        print("2. Email")
                        print("3. First Name")
                        print("4. Last Name")
                        print("5. Status")
                        print("6. Exit")

                        choice = input("Enter your choice: \n")

                        if choice == "1":
                            new_password = input("Enter new password: ")
                            current_user.set_password(new_password)
                        elif choice == "2":
                            new_email = input("Enter new email: ")
                            current_user.set_email(new_email)
                        elif choice == "3":
                            new_first_name = input("Enter new first name: ")
                            current_user.set_first_name(new_first_name)
                        elif choice == "4":
                            new_last_name = input("Enter new last name: ")
                            current_user.set_last_name(new_last_name)
                        elif choice == "5":
                            new_status = input("Enter new status: ")
                            user.set_status(new_status)
                        elif choice == "6":
                            user_table_functions.update_user(current_user)
                            print("User dictionary updated")
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1 and 6.")

                case "3":
                    year = input("Enter year: ")
                    status = input("Enter marital status (M/S): ")

                    while status.capitalize() != 'M' and status.capitalize() != 'S':
                        print("Error! Please enter M for Married or S for Single.\n")
                        status = input("Enter marital status (M/S): ")
                    total_income = float(input("Enter total income: "))
                    if status == 'M':
                        total_income -= MARRIED_DEDUCTIBLE
                    elif status == 'S':
                        total_income -= SINGLE_DEDUCTIBLE
                    if total_income < 0:
                        print("Your income is below the taxable amount!")
                        income_tax = 0
                    else:
                        income_tax = total_income * INCOME_TAX

                    tax_table_functions.add_tax_info(current_user.user_name, year, status, total_income, income_tax)

                case "4":
                    break

                case _:
                    print("\nCHOICE NOT IN SELECTION")

    def display_admin_interface(self):
        print("\nWelcome to Shuttle Cash!")
        # print("1) Generate estimate: ")

        # print("2) Display user information")
        print("ADMIN OPTIONS")
        print("1) Display all user data")
        print("2) Display user information by user name")
        print("3) Delete user by ID")
        print("4) Display tax table")
        print("5) Exit")
        choice = input("Please enter your choice: ")

        return choice
    
    def manage_admin_interface(self, user_table_functions, tax_table_functions, user_dictionary, tax_dictionary):
        choice = 0
        while choice != "5":
            choice = self.display_admin_interface()
            match choice:
                case "1":
                    user_table_functions.display_table()
                    tax_table_functions.display_table()
                case "2":
                    user_name = (input("Enter User Name to search: "))
                    if user_name in dict.keys(user_dictionary):
                        print(user_dictionary[user_name].display_user_info())
                        for tax_object in tax_dictionary.values():
                            if tax_object.user_name == user_name:
                                print(tax_object.display_tax_info())

                case "3":
                    user_id = (input("Enter user name of user to delete: "))
                    user_dictionary.pop(user_id)
                    user_table_functions.delete_user(user_id)
                case "4":
                    tax_table_functions.display_table()

                case "5":
                    break
                case _:
                    print("\nCHOICE NOT IN SELECTION")
