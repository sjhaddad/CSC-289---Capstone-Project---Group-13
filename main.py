from interface import Interface
from sqlite import Sqlite

ui = Interface()
sql = Sqlite()

sql.create_table()

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
        case _:
            print("\nCHOICE NOT IN SELECTION")
print("Thank you for using Shuttle Cash!")
