import mysql.connector

# Let's build a connection to MySQL DB
def get_connection():
    try:
        print("Attempting to connect to the database...")
        connection = mysql.connector.connect(
            host="localhost",           
            user="root",                
            password="root",   
            database="mental_health_app"  
        )
        print("Database connection established. Yeahhh")
        return connection
    except Exception as e:
        print(f"Error while connecting to the database: {e}")
        raise



# Adding SQLite for testing additional functionalities like CBT

import sqlite3

def get_sqlite_connection(): # Returns a connection to the SQLite database.

    try:
        connection = sqlite3.connect("db/thought_logs.db")  # Path to SQLite DB
        return connection
    except sqlite3.Error as e:
        print(f"SQLite connection error: {e}")
        raise

def initialize_sqlite_db(): # Initializes the SQLite database with the required schema.

    try:
        connection = get_sqlite_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS thought_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        print("SQLite database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing SQLite DB: {e}")
    finally:
        if connection:
            connection.close()


def log_category_to_sqlite(categories):
    """
    Logs thought categories into the SQLite database.
    :param categories: List of classified categories
    """
    try:
        connection = get_sqlite_connection()
        cursor = connection.cursor()
        for category in categories:
            cursor.execute("INSERT INTO thought_logs (category) VALUES (?)", (category,))
        connection.commit()
        print("Categories logged successfully to SQLite.")
    except sqlite3.Error as e:
        print(f"Error while logging categories to SQLite: {e}")
        raise
    finally:
        if connection:
            cursor.close()
            connection.close()

import pandas as pd

# Fetch recurring thought categories from SQLite. This will return a DataFrame with categories and their counts.
def fetch_recurring_themes():

    try:
        connection = get_sqlite_connection()
        query = """
        SELECT 
            category, 
            COUNT(*) AS count 
        FROM thought_logs
        GROUP BY category
        ORDER BY count DESC;
        """
        themes = pd.read_sql(query, connection)
        return themes
    except Exception as e:
        print(f"Error fetching recurring themes from SQLite: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()