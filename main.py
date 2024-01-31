from user import User
from sqlite import create_table, add_user, display_table

first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
total_income = float(input("Enter total income: "))

user1 = User(first_name, last_name, total_income)

create_table()
add_user(user1)
display_table()
