from user import User
from sqlite import create_table, add_user, update_user, display_user_info_by_name, display_table


def create_table():
    create_table()


# 1
def new_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    marital_status = input("Single or married: ")
    status = 0
    if marital_status.capitalize() == "Single":
        status = 12750
    else:
        status = 22500
    total_income = float(input("Enter total income: "))
    if marital_status.capitalize() == "Single" and total_income <= 12750:
        print("Your income is below the taxable amount")
    if marital_status.capitalize() == "Married" and total_income <= 25500:  # If we don't include this, users with negative taxes owed would be stored in the database
        print("Your income is below the taxable amount")
    else:
        user1 = User(first_name, last_name, status, total_income)
        add_user(user1)
        return "New user added"


# 2
def edit_income():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    total_income = float(input("Enter updated total income: "))
    user_to_update = User(first_name, last_name, 0, total_income)
    update_user(user_to_update)
    return "Income has been edited"


# 3
def display_info():
    display_table()


# 4
def display_by_name():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    display_user_info_by_name(first_name, last_name)
