from databaseConnect.db_connect import get_connection
from datetime import datetime

#USER MODEL
class User:
    def __init__(self, user_id=None, username=None, password=None,
                 full_name=None, email=None, phone=None,
                 role="Member", status="Active", created_date=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.role = role
        self.status = status
        self.created_date = created_date or datetime.now()

    @staticmethod
    def get_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [User] WHERE user_id = ?", user_id)
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def get_by_username(username):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [User] WHERE username = ?", username)
        row = cursor.fetchone()
        conn.close()
        return row

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO [User] (username, password, full_name, email, phone, role, status, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.username, self.password, self.full_name,
            self.email, self.phone, self.role, self.status, self.created_date
        ))
        conn.commit()
        conn.close()


#CATEGORY MODEL
class Category:
    def __init__(self, category_id=None, category_name=None, description=None):
        self.category_id = category_id
        self.category_name = category_name
        self.description = description

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Category")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Category (category_name, description)
            VALUES (?, ?)
        """, (self.category_name, self.description))
        conn.commit()
        conn.close()


#BOOK MODEL
class Book:
    def __init__(self, book_id=None, title=None, author=None,
                 category_id=None, description=None,
                 detailed_info=None, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category_id = category_id
        self.description = description
        self.detailed_info = detailed_info
        self.status = status

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Book")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Book (title, author, category_id, description, detailed_info, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.title, self.author, self.category_id,
            self.description, self.detailed_info, self.status
        ))
        conn.commit()
        conn.close()



# BORROW RECORD MODEL
class BorrowRecord:
    def __init__(self, borrow_id=None, user_id=None, book_id=None,
                 borrow_date=None, due_date=None, return_date=None,
                 overdue_days=0, fine_amount=0, status="Borrowed"):
        self.borrow_id = borrow_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date or datetime.now()
        self.due_date = due_date
        self.return_date = return_date
        self.overdue_days = overdue_days
        self.fine_amount = fine_amount
        self.status = status

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO BorrowRecord
            (user_id, book_id, borrow_date, due_date, return_date,
             overdue_days, fine_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.user_id, self.book_id, self.borrow_date,
            self.due_date, self.return_date,
            self.overdue_days, self.fine_amount, self.status
        ))
        conn.commit()
        conn.close()
