from interface_functions import *


def user_interface():
    print("\nWelcome to Shuttle Cash!")
    print("1) Enter new user information")
    print("2) Edit user income by name")
    print("3) Display all user information")
    print("4) Display user information by name")
    print("5) Exit")
    choice = input("Please enter your choice: ")
    return int(choice)


create_table()

choice = 0
while choice != 5:
    choice = user_interface()
    match choice:
        case 1:
            new_user()
        case 2:
            edit_income()
        case 3:
            display_info()
        case 4:
            display_by_name()
        case 5:
            break
        case _:  # Default value in case user inputs a choice that isn't specified
            pass
print("Thank you for using Shuttle Cash!")
