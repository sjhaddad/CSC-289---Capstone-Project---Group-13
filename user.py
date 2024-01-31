class User:

    def __init__(self, first, last, total_income):
        self.first = first
        self.last = last
        self.total_income = total_income
        # https://www.ncdor.gov/taxes-forms/individual-income-tax/north-carolina-standard-deduction-or-north-carolina-itemized-deductions
        # standard deduction for single status is $12,750.
        # income tax rate is 4.75%
        self.tax = round((total_income - 12750) * 0.0475, 2)


