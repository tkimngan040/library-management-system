"""
Book Model - Manages book information in the Library Management System
Author: Member 2 - Book Management (Admin)
Description: Handles all book-related database operations and business logic
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple


class Book:
    """
    Book class representing a book in the library system
    
    Attributes:
        book_id (int): Unique identifier for the book
        title (str): Book title
        author (str): Book author
        category (str): Book category/genre
        description (str): Brief description of the book
        detailed_info (str): Detailed information about the book
        total_quantity (int): Total number of copies
        available_quantity (int): Number of available copies
        status (str): Current status (Available/Borrowed)
        created_at (str): Timestamp when book was added
    """
    
    def __init__(self, book_id: int = None, title: str = "", author: str = "",
                 category: str = "", description: str = "", detailed_info: str = "",
                 total_quantity: int = 0, available_quantity: int = 0,
                 status: str = "Available", created_at: str = None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.detailed_info = detailed_info
        self.total_quantity = total_quantity
        self.available_quantity = available_quantity
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        """String representation of Book"""
        return f"[{self.book_id}] {self.title} by {self.author} - {self.status}"

    def __repr__(self):
        """Detailed representation for debugging"""
        return f"Book(id={self.book_id}, title='{self.title}', author='{self.author}')"

    @staticmethod
    def create_table(conn: sqlite3.Connection):
        """
        Create books table in database if it doesn't exist
        
        Args:
            conn: Database connection object
        """
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                detailed_info TEXT,
                total_quantity INTEGER DEFAULT 1,
                available_quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'Available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()

    def save(self, conn: sqlite3.Connection) -> bool:
        """
        Save a new book to the database
        
        Args:
            conn: Database connection object
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO books (title, author, category, description, detailed_info,
                                 total_quantity, available_quantity, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.title, self.author, self.category, self.description,
                  self.detailed_info, self.total_quantity, self.available_quantity,
                  self.status, self.created_at))
            
            self.book_id = cursor.lastrowid
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error saving book: {e}")
            return False

    @staticmethod
    def get_by_id(book_id: int, conn: sqlite3.Connection) -> Optional['Book']:
        """
        Retrieve a book by its ID
        
        Args:
            book_id: ID of the book to retrieve
            conn: Database connection object
            
        Returns:
            Book object if found, None otherwise
        """
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
            row = cursor.fetchone()
            
            if row:
                return Book(
                    book_id=row[0],
                    title=row[1],
                    author=row[2],
                    category=row[3],
                    description=row[4],
                    detailed_info=row[5],
                    total_quantity=row[6],
                    available_quantity=row[7],
                    status=row[8],
                    created_at=row[9]
                )
            return None
            
        except sqlite3.Error as e:
            print(f"Error retrieving book: {e}")
            return None

    @staticmethod
    def get_all(conn: sqlite3.Connection, limit: int = None, offset: int = 0) -> List['Book']:
        """
        Retrieve all books from database with optional pagination
        
        Args:
            conn: Database connection object
            limit: Maximum number of books to retrieve
            offset: Starting position for pagination
            
        Returns:
            List of Book objects
        """
        try:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM books ORDER BY book_id DESC'
            if limit:
                query += f' LIMIT {limit} OFFSET {offset}'
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            books = []
            for row in rows:
                books.append(Book(
                    book_id=row[0],
                    title=row[1],
                    author=row[2],
                    category=row[3],
                    description=row[4],
                    detailed_info=row[5],
                    total_quantity=row[6],
                    available_quantity=row[7],
                    status=row[8],
                    created_at=row[9]
                ))
            return books
            
        except sqlite3.Error as e:
            print(f"Error retrieving books: {e}")
            return []

    @staticmethod
    def get_total_count(conn: sqlite3.Connection) -> int:
        """
        Count total number of books in database
        
        Args:
            conn: Database connection object
            
        Returns:
            Total count of books
        """
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM books')
            count = cursor.fetchone()[0]
            return count
        except sqlite3.Error:
            return 0

    def update(self, conn: sqlite3.Connection) -> bool:
        """
        Update book information in database
        
        Args:
            conn: Database connection object
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE books 
                SET title = ?, author = ?, category = ?, description = ?,
                    detailed_info = ?, total_quantity = ?, available_quantity = ?,
                    status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE book_id = ?
            ''', (self.title, self.author, self.category, self.description,
                  self.detailed_info, self.total_quantity, self.available_quantity,
                  self.status, self.book_id))
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error updating book: {e}")
            return False

    @staticmethod
    def delete(book_id: int, conn: sqlite3.Connection) -> Tuple[bool, str]:
        """
        Delete a book from database
        
        Args:
            book_id: ID of the book to delete
            conn: Database connection object
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            cursor = conn.cursor()
            
            # Check if book is currently borrowed
            cursor.execute('''
                SELECT COUNT(*) FROM borrow_records 
                WHERE book_id = ? AND return_date IS NULL
            ''', (book_id,))
            
            active_borrows = cursor.fetchone()[0]
            
            if active_borrows > 0:
                return False, f"Cannot delete! Book is currently borrowed by {active_borrows} member(s)."
            
            cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
            
            if cursor.rowcount == 0:
                return False, "Book not found."
            
            conn.commit()
            return True, "Book deleted successfully!"
            
        except sqlite3.Error as e:
            return False, f"Error deleting book: {e}"

    @staticmethod
    def search(keyword: str, field: str, conn: sqlite3.Connection) -> List['Book']:
        """
        Search for books by keyword and field
        
        Args:
            keyword: Search keyword
            field: Field to search in ('title', 'author', 'category', 'all')
            conn: Database connection object
            
        Returns:
            List of matching Book objects
        """
        try:
            cursor = conn.cursor()
            keyword = f'%{keyword}%'
            
            if field == 'title':
                query = 'SELECT * FROM books WHERE title LIKE ?'
                params = (keyword,)
            elif field == 'author':
                query = 'SELECT * FROM books WHERE author LIKE ?'
                params = (keyword,)
            elif field == 'category':
                query = 'SELECT * FROM books WHERE category LIKE ?'
                params = (keyword,)
            else:  # 'all'
                query = '''SELECT * FROM books 
                          WHERE title LIKE ? OR author LIKE ? OR category LIKE ?'''
                params = (keyword, keyword, keyword)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            books = []
            for row in rows:
                books.append(Book(
                    book_id=row[0],
                    title=row[1],
                    author=row[2],
                    category=row[3],
                    description=row[4],
                    detailed_info=row[5],
                    total_quantity=row[6],
                    available_quantity=row[7],
                    status=row[8],
                    created_at=row[9]
                ))
            return books
            
        except sqlite3.Error as e:
            print(f"Error searching books: {e}")
            return []

    @staticmethod
    def get_by_category(category: str, conn: sqlite3.Connection) -> List['Book']:
        """
        Get all books in a specific category
        
        Args:
            category: Category name
            conn: Database connection object
            
        Returns:
            List of Book objects in the category
        """
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE category = ? ORDER BY title', (category,))
            rows = cursor.fetchall()
            
            books = []
            for row in rows:
                books.append(Book(
                    book_id=row[0],
                    title=row[1],
                    author=row[2],
                    category=row[3],
                    description=row[4],
                    detailed_info=row[5],
                    total_quantity=row[6],
                    available_quantity=row[7],
                    status=row[8],
                    created_at=row[9]
                ))
            return books
            
        except sqlite3.Error as e:
            print(f"Error getting books by category: {e}")
            return []

    @staticmethod
    def get_categories(conn: sqlite3.Connection) -> List[str]:
        """
        Get list of all unique book categories
        
        Args:
            conn: Database connection object
            
        Returns:
            List of category names
        """
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT category FROM books ORDER BY category')
            categories = [row[0] for row in cursor.fetchall()]
            return categories
        except sqlite3.Error:
            return []

    def update_availability(self, quantity_change: int, conn: sqlite3.Connection) -> bool:
        """
        Update the available quantity of the book
        Used when borrowing (negative change) or returning (positive change) books
        
        Args:
            quantity_change: Amount to change (negative for borrow, positive for return)
            conn: Database connection object
            
        Returns:
            bool: True if successful, False otherwise
        """
        new_quantity = self.available_quantity + quantity_change
        
        # Validate new quantity
        if new_quantity < 0 or new_quantity > self.total_quantity:
            return False
        
        self.available_quantity = new_quantity
        self.status = "Available" if new_quantity > 0 else "Borrowed"
        
        return self.update(conn)

    def is_available(self) -> bool:
        """
        Check if book is available for borrowing
        
        Returns:
            bool: True if available, False otherwise
        """
        return self.available_quantity > 0

    @staticmethod
    def get_available_books(conn: sqlite3.Connection) -> List['Book']:
        """
        Get all books that are currently available
        
        Args:
            conn: Database connection object
            
        Returns:
            List of available Book objects
        """
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE available_quantity > 0 ORDER BY title')
            rows = cursor.fetchall()
            
            books = []
            for row in rows:
                books.append(Book(
                    book_id=row[0],
                    title=row[1],
                    author=row[2],
                    category=row[3],
                    description=row[4],
                    detailed_info=row[5],
                    total_quantity=row[6],
                    available_quantity=row[7],
                    status=row[8],
                    created_at=row[9]
                ))
            return books
            
        except sqlite3.Error as e:
            print(f"Error getting available books: {e}")
            return []
