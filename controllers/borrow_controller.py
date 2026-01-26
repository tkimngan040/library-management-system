# controllers/borrow_controller.py
from datetime import datetime, timedelta
from database.db_connection import get_connection

# Giới hạn số sách được mượn tối đa
MAX_BORROW_LIMIT = 5

def check_borrow_eligibility(user_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Kiểm tra trạng thái tài khoản và tiền phạt
    cursor.execute("SELECT status, fine_balance FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        return False, "Không tìm thấy thành viên."

    status, fine_balance = user
    if status == "locked":
        return False, "Tài khoản đã bị khóa."

    if fine_balance > 0:
        return False, "Bạn còn nợ tiền phạt."

    # 2. Kiểm tra sách quá hạn
    cursor.execute("""
        SELECT COUNT(*) FROM borrow_records
        WHERE user_id=? AND status='Borrowed' AND due_date < date('now')
    """, (user_id,))
    overdue = cursor.fetchone()[0]
    if overdue > 0:
        return False, "Bạn đang có sách quá hạn."

    # 3. Kiểm tra số lượng sách đang mượn
    cursor.execute("""
        SELECT COUNT(*) FROM borrow_records
        WHERE user_id=? AND status='Borrowed'
    """, (user_id,))
    count = cursor.fetchone()[0]
    if count >= MAX_BORROW_LIMIT:
        return False, "Đã vượt quá giới hạn mượn sách (tối đa 5 cuốn)."

    # 4. Kiểm tra tình trạng sách
    cursor.execute("SELECT status, quantity FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    if not book:
        return False, "Không tìm thấy sách."

    status, quantity = book
    if status != "Available" or quantity <= 0:
        return False, "Sách hiện không khả dụng."

    return True, "Đủ điều kiện mượn sách."


def create_borrow_record(user_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Ngày mượn
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    
    # Ngày hết hạn sau 14 ngày
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Lưu thông tin mượn sách vào bảng borrow_records
    cursor.execute("""
        INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status)
        VALUES (?, ?, ?, ?, 'Borrowed')
    """, (user_id, book_id, borrow_date, due_date))

    # Cập nhật trạng thái và số lượng sách
    cursor.execute("""
        UPDATE books
        SET quantity = quantity - 1,
            status = 'Borrowed'
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    return due_date


def borrow_book(user_id, book_id):
    # Kiểm tra điều kiện mượn sách
    eligible, message = check_borrow_eligibility(user_id, book_id)
    if not eligible:
        return False, message

    # Tạo bản ghi mượn sách
    due_date = create_borrow_record(user_id, book_id)
    return True, f"Mượn sách thành công. Hạn trả: {due_date}"
