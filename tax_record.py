from constants import *

class TaxRecord:

    def __init__(self, user_name, year, status, adjusted_income, income_tax):
        self.user_name = user_name
        self.status = status
        self.year = year
        self.adjusted_income = adjusted_income
        self.income_tax = income_tax



    # Getters
    def get_income_tax(self):
        return self.income_tax

    def get_user_name(self):
        return self.user_name
    
    def get_status(self):
        return self.status
    
    def get_year(self):
        return self.year
    
    def get_total_income(self):
        return self.total_income
    
    def get_income_tax(self):
        return self.income_tax
    
    # Setters
    def set_income_tax(self, income_tax):
        self.income_tax = income_tax
    def set_user_name(self, user_name):
        self.user_name = user_name
    
    def set_status(self, status):
        self.status = status

    def set_year(self, year):
        self.year = year

    def set_total_income(self, total_income):
        self.total_income = total_income
        self.income_tax = total_income * INCOME_TAX

    # Other methods
    def display_tax_info(self):
        if self.income_tax == 0:
            print("Year:", self.year)
            print("Status:", self.status)
            print("Total income:", f"${self.adjusted_income:.2f}")
            print("No income tax owed.\n")
        else:
            print("Year:", self.year)
            print("Status:", self.status)
            print("Total income - deductible:", f"${self.adjusted_income:.2f}")
            print(f"Income tax: ${self.income_tax:.2f}\n")