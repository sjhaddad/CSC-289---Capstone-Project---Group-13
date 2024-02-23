import mysql.connector
from account import Account

class User_table_manager:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database


    # ** THIS FUNCTION CURRENTLY UNUSED AS WE ARE NOT USING DICTS **
    def generate_user_dict(self):
        user_dict = {}  # Create an empty dictionary
        self.mycursor.execute("SELECT * FROM user")

        rows = self.mycursor.fetchall()

        for row in rows:
            user_name, password, email, firstname, lastname, status = row
            user_obj = Account(user_name, password, email, firstname, lastname)
            user_dict[user_name] = user_obj

        return user_dict

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
        email = new_user.email
        first_name = new_user.first_name
        last_name = new_user.last_name

        try:
            sql_mode_query = "SET SESSION sql_mode='STRICT_TRANS_TABLES'"
            mycursor.execute(sql_mode_query)

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
            print(f"User Name already exists. Please enter a different User Name.")

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
            print("{:<20} {:<20} {:<30} {:<20} {:<20}".format(
                "User Name", "Password", "E-mail", "First Name", "Last Name"))
            for row in rows:
                user_id, email, password, firstname, lastname = row
                print("{:<20} {:<20} {:<30} {:<20} {:<20} ".format(
                    user_id, email, password, firstname, lastname))
        except mysql.connector.Error as e:
            print(f"Failed to display table: {e}")



    def authenticate_user(self, user_name, password):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )

        try:
            # Create a cursor object to execute SQL statements
            mycursor = db.cursor()

            # Define the SQL statement to retrieve user credentials
            sql = "SELECT * FROM user WHERE user_name = %s AND password = %s"
            val = (user_name, password)

            # Execute the SQL statement
            mycursor.execute(sql, val)

            # Fetch the result
            result = mycursor.fetchone()

            # Close the cursor and connection
            # mycursor.close()

            # Check if the result is not None (i.e., user exists)
            if result:
                user_name, password, email, first_name, last_name = result
                user_account = Account(user_name, password, email, first_name, last_name)
                return user_account



        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return False

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

        # Fetch the result
        result = mycursor.fetchone()
        if result:
            user_id, email, password, first_name, last_name = result
            return Account(user_name, email, password, first_name, last_name)





        # Close the cursor and connection
        # self.mycursor.close()

