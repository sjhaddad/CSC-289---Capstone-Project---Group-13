from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from commandline_interface import Interface
from constants import *

user_table_manager = User_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")
tax_table_manager = Tax_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")

# Instantiate interface object
interface = Interface()

# Landing page
while True:
    choice = input("Enter 1 to create a new account, 2 to log in, or 3 to exit program: ")

    if choice in ["1", "2", "3"]:
        break
    else:
        print("Invalid choice. Please enter either 1 or 2.")

# User selected to create account
if choice == "1":
    new_user = interface.new_account(user_table_manager)

    interface.manage_user_interface(new_user, user_table_manager, tax_table_manager)

# User selected to log in
elif choice == "2":
    account = interface.login(user_table_manager)
    if account.get_user_name() == "admin" and account.get_password() == "admin":
        interface.manage_admin_interface(user_table_manager, tax_table_manager)
    else:
        interface.manage_user_interface(account, user_table_manager, tax_table_manager)

elif choice == "3":
    exit