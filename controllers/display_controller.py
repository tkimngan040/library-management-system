from database.db_connection import get_db_connection

class DisplayController:
    """
    Hiển thị danh sách & chi tiết sách
    """

    @staticmethod
    def get_all_books():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()

        books = []
        for r in rows:
            books.append({
                "book_id": r[0],
                "title": r[1],
                "author": r[2],
                "category": r[3],
                "total_copies": r[4],
                "available_copies": r[5],
                "description": r[6]
            })
        return books

    @staticmethod
    def get_book_details(book_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        r = cursor.fetchone()
        conn.close()

        if not r:
            return None

        return {
            "book_id": r[0],
            "title": r[1],
            "author": r[2],
            "category": r[3],
            "total_copies": r[4],
            "available_copies": r[5],
            "description": r[6]
        }
