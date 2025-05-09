# 🧠 SQL Assistant CLI with OpenAI & SQLite

This is a command-line based interactive assistant that helps you:
- Load CSV files into a local SQLite database.
- Run SQL queries manually or via plain text instructions.
- Interact with OpenAI's API to automatically generate SQL queries from natural language.
- View and manage your database tables easily.

---

## 🔧 Features

- **CSV to SQLite Importing**: Load `.csv` files into a SQLite database with automatic schema detection.
- **Interactive SQL Execution**: Run custom SQL queries directly in the terminal.
- **Natural Language to SQL**: Use OpenAI's GPT model to convert plain English instructions into SQL.
- **Database Management**: View table names, handle schema conflicts, and choose to overwrite, rename, or skip.
- **Error Logging**: All errors are logged in `error_log.txt` for debugging purposes.

---

## 📁 Project Structure

```
├── main.py # Main interactive assistant script
├── error_log.txt # Log file for runtime errors
├── data_tables.db # SQLite database (auto-generated)
└── README.md # You're here!
```


---

## 🚀 Getting Started

### 1. **Install Requirements**

Ensure you have Python 3.7+ and install required packages:

```bash
pip install pandas openai
```

### 2. Set Your OpenAI API Key

Replace the following placeholder in the code with your actual OpenAI API Key:
```python
client = OpenAI(
    api_key = "sk-..."  # <--- Replace this
)
```

### 3. Run the Assistant

```bash
python csv_to_db.py
```
---

### Usage

When running the CLI, you'll be prompted with options:
- `load`: Load a CSV file into the database.
- `query`: Enter a raw SQL query.
- `plain text`: Enter a plain English request (e.g. "show all users over 30").
- `list`: List all tables in the database.
- `exit`: Quit the assistant.

---

### Warnings and Notes
- Ensure your CSV files have valid headers and content
- All databasae interactions affect `data_tables.db` in the local directory
- The API key is hardcoded in the script for simplicity
- This script logs errors to `error_log.txt`

---

###Example

```bash
What would you like to do? (load, query, list, plain text, exit): plain text
Enter your instruction: show all employees with salary over 50000

Generated SQL Query: SELECT * FROM employees WHERE salary > 50000;
```
