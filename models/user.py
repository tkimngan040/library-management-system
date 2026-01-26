import bcrypt
from database.db_connection import DatabaseConnection
from datetime import datetime

class User:
    """User model class"""
    
    def __init__(self, user_id=None, username=None, password=None, full_name=None, 
                 email=None, phone=None, role=None, account_status='Active', 
                 fine_balance=0, created_date=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.role = role
        self.account_status = account_status
        self.fine_balance = fine_balance
        self.created_date = created_date
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user credentials"""
        query = "SELECT * FROM users WHERE username = ?"
        results = DatabaseConnection.execute_query(query, (username,))
        
        if results:
            user_data = dict(results[0])
            stored_password = user_data['password']
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return User(**user_data)
        
        return None
    
    @staticmethod
    def create_user(username, password, full_name, email, phone, role):
        """Create new user"""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        query = '''
            INSERT INTO users (username, password, full_name, email, phone, role)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        try:
            user_id = DatabaseConnection.execute_update(
                query, 
                (username, hashed_password.decode('utf-8'), full_name, email, phone, role)
            )
            return user_id
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = ?"
        results = DatabaseConnection.execute_query(query, (user_id,))
        
        if results:
            return User(**dict(results[0]))
        return None
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        query = "SELECT * FROM users ORDER BY user_id DESC"
        results = DatabaseConnection.execute_query(query)
        return [User(**dict(row)) for row in results]
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user information"""
        allowed_fields = ['full_name', 'email', 'phone', 'account_status', 'fine_balance']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
        
        try:
            DatabaseConnection.execute_update(query, tuple(values))
            return True
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        user = User.get_user_by_id(user_id)
        
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            return False, "Incorrect old password"
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        query = "UPDATE users SET password = ? WHERE user_id = ?"
        try:
            DatabaseConnection.execute_update(query, (hashed_password.decode('utf-8'), user_id))
            return True, "Password changed successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        # Check if user has active borrows
        query = "SELECT COUNT(*) as count FROM borrow_records WHERE user_id = ? AND status = 'Borrowed'"
        result = DatabaseConnection.execute_query(query, (user_id,))
        
        if result[0]['count'] > 0:
            raise Exception("Cannot delete user with active borrows")
        
        query = "DELETE FROM users WHERE user_id = ?"
        DatabaseConnection.execute_update(query, (user_id,))
