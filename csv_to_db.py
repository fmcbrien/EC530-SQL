import pandas as pd
import sqlite3
import os
import sys

# Function to log errors encountered
def log_error(error_message):
    with open('error_log.txt', 'a') as error_log:
        error_log.write(f"{error_message}\n")

# Function to load a CSV into the SQLite database
def csv_to_db(csv_file_path, conn):

    table_name = os.path.splitext(os.path.basename(csv_file_path))[0]

    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        error_message = f"Error reading CSV file: {str(e)}"
        log_error(error_message)
        sys.exit(error_message)

    conn = sqlite3.connect('data_tables.db')
    cursor = conn.cursor()

    # PRAGMA table_info to detect existing schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_cols = cursor.fetchall()

    if existing_cols:
        print(f"Table '{table_name}' already exists. The existing schema is:")
        for column in existing_cols:
            print(f"Column: {column[1]}, Type: {column[2]}")

        user_choice = input("Choose action - Overwrite (O), Rename (R), or Skip (S): ").strip().lower()
        
        if user_choice == 'o':
            print("Overwriting the table...")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        elif user_choice == 'r':
            new_table_name = input(f"Enter new name for the table (default: {table_name}_new): ").strip()
            if not new_table_name:
                new_table_name = f"{table_name}_new"
            table_name = new_table_name
            print(f"Renaming the table to '{table_name}'...")
        elif user_choice == 's':
            print("Skipping table creation.")
            conn.close()
            sys.exit("Skipping table creation.")

    # Inspect column names and data types
    column_data_types = df.dtypes
    columns = df.columns

    # Build CREATE TABLE statement dynamically
    sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    for column, dtype in zip(columns, column_data_types):
        if dtype == 'int64':
            sql_type = 'INTEGER'
        elif dtype == 'float64':
            sql_type = 'REAL'
        elif dtype == 'bool':
            sql_type = 'BOOLEAN'
        else:
            sql_type = 'TEXT'

        sql_create_table += f"{column} {sql_type}, "

    sql_create_table = sql_create_table.rstrip(', ') + ");"

    try:
        cursor.execute(sql_create_table)
        conn.commit()
    except Exception as e:
        error_message = f"Error creating table '{table_name}': {str(e)}"
        log_error(error_message)
        conn.close()
        sys.exit(error_message)

    # Insert csv data in database
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        error_message = f"Error inserting data into table '{table_name}': {str(e)}"
        log_error(error_message)
        conn.close()
        sys.exit(error_message)

    conn.commit()

# Function to perform SQL queries
def execute_sql_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            conn.commit()
            print("Query executed successfully.")
    except Exception as e:
        log_error(f"Error executing query: {str(e)}")
        print(f"Error executing query: {str(e)}")

# Function to list all tables in the database
def list_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in the database.")
    except Exception as e:
        log_error(f"Error listing tables: {str(e)}")
        print(f"Error listing tables: {str(e)}")

# Main function to simulate the interactive assistant
def interactive_assistant():
    print("Welcome to the Database Assistant using Python CLI")
    print("You can load CSV files, run SQL queries, list tables, or exit.")

    # Connect to the SQLite database
    conn = sqlite3.connect('data_tables.db')

    while True:
        # Display the prompt and get user input
        user_input = input("\nWhat would you like to do? (load, query, list, exit): ").strip().lower()

        if user_input == "load":
            # Prompt user for CSV file path
            csv_file_path = input("Enter the path to the CSV file: ").strip()
            if os.path.exists(csv_file_path) and csv_file_path.endswith(".csv"):
                csv_to_db(csv_file_path, conn)
            else:
                print("Invalid file path or not a CSV file. Please try again.")
        
        elif user_input == "query":
            # Prompt user for SQL query
            sql_query = input("Enter your SQL query: ").strip()
            if sql_query:
                execute_sql_query(conn, sql_query)
            else:
                print("Please enter a valid SQL query.")

        elif user_input == "list":
            # List all tables in the database
            list_tables(conn)

        elif user_input == "exit":
            print("Goodbye!")
            break  # Exit the loop and end the program

        else:
            print("Invalid input. Please type 'load', 'query', 'list', or 'exit'.")

    # Close the database connection when done
    conn.close()

if __name__ == "__main__":
    interactive_assistant()