from models.borrow_record import BorrowRecord

class HistoryController:
    @staticmethod
    def get_user_history(user_id, filter_status=None):
        return BorrowRecord.get_user_borrow_records(user_id, status=filter_status)
    
    @staticmethod
    def get_all_borrow_records():
        return BorrowRecord.get_all_borrow_records()
