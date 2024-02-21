from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from interface import Interface
from constants import *

user_table_manager = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                             "mypassword",
                                             database="Tax_Calculator")
tax_table_manager = Tax_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                           "mypassword",
                                           database="Tax_Calculator")

# Instantiate interface object
interface = Interface()

# Main loop
while True:
    choice = input("Enter 1 to create a new account or 2 to log in: ")

    if choice in ["1", "2"]:
        break
    else:
        print("Invalid choice. Please enter either 1 or 2.")
if choice == "1":
    new_user = interface.new_account(user_table_manager)

    interface.manage_user_interface(new_user, user_table_manager,tax_table_manager )


elif choice == "2":
    account = interface.login(user_table_manager)
    if account.get_user_name() == "admin" and account.get_password() == "admin":
        interface.manage_admin_interface(user_table_manager, tax_table_manager)
    else:
        interface.manage_user_interface(account, user_table_manager, tax_table_manager)
