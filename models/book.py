from database.db_connection import DatabaseConnection

class Book:
    """Book model class"""
    
    def __init__(self, book_id=None, title=None, author=None, category_id=None,
                 description=None, detailed_info=None, total_quantity=1,
                 available_quantity=1, created_date=None, category_name=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category_id = category_id
        self.description = description
        self.detailed_info = detailed_info
        self.total_quantity = total_quantity
        self.available_quantity = available_quantity
        self.created_date = created_date
        self.category_name = category_name
    
    @property
    def status(self):
        """Get book availability status"""
        return "Available" if self.available_quantity > 0 else "Borrowed"
    
    @staticmethod
    def create_book(title, author, category_id, description, detailed_info, quantity):
        """Create new book"""
        query = '''
            INSERT INTO books (title, author, category_id, description, detailed_info, 
                             total_quantity, available_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        
        try:
            book_id = DatabaseConnection.execute_update(
                query,
                (title, author, category_id, description, detailed_info, quantity, quantity)
            )
            return book_id
        except Exception as e:
            raise Exception(f"Error creating book: {str(e)}")
    
    @staticmethod
    def get_book_by_id(book_id):
        """Get book by ID"""
        query = '''
            SELECT b.*, c.category_name 
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.category_id
            WHERE b.book_id = ?
        '''
        results = DatabaseConnection.execute_query(query, (book_id,))
        
        if results:
            return Book(**dict(results[0]))
        return None
    
    @staticmethod
    def get_all_books():
        """Get all books with category names"""
        query = '''
            SELECT b.*, c.category_name 
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.category_id
            ORDER BY b.book_id DESC
        '''
        results = DatabaseConnection.execute_query(query)
        return [Book(**dict(row)) for row in results]
    
    @staticmethod
    def update_book(book_id, **kwargs):
        """Update book information"""
        allowed_fields = ['title', 'author', 'category_id', 'description', 
                         'detailed_info', 'total_quantity']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(book_id)
        query = f"UPDATE books SET {', '.join(updates)} WHERE book_id = ?"
        
        try:
            DatabaseConnection.execute_update(query, tuple(values))
            return True
        except Exception as e:
            raise Exception(f"Error updating book: {str(e)}")
    
    @staticmethod
    def delete_book(book_id):
        """Delete book"""
        # Check if book is currently borrowed
        book = Book.get_book_by_id(book_id)
        if book and book.available_quantity < book.total_quantity:
            raise Exception("Cannot delete book with active borrows")
        
        query = "DELETE FROM books WHERE book_id = ?"
        DatabaseConnection.execute_update(query, (book_id,))
    
    @staticmethod
    def update_quantity(book_id, change):
        """Update available quantity"""
        query = '''
            UPDATE books 
            SET available_quantity = available_quantity + ? 
            WHERE book_id = ?
        '''
        DatabaseConnection.execute_update(query, (change, book_id))
    
    @staticmethod
    def get_categories():
        """Get all categories"""
        query = "SELECT * FROM categories ORDER BY category_name"
        return DatabaseConnection.execute_query(query)
    
    @staticmethod
    def create_category(category_name, description):
        """Create new category"""
        query = "INSERT INTO categories (category_name, description) VALUES (?, ?)"
        return DatabaseConnection.execute_update(query, (category_name, description))
