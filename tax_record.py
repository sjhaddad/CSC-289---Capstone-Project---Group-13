from constants import *


class TaxRecord:

    def __init__(self, user_name, year, status, total_income):
        self.user_name = user_name
        self.status = status
        self.year = year
        self.total_income = total_income
        self.income_tax = total_income * INCOME_TAX

    def display_tax_info(self):
        return(f'\nStatus: {self.status}\nYear: {self.year}\n' \
              f'Total income: {self.total_income}\nIncome tax: {self.income_tax}\n')
