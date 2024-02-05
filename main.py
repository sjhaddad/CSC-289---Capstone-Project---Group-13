from interface import *


user_interface()
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
