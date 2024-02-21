from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database schema
def initialize_database():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                store TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT
            )
        ''')
        conn.commit()

# Initialize the database schema
initialize_database()
@app.route('/')
def home():
    return render_template('home.html')

# Route to display home.html first and then navigate to the expense tracker
@app.route('/expense_tracker')
def expense_tracker():
    return render_template('home.html', redirect=True)  # Pass redirect parameter to home.html

@app.route('/index')
def index():
    with get_db_connection() as conn:
        cursor = conn.execute('SELECT * FROM expenses')
        expenses = cursor.fetchall()
        total_expenses = sum(expense['amount'] for expense in expenses)
    return render_template('index.html', expenses=expenses, total_expenses=total_expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        if request.method == 'POST':
            description = request.form['description']
            amount = request.form['amount']
            store = request.form['store']
            with get_db_connection() as conn:
                conn.execute('INSERT INTO expenses (description, amount, store) VALUES (?, ?, ?)', (description, amount, store))
                conn.commit()
        return jsonify({"message": "Expense added successfully"}), 201
    except Exception as e:
        return str(e), 500

@app.route('/edit_expense/<int:expense_id>', methods=['POST'])
def edit_expense(expense_id):
    try:
        if request.method == 'POST':
            amount = float(request.form['amount'])
            description = request.form['description']
            store = request.form['store']
            with get_db_connection() as conn:
                conn.execute('UPDATE expenses SET amount = ?, description = ?, store = ? WHERE id = ?', (amount, description, store, expense_id))
                conn.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return str(e), 500

@app.route('/delete_expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    try:
        with get_db_connection() as conn:
            conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
            conn.commit()
        return jsonify({"message": "Expense deleted successfully"}), 200
    except Exception as e:
        return str(e), 500
        
@app.route('/get_expense/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    try:
        with get_db_connection() as conn:
            expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        return jsonify(dict(expense))
    except Exception as e:
        return str(e), 500

@app.route('/get_stores', methods=['GET'])
def get_stores():
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM store')
            stores = cursor.fetchall()
        return jsonify(stores)
    except Exception as e:
        return str(e), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5004)
