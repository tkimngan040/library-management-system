from models.book import Book
from models.user import User

class AdminController:
    @staticmethod
    def add_book(title, author, category_id, description, detailed_info, quantity):
        try:
            book_id = Book.create_book(title, author, category_id, description, detailed_info, quantity)
            return True, f"Book added successfully with ID: {book_id}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def update_book(book_id, **kwargs):
        try:
            Book.update_book(book_id, **kwargs)
            return True, "Book updated successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_book(book_id):
        try:
            Book.delete_book(book_id)
            return True, "Book deleted successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_all_books():
        return Book.get_all_books()
    
    @staticmethod
    def get_categories():
        return Book.get_categories()
    
    @staticmethod
    def add_member(username, password, full_name, email, phone):
        try:
            user_id = User.create_user(username, password, full_name, email, phone, 'Member')
            return True, f"Member added with ID: {user_id}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def update_member(user_id, **kwargs):
        try:
            User.update_user(user_id, **kwargs)
            return True, "Member updated"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_member(user_id):
        try:
            User.delete_user(user_id)
            return True, "Member deleted"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_all_members():
        users = User.get_all_users()
        return [u for u in users if u.role == 'Member']
