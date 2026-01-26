from models.book import Book
from models.user import User
from models.borrow_record import BorrowRecord
from datetime import datetime
import config

class ReturnController:
    @staticmethod
    def calculate_fine(due_date_str, return_date_str):
        due = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S')
        ret = datetime.strptime(return_date_str, '%Y-%m-%d %H:%M:%S')
        
        if ret <= due:
            return 0, 0
        
        overdue_days = (ret - due).days
        fine = overdue_days * config.FINE_PER_DAY
        return overdue_days, fine
    
    @staticmethod
    def return_book(record_id):
        try:
            records = BorrowRecord.get_all_borrow_records()
            record = next((r for r in records if r.record_id == record_id), None)
            
            if not record:
                return False, "Record not found"
            
            if record.status != 'Borrowed':
                return False, "Already returned"
            
            return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            overdue_days, fine = ReturnController.calculate_fine(record.due_date, return_date)
            
            BorrowRecord.update_record(record_id, return_date=return_date, status='Returned',
                                      overdue_days=overdue_days, fine_amount=fine)
            Book.update_quantity(record.book_id, 1)
            
            if fine > 0:
                user = User.get_user_by_id(record.user_id)
                User.update_user(record.user_id, fine_balance=user.fine_balance + fine)
                return True, f"Returned. Overdue: {overdue_days} days. Fine: {fine:,.0f} VND"
            
            return True, "Book returned successfully!"
        except Exception as e:
            return False, str(e)

