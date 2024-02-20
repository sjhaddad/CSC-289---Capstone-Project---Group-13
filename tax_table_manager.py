import mysql.connector
from tax_record import TaxRecord


class Tax_table_manager:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        self.mycursor = self.db.cursor()

    def generate_tax_dict(self):
        tax_dict = {}  # Create an empty dictionary
        self.mycursor.execute("SELECT * FROM tax")

        tax_table = self.mycursor.fetchall()

        for record in tax_table:
            tax_id, user_name, year, status, total_income, income_tax = record
            tax_obj = TaxRecord(user_name, year, status, total_income)
            tax_dict[tax_id] = tax_obj

        return tax_dict

    def add_tax_info(self, user_name, year, status, total_income, income_tax):
        try:
            sql = "INSERT INTO tax (user_name, year, status, total_income, income_tax) VALUES (%s, %s, %s, %s, %s)"
            val = (user_name, year, status, total_income, income_tax)
            self.mycursor.execute(sql, val)
            self.db.commit()
            print(f'Estimated income tax: {income_tax}')
        except mysql.connector.Error as e:
            print(f"Failed to add user: {e}")



    def display_table(self):

        try:
            self.mycursor.execute("SELECT * FROM tax")
            rows = self.mycursor.fetchall()

            print("\nTax Table:")

            for row in rows:
                tax_id, user_name, year, status, total_income, income_tax = row
                print("{:<10} {:<30} {:<20} {:<20} {:<20} {:<20}".format(
                    tax_id, user_name, year, status, total_income, income_tax))
        except mysql.connector.Error as e:
            print(f"Failed to display table: {e}")
