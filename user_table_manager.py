import mysql.connector
from account import Account

class User_table_manager:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        # If you find yourself re-declaring a variable in every single function in a class, just make that variable a member variable
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        self.mycursor = self.db.cursor(buffered=True)

    '''
    TABLE CREATION AND DELETION FUNCTIONS
    '''
    def create_user_table(self):
        create_table_query = """
            CREATE TABLE user (
                user_name VARCHAR(50) PRIMARY KEY,
                password VARBINARY(100),
                email VARCHAR(50),
                first_name VARCHAR(50),
                last_name VARCHAR(50)
            )
            """

        # Execute the SQL statement to create the table
        self.mycursor.execute(create_table_query)

        # Commit the transaction
        self.db.commit()

    def drop_user_table(self):
        # Execute the SQL statement to create the table
        self.mycursor.execute("DROP TABLE user")

        # Commit the transaction
        self.db.commit()

    '''
    TABLE EDITING FUNCTIONS
    '''
    def add_user(self, new_user):
        user_name = new_user.user_name
        password = new_user.password
        email = new_user.email
        first_name = new_user.first_name
        last_name = new_user.last_name

        try:
            # Define the INSERT INTO statement
            sql = "INSERT INTO user (user_name, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
            val = (user_name, password, email, first_name, last_name)

            # Execute the INSERT INTO statement
            self.mycursor.execute(sql, val)
            self.db.commit()

            print("User added successfully")
            return True

        except mysql.connector.Error as e:
            self.db.rollback()  # Rollback changes if an error occurs
            print(f"User Name already exists. Please enter a different User Name.{e}")

    def update_user(self, updated_user):
        try:
            # Construct the UPDATE statement
            update_query = "UPDATE user SET "
            update_query += "password = %s, email = %s, first_name = %s, last_name = %s"
            update_query += "WHERE user_name = %s"

            # Execute the UPDATE statement with the new values
            values = (updated_user.password, updated_user.email, updated_user.first_name,
                      updated_user.last_name, updated_user.user_name)
            self.mycursor.execute(update_query, values)

            # Commit the transaction
            self.db.commit()
            print("Database updated")

        except mysql.connector.Error as e:
            print(f"Error updating user information: {e}")

    def delete_user(self, user_name):
        # Check if the user_id exists in the table
        sql_check = "SELECT * FROM user WHERE user_name = %s"
        self.mycursor.execute(sql_check, (user_name,))
        result = self.mycursor.fetchone()

        if result is None:
            print("Error: User ID not found.")
            return  # Exit the function if user_id does not exist

        # Define the SQL query to delete the record with the specified user_id
        sql_delete = "DELETE FROM user WHERE user_name = %s"

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
            self.mycursor.execute("SELECT * FROM user")
            rows = self.mycursor.fetchall()

            print("\nUser Table:")
            print("{:<20} {:<40} {:<30} {:<20} {:<20}".format(
                "User Name", "Password", "E-mail", "First Name", "Last Name"))
            for row in rows:
                user_name, password, email, firstname, lastname = row
                password_hex = password.hex()
                password_hex_shortened = password_hex[:30]
                print("{:<20} {:<40} {:<30} {:<20} {:<20} ".format(
                    user_name, password_hex_shortened, email, firstname, lastname))
        except mysql.connector.Error as e:
            print(f"Failed to display table: {e}")

    '''
    DATA RETRIEVAL FUNCTIONS (GETTERS)
    '''
    def get_account_by_user_name(self, user_name):
        # Define the SQL statement to retrieve user credentials
        sql = "SELECT * FROM user WHERE user_name = %s"
        val = (user_name,)

        # Execute the SQL statement
        self.mycursor.execute(sql, val)

        # Fetch the result2
        result = self.mycursor.fetchone()
        if result:
            user_name, password, email, first_name, last_name = result
            password = bytes(password)

            return Account(user_name, password, email, first_name, last_name)

    def get_user_dict(self):
        user_data_dict = {}
        self.mycursor.execute("SELECT * FROM user")
        rows = self.mycursor.fetchall()

        for row in rows:
            user_name, password, email, firstname, lastname = row
            password_hex = password.hex()
            password_hex_shortened = password_hex[:30]
            user = Account(user_name, password_hex_shortened, email, firstname, lastname)
            user_data_dict[user_name] = user

        return user_data_dict

    def get_account_by_email(self, email):
        # Define the SQL statement to retrieve user credentials
        sql = "SELECT * FROM user WHERE email = %s"
        val = (email,)

        # Execute the SQL statement
        self.mycursor.execute(sql, val)

        # Fetch the result2
        result = self.mycursor.fetchone()
        if result:
            user_name, password, email, first_name, last_name = result
            password = bytes(password)

            return Account(user_name, password, email, first_name, last_name)

