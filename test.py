from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import uuid
from datetime import datetime, timedelta
from user_table_manager import User_table_manager
from tax_table_manager import Tax_table_manager
from tax_record import TaxRecord
from account import Account
from flask_mail import Mail, Message
from constants import *

user_table_manager = User_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                        "password",
                                        database="tax_program")
tax_table_manager = Tax_table_manager("database-2.cl6g04m6q6id.us-east-1.rds.amazonaws.com", "admin",
                                      "password",
                                      database="tax_program")


# Execute an SQL query to retrieve the list of tables in the database
# tax_table_manager.drop_tax_table()
tax_table_manager.mycursor.execute("SHOW TABLES")

# Fetch all rows from the result set
tables = tax_table_manager.mycursor.fetchall()

# Display the list of tables
print("Tables in the database:")
for table in tables:
    print(table[0])  # Assuming the table name is the first element in each row

# Create tax table
#tax_table_manager.create_tax_table()