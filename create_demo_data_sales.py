import pyodbc
from faker import Faker
import os
from dotenv import load_dotenv

fake = Faker()

this_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(this_directory, ".env"))

# Define your connection parameters
server = "localhost\\SQLEXPRESS"  # Example: 'localhost\SQLEXPRESS'
database = "sales_db"  # Your database name

# Create a connection string
# This will only work with Windows authentication
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"


def insert_customers(n):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for _ in range(n):
                cursor.execute(
                    "INSERT INTO Customers (FirstName, LastName, Email, Phone, Address, City, State, ZipCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    fake.first_name(),
                    fake.last_name(),
                    fake.email(),
                    fake.phone_number(),
                    fake.street_address(),
                    fake.city(),
                    fake.state(),
                    fake.zipcode(),
                )
            conn.commit()

def insert_products(n):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for _ in range(n):
                cursor.execute(
                    "INSERT INTO Products (ProductName, Description, Price, StockQuantity) VALUES (?, ?, ?, ?)",
                    fake.word().capitalize(),
                    fake.text(max_nb_chars=200),
                    fake.random_number(digits=2),
                    fake.random_int(min=10, max=100),
                )
            conn.commit()

def insert_invoices_and_items(n_customers, n_products, n_invoices):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for _ in range(n_invoices):
                customer_id = fake.random_int(min=1, max=n_customers)
                cursor.execute(
                    "INSERT INTO Invoices (CustomerID, InvoiceDate, TotalAmount, PaymentMethod, Status) VALUES (?, ?, ?, ?, ?)",
                    customer_id,
                    fake.date_between(start_date='-2y', end_date='today'),
                    fake.random_number(digits=3),
                    fake.random_element(elements=('Cash', 'Credit Card', 'Online Payment')),
                    fake.random_element(elements=('Paid', 'Pending', 'Cancelled')),
                )
                invoice_id = cursor.execute("SELECT @@IDENTITY AS id;").fetchval()

                # Insert a few invoice items for each invoice
                for _ in range(fake.random_int(min=1, max=5)):  # Each invoice has 1 to 5 items
                    cursor.execute(
                        "INSERT INTO InvoiceItems (InvoiceID, ProductID, Quantity, Price) VALUES (?, ?, ?, ?)",
                        invoice_id,
                        fake.random_int(min=1, max=n_products),
                        fake.random_int(min=1, max=10),  # Quantity
                        fake.random_number(digits=2),  # Price
                    )
            conn.commit()


def execute_sql(file_path):
    with open(file_path, "r") as file:
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
    execute_sql("create_tables_sales.sql")
    # Adjust these numbers based on how much data you want to generate
    num_customers = 100
    num_products = 50
    num_invoices = 200

    insert_customers(num_customers)
    insert_products(num_products)
    insert_invoices_and_items(num_customers, num_products, num_invoices)
