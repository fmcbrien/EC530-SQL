import pandas as pd
import sqlite3
import os
import sys
import traceback

def log_error(error_message):
    with open('error_log.txt', 'a') as error_log:
        error_log.write(f"{error_message}\n")

# Step 2a: Read csv data
csv_file_path = 'test.csv'

table_name = os.path.splitext(os.path.basename(csv_file_path))[0]

try:
    df = pd.read_csv(csv_file_path)
except Exception as e:
    error_message = f"Error reading CSV file: {str(e)}"
    log_error(error_message)
    sys.exit(error_message)

# Step 2b: Open the database
conn = sqlite3.connect('data_tables.db')
cursor = conn.cursor()

# Step 3a: PRAGMA table_info to detect existing schema
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

# Step 2c: Inspect column names and data types
column_data_types = df.dtypes
columns = df.columns

# Step 2d: Build CREATE TABLE statement dynamically
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

# Step 2e: Insert csv data in
try:
    df.to_sql(table_name, conn, if_exists='replace', index=False)
except Exception as e:
    error_message = f"Error inserting data into table '{table_name}': {str(e)}"
    log_error(error_message)
    conn.close()
    sys.exit(error_message)

conn.commit()
conn.close()