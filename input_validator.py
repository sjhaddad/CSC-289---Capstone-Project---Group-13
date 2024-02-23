from datetime import datetime


def validate_user_name():
    while True:
        user_name = input("Enter User Name: ")
        if user_name:
            return user_name
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_password():
    while True:
        password = input("Enter a password: ")
        if password:
            return password
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_email():
    while True:
        email = input("Enter email: ")
        if email:
            return email
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_first_name():
    while True:
        first_name = input("Enter User Name: ")
        if first_name:
            return first_name
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_last_name():
    while True:
        user_name = input("Enter User Name: ")
        if user_name:
            return user_name
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_total_income():
    while True:
        total_income_input = input("Enter total income: ").strip()
        if total_income_input:
            try:
                total_income = float(total_income_input)
                if total_income >= 0:
                    return total_income
                else:
                    print("Total income must be a positive number.")
            except ValueError:
                print("Please enter a valid number for total income.")
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_status():
    while True:
        status = input("Enter marital status (M for Married, S for Single): ").strip().upper()
        if status:
            if status == 'M' or status == 'S':
                return status
            else:
                print("Error! Please enter M for Married or S for Single.")
        else:
            print("Input cannot be blank. Please enter a value.")


def validate_year():
    while True:
        year_str = input("Enter a year: ").strip()
        if year_str:
            try:
                year = int(year_str)
                current_year = datetime.now().year
                if len(year_str) != 4:
                    raise ValueError("Year must be exactly four digits")
                if year < 1975 or year > current_year:
                    raise ValueError(f"Year must be between 1975 and {current_year}")
                return year
            except ValueError as e:
                print("Invalid year format:", e)
        else:
            print("Input cannot be blank. Please enter a value.")
