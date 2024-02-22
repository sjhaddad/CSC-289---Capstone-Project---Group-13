from datetime import datetime


def validate_total_income():
    while True:
        total_income_input = input("Enter total income: ")
        try:
            total_income = float(total_income_input)
            if total_income >= 0:
                return total_income
            else:
                print("Total income must be a positive number.")
        except ValueError:
            print("Please enter a valid number for total income.")


def validate_marital_status():
    while True:
        status = input("Enter marital status (M for Married, S for Single): ").strip().upper()
        if status == 'M' or status == 'S':
            return status
        else:
            print("Error! Please enter M for Married or S for Single.")


def validate_year():
    while True:
        year_str = input("Enter a year: ")
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