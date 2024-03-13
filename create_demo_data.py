import pyodbc
from faker import Faker
import os
from dotenv import load_dotenv
fake = Faker()

this_directory = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(this_directory, ".env"))

# Define your connection parameters
server = "localhost\\SQLEXPRESS"  # e.g., 'localhost\SQLEXPRESS'
# server = os.environ.get("server")
database = os.environ.get("database")

# Create a connection string
# This will only work with windows authentication
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"


def insert_schools(n):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for _ in range(n):
                cursor.execute(
                    "INSERT INTO schools (school_name, school_address, school_city, school_state, school_zip) VALUES (?, ?, ?, ?, ?)",
                    fake.company(),
                    fake.street_address(),
                    fake.city(),
                    fake.state(),
                    fake.zipcode(),
                )
            conn.commit()


def insert_students(n, school_id_range):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for _ in range(n):
                cursor.execute(
                    "INSERT INTO students (student_name, date_of_birth, gender, school_id) VALUES (?, ?, ?, ?)",
                    fake.name(),
                    fake.date_of_birth(minimum_age=5, maximum_age=20),
                    fake.random_element(elements=("Male", "Female")),
                    fake.random_int(min=school_id_range[0], max=school_id_range[1]),
                )
            conn.commit()


def insert_student_test_scores(n, student_id_range):
    subjects = ["Math", "Science", "History", "English", "Art"]
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            for _ in range(n):
                cursor.execute(
                    "INSERT INTO student_test_scores (student_id, test_date, test_subject, test_score) VALUES (?, ?, ?, ?)",
                    fake.random_int(min=student_id_range[0], max=student_id_range[1]),
                    fake.date_between(start_date="-1y", end_date="today"),
                    fake.random_element(elements=subjects),
                    fake.random_number(digits=2),
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
    execute_sql("create_tables.sql")
    number_of_schools = 10
    number_of_students = 100
    number_of_test_scores = 1000
    insert_schools(number_of_schools)
    insert_students(
        number_of_students, (1, number_of_schools)
    )  # Assuming school IDs 1 through 10 exist
    insert_student_test_scores(
        number_of_test_scores, (1, number_of_students)
    )  # Assuming student IDs 1 through 100 exist

    1 / 0
