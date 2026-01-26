from database.databaseConnect.db_connect import get_connection


def view_borrow_history(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.title,
               br.borrow_date,
               br.due_date,
               br.return_date,
               br.status,
               br.fine
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE br.member_id = ?
        ORDER BY br.borrow_date DESC
    """, (member_id,))

    records = cursor.fetchall()
    conn.close()
    return records
