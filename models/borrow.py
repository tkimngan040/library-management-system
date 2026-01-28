from database import get_connection
from datetime import date, timedelta
import uuid

class Borrow:

    @staticmethod
    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT b.BorrowID, u.Username, bk.Title,
                   b.BorrowDate, b.Status
            FROM BorrowRecord b
            JOIN Users u ON b.UserID = u.UserID
            JOIN Book bk ON b.BookID = bk.BookID
        """)
        rows = cur.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def create(user_id, book_id):
        conn = get_connection()
        cur = conn.cursor()

        borrow_id = str(uuid.uuid4())[:8]
        today = date.today()
        due = today + timedelta(days=7)

        cur.execute("""
        INSERT INTO BorrowRecord
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            borrow_id,
            user_id,
            book_id,
            today.isoformat(),
            due.isoformat(),
            None,
            "Borrowed"
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def return_book(borrow_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT BookID, DueDate
        FROM BorrowRecord
        WHERE BorrowID=?
        """, (borrow_id,))
        book_id, due = cur.fetchone()

        today = date.today()

        # update borrow
        cur.execute("""
        UPDATE BorrowRecord
        SET ReturnDate=?, Status='Returned'
        WHERE BorrowID=?
        """, (today.isoformat(), borrow_id))

        # update book
        cur.execute("""
        UPDATE Book
        SET AvailableCopies = AvailableCopies + 1
        WHERE BookID=?
        """, (book_id,))

        # fine
        if today > date.fromisoformat(due):
            days = (today - date.fromisoformat(due)).days
            fine_id = str(uuid.uuid4())[:8]
            amount = days * 5000

            cur.execute("""
            INSERT INTO Fine VALUES (?, ?, ?, ?)
            """, (fine_id, borrow_id, amount, "Unpaid"))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT br.BorrowID, b.Title, br.BorrowDate,
               br.ReturnDate, br.Status
        FROM BorrowRecord br
        JOIN Book b ON br.BookID=b.BookID
        WHERE br.UserID=?
        """, (user_id,))

        rows = cur.fetchall()
        conn.close()
        return rows
