import pandas as pd
import sqlite3
import os

# Step 2a: Read csv data
csv_file_path = 'test.csv'
df = pd.read_csv(csv_file_path)

# Step 2b: Open the database
conn = sqlite3.connect('data_tables.db')
cursor = conn.cursor()

# Step 2c: Inspect column names and data types
column_data_types = df.dtypes
columns = df.columns

# Step 2d: Build CREATE TABLE statement dynamically
table_name = os.path.splitext(os.path.basename(csv_file_path))[0]

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

cursor.execute(sql_create_table)
conn.commit()

# Step 2e: Insert csv data in
df.to_sql(table_name, conn, if_exists='append', index=False)


conn.commit()
conn.close()