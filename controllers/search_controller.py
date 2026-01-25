from database.db_connection import get_db_connection
class SearchController:
    """
    Đúng theo Use Case 2.2 Search Book trong tiểu luận
    """
    @staticmethod
    def search_books(keyword=None, category=None, sort_by=None, ascending=True):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        # Search by title keyword
        if keyword:
            query += " AND title LIKE ?"
            params.append(f"%{keyword}%")

        # Filter by category
        if category:
            query += " AND category LIKE ?"
            params.append(f"%{category}%")

        cursor.execute(query, params)
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
 # Sorting theo yêu cầu tiểu luận
        if sort_by:
            books = sorted(
                books,
                key=lambda x: x[sort_by],
                reverse=not ascending
            )

        return books
