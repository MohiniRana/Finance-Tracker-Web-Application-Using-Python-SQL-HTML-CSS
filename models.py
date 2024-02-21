# models.py

import sqlite3

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database schema
def initialize_database():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                store_id INTEGER NOT NULL,
                FOREIGN KEY (store_id) REFERENCES store (id)
            )
        ''')

# Initialize the database schema
initialize_database()

class Store:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color

class Expense:
    def __init__(self, id, amount, description, store_id):
        self.id = id
        self.amount = amount
        self.description = description
        self.store_id = store_id
