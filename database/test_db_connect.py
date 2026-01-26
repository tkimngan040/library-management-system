"""
Test database connection (SQLite) and initialize DB if missing.
Run from project root: python Database/test_db_connect.py
"""
import os
import config
from database.db_connection import DatabaseConnection

def test_connection(init_if_missing=True):
    conn = None
    try:
        conn = DatabaseConnection.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
        row = cur.fetchone()
        if row:
            print("Successfully connected to SQLite DB at:", config.DB_PATH)
            print("Found table:", row[0])
        else:
            print("Connected to SQLite DB but no tables found.")
            if init_if_missing:
                try:
                    from database.init_db import initialize_database
                    print("Initializing database...")
                    initialize_database()
                    print("Initialization complete. Re-testing connection...")
                    conn.close()
                    conn = DatabaseConnection.get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
                    row = cur.fetchone()
                    if row:
                        print("Database initialized and table found:", row[0])
                except Exception as e:
                    print("Failed to initialize database:", e)
    except Exception as e:
        print("Database connection error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    test_connection()
