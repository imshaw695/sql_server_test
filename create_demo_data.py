import pyodbc

# Define your connection parameters
server = 'localhost/'  # e.g., 'localhost\SQLEXPRESS'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
# For Windows authentication, you can use Trusted_Connection=yes instead of username and password

# Create a connection string
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# SQL file path
sql_file_path = 'path_to_your_sql_file.sql'

# Read the SQL query from the file
with open(sql_file_path, 'r') as file:
    sql_query = file.read()

# Connect to the database
try:
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            # Execute the SQL query
            cursor.execute(sql_query)
            # If your query is a SELECT statement, you may want to fetch the results
            # For other types of statements like CREATE, INSERT, UPDATE, or DELETE, you might want to commit the transaction
            conn.commit()  # Only if needed, for example, for DML statements. Comment out for SELECT statements.
    print("Query executed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
