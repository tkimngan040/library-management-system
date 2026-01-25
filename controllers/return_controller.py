from datetime import date
from database.db_connection import get_connection
from utils.fine_calculator import calculate_fine


def return_book(member_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Kiểm tra member có mượn sách này không
    cursor.execute("""
        SELECT id, due_date 
        FROM borrow_records
        WHERE member_id = ?
          AND book_id = ?
          AND status = 'Borrowed'
    """, (member_id, book_id))

    record = cursor.fetchone()
    if not record:
        conn.close()
        return False, "Bạn không mượn cuốn sách này."

    record_id, due_date = record
    return_date = date.today()

    # 2. Tính tiền phạt
    overdue_days, fine = calculate_fine(
        date.fromisoformat(due_date),
        return_date
    )

    # 3. Cập nhật borrow record
    cursor.execute("""
        UPDATE borrow_records
        SET return_date = ?, status = 'Returned', fine = ?
        WHERE id = ?
    """, (return_date.isoformat(), fine, record_id))

    # 4. Cập nhật trạng thái sách
    cursor.execute("""
        UPDATE books
        SET status = 'Available', quantity = quantity + 1
        WHERE id = ?
    """, (book_id,))

    # 5. Cập nhật tiền phạt cho member
    if fine > 0:
        cursor.execute("""
            UPDATE users
            SET fine_balance = fine_balance + ?
            WHERE id = ?
        """, (fine, member_id))

    conn.commit()
    conn.close()

    return True, {
        "return_date": return_date,
        "overdue_days": overdue_days,
        "fine": fine
    }

