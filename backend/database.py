# Import required libraries
import sqlite3
from backend.models import Base

# Create the database connection
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except sqlite3.Error as e:
        print(e)

# Create the tables
def create_table(table_name, model):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(model.__table__.create(conn))
    conn.commit()
