from database.db_connection import DatabaseConnection
from datetime import datetime, timedelta
import config

class BorrowRecord:
    """Borrow record model class"""
    
    def __init__(self, record_id=None, user_id=None, book_id=None, borrow_date=None,
                 due_date=None, return_date=None, status='Borrowed', overdue_days=0,
                 fine_amount=0, book_title=None, member_name=None):
        self.record_id = record_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        self.overdue_days = overdue_days
        self.fine_amount = fine_amount
        self.book_title = book_title
        self.member_name = member_name
    
    @staticmethod
    def create_borrow_record(user_id, book_id):
        """Create new borrow record"""
        borrow_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        due_date = (datetime.now() + timedelta(days=config.BORROW_PERIOD_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
        
        query = '''
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status)
            VALUES (?, ?, ?, ?, 'Borrowed')
        '''
        
        try:
            record_id = DatabaseConnection.execute_update(
                query,
                (user_id, book_id, borrow_date, due_date)
            )
            return record_id
        except Exception as e:
            raise Exception(f"Error creating borrow record: {str(e)}")
    
    @staticmethod
    def get_user_borrow_records(user_id, status=None):
        """Get borrow records for a user"""
        if status:
            query = '''
                SELECT br.*, b.title as book_title, u.full_name as member_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.user_id = ? AND br.status = ?
                ORDER BY br.borrow_date DESC
            '''
            results = DatabaseConnection.execute_query(query, (user_id, status))
        else:
            query = '''
                SELECT br.*, b.title as book_title, u.full_name as member_name
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.user_id = ?
                ORDER BY br.borrow_date DESC
            '''
            results = DatabaseConnection.execute_query(query, (user_id,))
        
        return [BorrowRecord(**dict(row)) for row in results]
    
    @staticmethod
    def get_all_borrow_records():
        """Get all borrow records"""
        query = '''
            SELECT br.*, b.title as book_title, u.full_name as member_name
            FROM borrow_records br
            JOIN books b ON br.book_id = b.book_id
            JOIN users u ON br.user_id = u.user_id
            ORDER BY br.borrow_date DESC
        '''
        results = DatabaseConnection.execute_query(query)
        return [BorrowRecord(**dict(row)) for row in results]
    
    @staticmethod
    def count_active_borrows(user_id):
        """Count active borrows for a user"""
        query = '''
            SELECT COUNT(*) as count 
            FROM borrow_records 
            WHERE user_id = ? AND status = 'Borrowed'
        '''
        result = DatabaseConnection.execute_query(query, (user_id,))
        return result[0]['count']
    
    @staticmethod
    def has_overdue_books(user_id):
        """Check if user has overdue books"""
        query = '''
            SELECT COUNT(*) as count 
            FROM borrow_records 
            WHERE user_id = ? AND status = 'Borrowed' 
            AND datetime(due_date) < datetime('now')
        '''
        result = DatabaseConnection.execute_query(query, (user_id,))
        return result[0]['count'] > 0
    
    @staticmethod
    def update_record(record_id, **kwargs):
        """Update borrow record"""
        allowed_fields = ['return_date', 'status', 'overdue_days', 'fine_amount']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(record_id)
        query = f"UPDATE borrow_records SET {', '.join(updates)} WHERE record_id = ?"
        
        try:
            DatabaseConnection.execute_update(query, tuple(values))
            return True
        except Exception as e:
            raise Exception(f"Error updating record: {str(e)}")
