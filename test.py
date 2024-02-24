import mysql.connector

from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager

user_table_manager = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                             "mypassword",
                                             database="new_tax_table")


tax_table_manager = Tax_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                             "mypassword",
                                             database="new_tax_table")

# Query the information schema to get primary key information
#tax_table_manager.drop_tax_table()
#user_table_manager.drop_user_table()
#user_table_manager.create_user_table()
#tax_table_manager.create_tax_table()
db= mysql.connector.connect(host="database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com",
                            user = "admin",
                            passwd = "mypassword",
                            database= "new_tax_table"
                            )
#user_table_manager.create_user_table()
#tax_table_manager.create_tax_table()

mycursor = db.cursor()
mycursor.execute("show databases")
databases = mycursor.fetchall()

    # Print the list of databases
for database in databases:
    print(database)