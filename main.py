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
    new_user = interface.new_user()
    user_dictionary[new_user.user_name] = new_user
    interface.manage_user_interface(new_user, user_dictionary, tax_dictionary, user_table_functions, tax_table_functions)


elif choice == "2":
    user = interface.login(user_dictionary)
    if user.get_user_name() == "admin" and user.get_password() == "admin":
        interface.manage_admin_interface(user_table_functions, tax_table_functions, user_dictionary, tax_dictionary)
    else:
        interface.manage_user_interface(user, user_dictionary, tax_dictionary, user_table_functions, tax_table_functions)
