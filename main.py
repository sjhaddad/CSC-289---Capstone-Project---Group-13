from interface import Interface
from sqlite import create_table

ui = Interface()
create_table()

choice = 0
while choice != 5:
    choice = ui.display_interface()
    match choice:
        case 1:
            ui.new_user()
        case 2:
            ui.edit_income()
        case 3:
            ui.display_info()
        case 4:
            ui.display_by_name()
        case 5:
            break
        case _:  # Default value in case user inputs a choice that isn't specified
            pass
print("Thank you for using Shuttle Cash!")
