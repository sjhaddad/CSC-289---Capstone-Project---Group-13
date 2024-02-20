import mysql.connector
from account import Account


class User_table_manager:

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

    def add_user(self, new_user):
        user_name = new_user.user_name
        password = new_user.password
        email = new_user.email
        first_name = new_user.first_name
        last_name = new_user.last_name

        try:
            sql = "INSERT INTO user (user_name, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
            val = (user_name, password, email, first_name, last_name)

            self.mycursor.execute(sql, val)
            self.db.commit()

            print("User added successfully")
        except mysql.connector.Error as e:
            self.db.rollback()  # Rollback changes if an error occurs
            print(f"Failed to add user: {e}")
        # finally:
        #     self.mycursor.close()  # Close cursor
        #     self.db.close()  # Close database connection

    def delete_user(self, user_id):
        try:
            self.mycursor = self.db.cursor()

            # Define the primary key value of the record you want to delete
            primary_key_value = user_id  # Replace with the specific primary key value

            # Define the SQL query to delete the record with the specified primary key
            sql = "DELETE FROM user WHERE user_name = %s"

            # Execute the SQL query with the primary key value as a parameter
            self.mycursor.execute(sql, (primary_key_value,))

            # Commit the transaction
            self.db.commit()

            print("Record deleted successfully")

        except mysql.connector.Error as e:
            print(f"Error deleting record: {e}")

    def display_table(self):

        try:
            self.mycursor.execute("SELECT * FROM user")
            rows = self.mycursor.fetchall()

            print("\nUser Table:")
            print("{:<10} {:<10} {:<30} {:<20} {:<20}".format(
                "User Name", "Password", "E-mail", "First Name", "Last Name"))
            for row in rows:
                user_id, email, password, firstname, lastname, status = row
                print("{:<10} {:<10} {:<30} {:<20} {:<20} ".format(
                    user_id, email, password, firstname, lastname))
        except mysql.connector.Error as e:
            print(f"Failed to display table: {e}")

    def search_by_user_id(self, user_id):
        mycursor = self.db.cursor()

        query = "SELECT * FROM user WHERE user_id = %s"
        mycursor.execute(query, (user_id,))

        result = mycursor.fetchone()

        if result:
            user_id, email, password, first_name, last_name, status = result

            print(f'\nUser ID: {user_id}')
            print(f'Email: {email}')
            print(f'Password: {password}')
            print(f'First Name: {first_name}')
            print(f'Last Name: {last_name}')
            print(f'Status: {status}')
        else:
            print("Item not found")



