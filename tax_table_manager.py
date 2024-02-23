import mysql.connector
from tax_record import TaxRecord


class Tax_table_manager:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    # ** THIS FUNCTION CURRENTLY UNUSED AS WE ARE NOT USING DICTS **
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
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()

        try:
            sql = "INSERT INTO tax (user_name, year, status, total_income, income_tax) VALUES (%s, %s, %s, %s, %s)"
            val = (user_name, year, status, total_income, income_tax)
            mycursor.execute(sql, val)
            db.commit()
            print(f'Estimated income tax: {income_tax}')
            # self.mycursor.close()
            # self.db.close()
        except mysql.connector.Error as e:
            print(f"Failed to add user: {e}")

    # def delete_user(self, user_name):
    #         db = mysql.connector.connect(
    #             host=self.host,
    #             user=self.user,
    #             passwd=self.passwd,
    #             database=self.database
    #         )
    #         mycursor = db.cursor()
    #         mycursor = db.cursor()
    #
    #         # Define the primary key value of the record you want to delete
    #         primary_key_value = user_name  # Replace with the specific primary key value
    #
    #         # Define the SQL query to delete the record with the specified primary key
    #         sql = "DELETE FROM tax WHERE user_name = %s"
    #
    #         # Execute the SQL query with the primary key value as a parameter
    #         mycursor.execute(sql, (primary_key_value,))
    #
    #         # Commit the transaction
    #         db.commit()
    #
    #         print("Record deleted successfully")

    def display_table(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
        try:
            mycursor.execute("SELECT * FROM tax")
            rows = mycursor.fetchall()

            print("\nTax Table:")
            print("{:<10} {:<30} {:<20} {:<20} {:<20} {:<20}".format(
                "Tax ID", "User Name", "Year", "Status", "Total Income", "Income Tax"))
            for row in rows:
                tax_id, user_name, year, status, total_income, income_tax = row
                print("{:<10} {:<30} {:<20} {:<20} {:<20} {:<20}".format(
                    tax_id, user_name, year, status, total_income, income_tax))
        except mysql.connector.Error as e:
            print(f"Failed to display table: {e}")

    def get_tax_records(self, user_name):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
        try:
            tax_records = []  # List to store Tax objects

            sql = "SELECT * FROM tax WHERE user_name = %s"
            val = (user_name,)

            # Execute the SQL statement
            mycursor.execute(sql, val)

            # Fetch all the results
            results = mycursor.fetchall()

            # Iterate over the fetched records
            for record in results:
                # Unpack the record
                tax_id, user_name, year, status, total_income, income_tax = record
                # Create a Tax object and append it to the list
                tax_obj = TaxRecord(user_name, year, status, total_income, income_tax)
                tax_records.append(tax_obj)

            # Close the cursor after fetching and processing the results
            # self.mycursor.close()

            # Return the list of Tax objects
            return tax_records

        except mysql.connector.Error as e:
            print(f"Failed to fetch tax records: {e}")
            return None  # Return None in case of an error

    def is_year_unique(self, user_name, year):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()

        sql = "SELECT COUNT(*) FROM tax WHERE user_name = %s AND year = %s"
        val = (user_name, year)
        mycursor.execute(sql, val)
        count = mycursor.fetchone()[0] #COUNT( * ) returns numbers of rows with matching condition, my cursor returns tuple
        return count == 0


