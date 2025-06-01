# db.py


# =========================
# imports
# =========================
import sqlite3


# =========================
# classes
# =========================
class Expense:
    """
    represents an expense entry in the database.
    """
    
    fields = ["id", "date", "category", "name", "amount", "fixed", "comment"]
    
    def __init__(self, id, date, category, name, amount, comment, fixed=0):
        self.id = id
        self.date = date
        self.category = category
        self.name = name
        self.amount = amount
        self.fixed = fixed
        self.comment = comment
    
    def __repr__(self):
        return f"Expense(id={self.id}, date={self.date}, category={self.category}, name={self.name}, amount={self.amount}, fixed={self.fixed}, comment={self.comment})"
    
    def __str__(self):
        return f"{self.id} | {self.date} | {self.category} | {self.name} | {self.amount} | {'Fixed' if self.fixed else 'Variable'} | {self.comment}"



# =========================
# database functions
# =========================

def get_connection():
    """
    return connection to the SQLite database
    """
    return sqlite3.connect("expensesDB.sqlite")


def create_table():
    """
    create the expenses table in the database if it does not exist
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                name TEXT,
                amount REAL NOT NULL,
                fixed BOOLEAN NOT NULL,
                comment TEXT
            )
        """)
        conn.commit()
        

def add_expense(expense):
    """
    add an expense entry to the database
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        fields = [f for f in Expense.fields if f != "id"]
        values = [getattr(expense, k) for k in fields]
        sql = f"INSERT INTO expenses ({', '.join(fields)}) VALUES ({', '.join(['?'] * len(fields))})"
        cursor.execute(sql, values)
        conn.commit()
        

def get_column_names():
    """
    retrieve the column names of the expenses table
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(expenses)")
        columns = [info[1] for info in cursor.fetchall()]
        columns = columns[1:]
        columns = [entry.capitalize() for entry in columns]
        return columns
    

def get_expenses():
    """
    get all expenses from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # retrieve all rows from the expenses table
        sql = "SELECT * FROM expenses"
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        # convert rows to Expense objects
        expenses = []
        for row in rows:
            expense = Expense(*row)
            expenses.append(expense)
        
        return expenses