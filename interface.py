from user_account import UserAccount
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

        user = UserAccount(user_name, password, email, first_name, last_name)
        user_table_functions.add_user(user)

        return user

    def display_user_interface(self):
        print("\nWelcome to Shuttle Cash!")
        print("1) Display all user information")
        print("2) Edit user profile: ")
        print("3) Generate income tax estimate: ")

        print("4) Exit\n")
        choice = input("Please enter your choice: ")
        return choice

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
