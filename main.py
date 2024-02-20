from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from interface import Interface
from constants import *

user_table_functions = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin", "mypassword",
                                          database="Tax_Calculator")
tax_table_functions = Tax_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin", "mypassword",
                                        database="Tax_Calculator")

user_dictionary = user_table_functions.generate_user_dict()
tax_dictionary = tax_table_functions.generate_tax_dict()
ui = Interface()


def login():
    generate_user_dictionary = user_table_functions.generate_user_dict()

    while True:
        user_name = input("Enter your user name: ")
        password = input("Enter your password: ")

        if user_name in dict.keys(generate_user_dictionary) and generate_user_dictionary[
            user_name].get_password() == password:

            return generate_user_dictionary[
                user_name]
        else:
            print("Access denied. Please try again.")



def manage_user_interface(user):

    # current_user is user account object
    current_user = user_dictionary[user.get_user_name()]
    choice = 0
    while choice != 4:

        choice = ui.display_user_interface()
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
                year = input("Enter year:")
                status = input("Enter status: ")

                while status.capitalize() != 'M' and status.capitalize() != 'S':
                    print("Error! Please enter M for Married or S for Single.\n")
                    status = input("Enter marital status (M/S): ")
                total_income = float(input("Enter total income: "))
                if status == 'M':
                    total_income -= MARRIED_DEDUCTIBLE
                elif status == 'S':
                    total_income -= SINGLE_DEDUCTIBLE
                income_tax = total_income * INCOME_TAX

                tax_table_functions.add_tax_info(current_user.user_name, year, status, total_income, income_tax)

            case "4":
                break

            case _:
                print("\nCHOICE NOT IN SELECTION")


def manage_admin_interface():
    choice = 0
    while choice != "5":
        user_dictionary = user_table_functions.generate_user_dict()
        tax_dictionary = tax_table_functions.generate_tax_dict()

        choice = ui.display_admin_interface()
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


while True:
    choice = input("Enter 1 to create a new account or 2 to log in: ")

    if choice in ["1", "2"]:
        break
    else:
        print("Invalid choice. Please enter either 1 or 2.")
if choice == "1":
    new_user = ui.new_user()
    user_dictionary[new_user.user_name] = new_user
    manage_user_interface(new_user)


elif choice == "2":
    user = login()
    if user.get_user_name() == "admin" and user.get_password() == "admin":

        manage_admin_interface()
    else:
        manage_user_interface(user)
