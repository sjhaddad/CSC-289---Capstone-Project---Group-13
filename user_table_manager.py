import mysql.connector
from account import Account


class User_table_manager:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    def update_user(self, updated_user):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
        try:

            # Construct the UPDATE statement
            update_query = "UPDATE user SET "
            update_query += "password = %s, email = %s, first_name = %s, last_name = %s"
            update_query += "WHERE user_name = %s"

            # Execute the UPDATE statement with the new values
            values = (updated_user.password, updated_user.email, updated_user.first_name,
                      updated_user.last_name, updated_user.user_name)
            mycursor.execute(update_query, values)

            # Commit the transaction
            db.commit()
            print("Database updated")

        except mysql.connector.Error as e:
            print(f"Error updating user information: {e}")

    def add_user(self, new_user):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
        user_name = new_user.user_name
        password = new_user.password
        print(type(password))
        email = new_user.email
        first_name = new_user.first_name
        last_name = new_user.last_name

        try:

            # Define the INSERT INTO statement
            sql = "INSERT INTO user (user_name, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
            val = (user_name, password, email, first_name, last_name)

            # Execute the INSERT INTO statement
            mycursor.execute(sql, val)
            db.commit()

            print("User added successfully")
            return True

        except mysql.connector.Error as e:
            db.rollback()  # Rollback changes if an error occurs
            print(f"User Name already exists. Please enter a different User Name.{e}")

    def delete_user(self, user_name):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()

        # Check if the user_id exists in the table
        sql_check = "SELECT * FROM user WHERE user_name = %s"
        mycursor.execute(sql_check, (user_name,))
        result = mycursor.fetchone()

        if result is None:
            print("Error: User ID not found.")
            return  # Exit the function if user_id does not exist

        # Define the SQL query to delete the record with the specified user_id
        sql_delete = "DELETE FROM user WHERE user_name = %s"

        # Execute the SQL query with the user_id value as a parameter
        mycursor.execute(sql_delete, (user_name,))

        # Commit the transaction
        db.commit()

        print("Record deleted successfully")

    def display_table(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
        try:
            mycursor.execute("SELECT * FROM user")
            rows = mycursor.fetchall()

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

    def get_account_by_user_name(self, user_name):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
        # Create a cursor object to execute SQL statements

        # Define the SQL statement to retrieve user credentials
        sql = "SELECT * FROM user WHERE user_name = %s"
        val = (user_name,)

        # Execute the SQL statement
        mycursor.execute(sql, val)

        # Fetch the result2

        result = mycursor.fetchone()
        if result:
            user_name, password, email, first_name, last_name = result
            password = bytes(password)

            return Account(user_name, password, email, first_name, last_name)

        # Close the cursor and connection
        # self.mycursor.close()

    def create_user_table(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()
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
        mycursor.execute(create_table_query)

        # Commit the transaction
        db.commit()

        # Close the cursor and database connection
        mycursor.close()
        db.close()

    def drop_user_table(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        mycursor = db.cursor()

        # Execute the SQL statement to create the table
        mycursor.execute("DROP TABLE user")

        # Commit the transaction
        db.commit()

        # Close the cursor and database connection
        mycursor.close()
        db.close()
