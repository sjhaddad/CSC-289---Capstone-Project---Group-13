from constants import *

class TaxRecord:

    def __init__(self, user_name, year, status, total_income):
        self.user_name = user_name
        self.status = status
        self.year = year
        self.total_income = total_income
        self.income_tax = total_income * INCOME_TAX

    # Getters
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
        print(f'\nYear: {self.year}\nStatus: {self.status}\n' \
              f'Total income: {self.total_income}\nIncome tax: {self.income_tax}\n')
