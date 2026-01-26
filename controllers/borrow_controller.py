from models.book import Book
from models.user import User
from models.borrow_record import BorrowRecord
import config

class BorrowController:
    @staticmethod
    def check_borrow_eligibility(user_id, book_id):
        user = User.get_user_by_id(user_id)
        if not user:
            return False, "User not found"
        
        if user.account_status == config.ACCOUNT_LOCKED:
            return False, "Account is locked"
        
        if user.fine_balance > 0:
            return False, f"Unpaid fines: {user.fine_balance:,.0f} VND"
        
        active_borrows = BorrowRecord.count_active_borrows(user_id)
        if active_borrows >= config.MAX_BOOKS_PER_MEMBER:
            return False, f"Max limit reached ({config.MAX_BOOKS_PER_MEMBER} books)"
        
        if BorrowRecord.has_overdue_books(user_id):
            return False, "You have overdue books"
        
        book = Book.get_book_by_id(book_id)
        if not book or book.available_quantity <= 0:
            return False, "Book not available"
        
        return True, "Eligible"
    
    @staticmethod
    def borrow_book(user_id, book_id):
        eligible, message = BorrowController.check_borrow_eligibility(user_id, book_id)
        if not eligible:
            return False, message
        
        try:
            record_id = BorrowRecord.create_borrow_record(user_id, book_id)
            Book.update_quantity(book_id, -1)
            return True, f"Book borrowed! Record ID: {record_id}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_user_borrowed_books(user_id):
        return BorrowRecord.get_user_borrow_records(user_id, status='Borrowed')
