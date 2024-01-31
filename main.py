from user import User
from sqlite import create_table, add_user, display_table

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
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            total_income = float(input("Enter total income: "))
            if total_income <= 12750:   # If we don't include this, users with negative taxes owed would be stored in the database
                print("Your income is below the taxable amount")
            else:
                user1 = User(first_name, last_name, total_income)
                add_user(user1)
        case 2:
            print("Placeholder :)")
        case 3:
            display_table()
        case 4:
            print("Placeholder :)")
        case 5:
            break
        case _:     # Default value in case user inputs a choice that isn't specified
            pass
print("Thank you for using Shuttle Cash!")