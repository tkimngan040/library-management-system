import sqlite3

DB_NAME = "library.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Username TEXT UNIQUE,
        Password TEXT,
        Role TEXT
    )
    """)

    # BOOK
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Book (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        Category TEXT,
        Detail TEXT,
        TotalCopies INTEGER,
        AvailableCopies INTEGER
    )
    """)

    # BORROW RECORD
    cur.execute("""
    CREATE TABLE IF NOT EXISTS BorrowRecord (
        BorrowID TEXT PRIMARY KEY,
        UserID TEXT,
        BookID TEXT,
        BorrowDate TEXT,
        DueDate TEXT,
        ReturnDate TEXT,
        Status TEXT
    )
    """)

    # FINE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Fine (
        FineID TEXT PRIMARY KEY,
        BorrowID TEXT,
        Amount INTEGER,
        Status TEXT
    )
    """)

    conn.commit()
    conn.close()
