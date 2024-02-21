from user_table_manager import User_table_manager

user_table_manager = User_table_manager("database-2.cvi44qi26x3h.us-east-2.rds.amazonaws.com", "admin",
                                             "mypassword",
                                             database="Tax_Calculator")
# Query the information schema to get primary key information
user_table_manager.mycursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = 'user'
        AND CONSTRAINT_NAME = 'PRIMARY'
    """)

# Fetch the result
primary_key_column =  user_table_manager.mycursor.fetchone()

if primary_key_column:
    print(f"The primary key column is: {primary_key_column[0]}")
else:
    print("No primary key found for the specified table.")


