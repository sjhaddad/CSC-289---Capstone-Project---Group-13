from constants import *

class User:

    def __init__(self, first, last, status, total_income):
        self.first = first
        self.last = last
        self.status = status
        self.total_income = total_income
        if self.status.capitalize() == "Single":
            self.deductible = SINGLE_DEDUCTIBLE
        else:
            self.deductible = MARRIED_DEDUCTIBLE
        self.tax = round((total_income - self.deductible) * INCOME_TAX, 2)

    def get_first(self):
        return self.first
    
    def get_last(self):
        return self.last
    
    def get_status(self):
        return self.status
    
    def get_total_income(self):
        return self.total_income
    
    def get_tax(self):
        return self.tax
    
    def set_first(self, first):
        self.first = first
    
    def set_last(self, last):
        self.last = last
    
    def set_status(self, status):
        self.status = status
    
    def set_total_income(self, total):
        self.total_income = total
    
    def set_tax(self, tax):
        self.tax = tax
    


