import mysql.connector
from tax_record import TaxRecord


class Tax_table_manager:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

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
        count = mycursor.fetchone()[
            0]  # COUNT( * ) returns numbers of rows with matching condition, my cursor returns tuple
        return count == 0

    def create_tax_table(self):
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )

        # Create a cursor object to execute SQL statements
        cursor = db.cursor()

        # Define the SQL statement to create the tax table
        create_table_query = """
        CREATE TABLE tax (
            tax_id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255),
            FOREIGN KEY (user_name) REFERENCES user(user_name) ON DELETE CASCADE,
            year INT,
            status VARCHAR(255),
            total_income DECIMAL(10, 2),
            income_tax DECIMAL(10, 2)
        )
        """

        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)

        # Commit the transaction
        db.commit()

        # Close the cursor and database connection
        cursor.close()
        db.close()

    def drop_tax_table(self):
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()

        # Define the SQL statement to create the tax table

        # Execute the SQL statement to create the table
        mycursor.execute("DROP TABLE tax")

        # Commit the transaction
        db.commit()

        # Close the cursor and database connection
        mycursor.close()
        db.close()
