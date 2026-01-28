from database import get_connection
import uuid

class Book:

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT BookID, Title, Author, Category,
                   TotalCopies, AvailableCopies
            FROM Book
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    def create(self, title, author, category, total):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Book
            (BookID, Title, Author, Category, TotalCopies, AvailableCopies)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            title, author, category,
            total, total
        ))
        conn.commit()
        conn.close()

    def delete(self, book_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Book WHERE BookID = ?", (book_id,))
        conn.commit()
        conn.close()

    def get_by_id(self, book_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT BookID, Title, Author, Category,
                   TotalCopies, AvailableCopies
            FROM Book
            WHERE BookID = ?
        """, (book_id,))

        row = cur.fetchone()
        conn.close()
        return row

    def decrease_available(self, book_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Book
            SET AvailableCopies = AvailableCopies - 1
            WHERE BookID = ? AND AvailableCopies > 0
        """, (book_id,))

        conn.commit()
        conn.close()
