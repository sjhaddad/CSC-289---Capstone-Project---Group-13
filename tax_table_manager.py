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
    '''
    TABLE CREATION AND DELETION FUNCTIONS
    '''
    def create_tax_table(self):
        # Define the SQL statement to create the tax table
        create_table_query = """
        CREATE TABLE tax (
            tax_id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(100),
            FOREIGN KEY (user_name) REFERENCES user(user_name) ON DELETE CASCADE,
            year INT,
            status VARCHAR(10),
            total_income FLOAT(10, 2),
            adjusted_total_income FLOAT(10,2),
            income_tax FLOAT(10, 2)
        )
        """

        # Execute the SQL statement to create the table
        self.mycursor.execute(create_table_query)

        # Commit the transaction
        self.db.commit()

    def drop_tax_table(self):
        # Define the SQL statement to create the tax table

        # Execute the SQL statement to create the table
        self.mycursor.execute("DROP TABLE tax")

        # Commit the transaction
        self.db.commit()


    '''
    TABLE EDITING FUNCTIONS
    '''
    def add_tax_info(self, tax_record):
        user_name = tax_record.get_user_name()
        year = tax_record.get_year()
        status = tax_record.get_status()
        total_income = tax_record.get_total_income()
        adjusted_total_income = tax_record.get_adjusted_total_income()
        income_tax = tax_record.get_income_tax()

        try:
            sql = "INSERT INTO tax (user_name, year, status, total_income, adjusted_total_income, income_tax) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (user_name, year, status, total_income, adjusted_total_income, income_tax)
            self.mycursor.execute(sql, val)
            self.db.commit()
            print(f'Estimated income tax: ${income_tax:.2f}')
            # self.self.mycursor.close()
            # self.self.db.close()
        except mysql.connector.Error as e:
            print(f"Failed to add user: {e}")
    
    def delete_record(self, user_name):
        sql_check = "SELECT * FROM tax WHERE user_name = %s"
        self.mycursor.execute(sql_check, (user_name,))
        result = self.mycursor.fetchone()

        if result is None:
            print("Error: User ID not found.")
            return  # Exit the function if user_id does not exist

        # Define the SQL query to delete the record with the specified user_id
        sql_delete = "DELETE FROM tax WHERE user_name = %s"

        # Execute the SQL query with the user_id value as a parameter
        self.mycursor.execute(sql_delete, (user_name,))

        # Commit the transaction
        self.db.commit()

        print("Record deleted successfully")

    '''
    TABLE DISPLAY FUNCTION
    '''
    def display_table(self):
        try:
            self.mycursor.execute("SELECT * FROM tax")
            rows = self.mycursor.fetchall()

            print("\nTax Table:")
            print("{:<10} {:<30} {:<20} {:<20} {:<20} {:<30} {:<20}".format(
                "Tax ID", "User Name", "Year", "Status", "Total Income", "Adjusted Income", "Income Tax"))
            for row in rows:
                tax_id, user_name, year, status, total_income, adjusted_total_income, income_tax = row
                print("{:<10} {:<30} {:<20} {:<20} {:<20}{:<30} {:<20}".format(
                    tax_id, user_name, year, status, total_income, adjusted_total_income, income_tax))
        except mysql.connector.Error as e:
            print(f"Failed to display table: {e}")

    '''
    DATA RETRIEVAL FUNCTIONS (GETTERS)
    '''
    def get_tax_records(self, user_name):
        try:
            tax_records = []  # List to store Tax objects

            sql = "SELECT * FROM tax WHERE user_name = %s"
            val = (user_name,)

            # Execute the SQL statement
            self.mycursor.execute(sql, val)

            # Fetch all the results
            results = self.mycursor.fetchall()

            # Iterate over the fetched records
            for record in results:
                # Unpack the record
                tax_id, user_name, year, status, total_income, adjusted_total_income, income_tax = record
                # Create a Tax object and append it to the list
                tax_obj = TaxRecord(user_name, year, status, total_income)
                tax_records.append(tax_obj)

            # Close the cursor after fetching and processing the results
            # self.self.mycursor.close()

            # Return the list of Tax objects
            return tax_records

        except mysql.connector.Error as e:
            print(f"Failed to fetch tax records: {e}")
            return None  # Return None in case of an error

    def get_tax_dict(self):
        tax_data_dict = {}
        self.mycursor.execute("SELECT * FROM tax")
        rows = self.mycursor.fetchall()

        for row in rows:
            tax_id, user_name, year, status, total_income, adjusted_total_income, income_tax = row
            user_record = TaxRecord(user_name, year, status, total_income)
            tax_data_dict[user_name] = user_record

        return tax_data_dict
    
    '''
    INPUT VALIDATION FUNCTIONS
    '''
    def is_year_unique(self, user_name, year):
        sql = "SELECT COUNT(*) FROM tax WHERE user_name = %s AND year = %s"
        val = (user_name, year)
        self.mycursor.execute(sql, val)
        count = self.mycursor.fetchone()[
            0]  # COUNT( * ) returns numbers of rows with matching condition, my cursor returns tuple
        return count == 0