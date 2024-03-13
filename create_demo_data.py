import pyodbc

# Define your connection parameters
server = 'localhost\\SQLEXPRESS'  # e.g., 'localhost\SQLEXPRESS'
database = 'test_db'

# Create a connection string
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

def execute_sql(file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read()
    try:
        # Connect to the database
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

if __name__ == "__main__":
    # create tables
    execute_sql("create_tables.sql")

    1/0
