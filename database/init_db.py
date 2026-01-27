import sqlite3
import os
import config
import bcrypt

def initialize_database():
    data_dir = os.path.dirname(config.DB_PATH)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    
    data_dir = os.path.dirname(config.DB_PATH)
    os.makedirs(data_dir, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL,
            account_status TEXT DEFAULT 'Active',
            fine_balance REAL DEFAULT 0,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category_id INTEGER,
            description TEXT,
            detailed_info TEXT,
            total_quantity INTEGER DEFAULT 1,
            available_quantity INTEGER DEFAULT 1,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT DEFAULT 'Borrowed',
            overdue_days INTEGER DEFAULT 0,
            fine_amount REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)

    try:
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT INTO users (username, password, full_name, role)
            VALUES (?, ?, ?, ?)
        """, ('admin', hashed_password.decode('utf-8'), 'System Administrator', 'Admin'))
    except sqlite3.IntegrityError:
        pass

    try:
        hashed_password = bcrypt.hashpw('member123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("""
            INSERT INTO users (username, password, full_name, email, role)
            VALUES (?, ?, ?, ?, ?)
        """, ('john_doe', hashed_password.decode('utf-8'), 'John Doe', 'john@example.com', 'Member'))
    except sqlite3.IntegrityError:
        pass

    categories = [
        ('Fiction', 'Fictional literature'),
        ('Science', 'Scientific books'),
        ('History', 'Historical books'),
        ('Technology', 'Technology and programming'),
        ('Art', 'Art and design books')
    ]

    for cat_name, cat_desc in categories:
        try:
            cursor.execute('INSERT INTO categories (category_name, description) VALUES (?, ?)',
                         (cat_name, cat_desc))
        except sqlite3.IntegrityError:
            pass

    sample_books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', 1, 'A classic American novel', 'Detailed info about The Great Gatsby', 3, 3),
        ('1984', 'George Orwell', 1, 'Dystopian social science fiction', 'Detailed info about 1984', 2, 2),
        ('A Brief History of Time', 'Stephen Hawking', 2, 'Popular science book', 'Detailed info about physics', 4, 4),
        ('Sapiens', 'Yuval Noah Harari', 3, 'A brief history of humankind', 'Detailed info about human history', 5, 5),
        ('Clean Code', 'Robert C. Martin', 4, 'A handbook of agile software craftsmanship', 'Programming best practices', 3, 3)
    ]

    for book in sample_books:
        try:
            cursor.execute("""
                INSERT INTO books (title, author, category_id, description, detailed_info, total_quantity, available_quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, book)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print("Database initialized successfully!")