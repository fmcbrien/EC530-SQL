import pandas as pd
import sqlite3

# Step 1a: Read csv data
csv_file_path = 'sales_data.csv'
df = pd.read_csv(csv_file_path)

# Step 1b: Insert data into sql
conn = sqlite3.connect('data_tables.db')
df.to_sql('sales', conn, if_exists='append', index=False)

# Step 1c: Commit and close connection
conn.commit()
conn.close()