# models/borrow_record.py
from datetime import datetime, timedelta

class BorrowRecord:
    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = datetime.now().strftime("%Y-%m-%d")
        self.due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        self.return_date = None
        self.status = "Borrowed"
        self.fine = 0
