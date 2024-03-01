import mysql.connector

from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager

user_table_manager = User_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")


tax_table_manager = Tax_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")
#
# # Query the information schema to get primary key information
# #tax_table_manager.drop_tax_table()
# #user_table_manager.drop_user_table()
# #user_table_manager.create_user_table()
# #tax_table_manager.create_tax_table()
db= mysql.connector.connect(host="database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com",
                            user = "admin",
                            passwd = "password",
                            database= "tax_program"
                            )
#user_table_manager.create_user_table()
#tax_table_manager.create_tax_table()

# Create cursor
mycursor = db.cursor()
#mycursor.execute("CREATE DATABASE tax_program")

# Use the database
#mycursor.execute("USE test_encryption")

# Drop the database
#mycursor.execute("DROP DATABASE test_encryption")

# Reconnect to MySQL server
#db.reconnect()

# Execute SHOW DATABASES again to see the updated list
# mycursor.execute("SHOW databases"
#                  "")
# databases = mycursor.fetchall()
#
# # Print the list of databases
# for database in databases:
#     print(database)
user_table_manager.create_user_table()
tax_table_manager.create_tax_table()