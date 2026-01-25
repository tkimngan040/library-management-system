"""
Unit Tests for Admin Module
Author: Member 2 - Book Management (Admin)
Description: Comprehensive tests for book and member management features
"""

import unittest
import sqlite3
import os
from datetime import datetime
from models.book import Book
from controllers.admin_controller import AdminController


class TestBookModel(unittest.TestCase):
    """Test cases for Book model"""
    
    def setUp(self):
        """Set up test database before each test"""
        self.db_name = 'test_library.db'
        self.conn = sqlite3.Connection(self.db_name)
        Book.create_table(self.conn)
        
        # Create borrow_records table for foreign key tests
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrow_records (
                borrow_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                book_id INTEGER,
                borrow_date TEXT,
                due_date TEXT,
                return_date TEXT,
                overdue_fine REAL,
                status TEXT
            )
        ''')
        self.conn.commit()
    
    def tearDown(self):
        """Clean up after each test"""
        self.conn.close()
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
    
    def test_create_book(self):
        """Test creating a new book"""
        book = Book(
            title="Test Book",
            author="Test Author",
            category="Fiction",
            description="A test book",
            detailed_info="Detailed test info",
            total_quantity=5,
            available_quantity=5
        )
        
        self.assertTrue(book.save(self.conn))
        self.assertIsNotNone(book.book_id)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.status, "Available")
    
    def test_get_book_by_id(self):
        """Test retrieving a book by ID"""
        book = Book(
            title="Test Book",
            author="Test Author",
            category="Fiction",
            total_quantity=3,
            available_quantity=3
        )
        book.save(self.conn)
        
        retrieved_book = Book.get_by_id(book.book_id, self.conn)
        
        self.assertIsNotNone(retrieved_book)
        self.assertEqual(retrieved_book.title, "Test Book")
        self.assertEqual(retrieved_book.author, "Test Author")
    
    def test_update_book(self):
        """Test updating book information"""
        book = Book(
            title="Original Title",
            author="Original Author",
            category="Fiction",
            total_quantity=5,
            available_quantity=5
        )
        book.save(self.conn)
        
        book.title = "Updated Title"
        book.author = "Updated Author"
        self.assertTrue(book.update(self.conn))
        
        updated_book = Book.get_by_id(book.book_id, self.conn)
        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.author, "Updated Author")
    
    def test_delete_book_without_borrows(self):
        """Test deleting a book that is not borrowed"""
        book = Book(
            title="To Delete",
            author="Test Author",
            category="Fiction",
            total_quantity=1,
            available_quantity=1
        )
        book.save(self.conn)
        
        success, message = Book.delete(book.book_id, self.conn)
        
        self.assertTrue(success)
        self.assertIn("success", message.lower())
        
        deleted_book = Book.get_by_id(book.book_id, self.conn)
        self.assertIsNone(deleted_book)
    
    def test_delete_book_with_active_borrows(self):
        """Test that deleting a borrowed book fails"""
        book = Book(
            title="Borrowed Book",
            author="Test Author",
            category="Fiction",
            total_quantity=1,
            available_quantity=0
        )
        book.save(self.conn)
        
        # Create an active borrow record
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status)
            VALUES (1, ?, '2024-01-01', '2024-01-15', 'Borrowed')
        ''', (book.book_id,))
        self.conn.commit()
        
        success, message = Book.delete(book.book_id, self.conn)
        
        self.assertFalse(success)
        self.assertIn("borrowed", message.lower())
    
    def test_search_books_by_title(self):
        """Test searching books by title"""
        books = [
            Book(title="Python Programming", author="Author A", category="Tech", total_quantity=1, available_quantity=1),
            Book(title="Java Programming", author="Author B", category="Tech", total_quantity=1, available_quantity=1),
            Book(title="Data Science", author="Author C", category="Science", total_quantity=1, available_quantity=1)
        ]
        
        for book in books:
            book.save(self.conn)
        
        results = Book.search("Programming", "title", self.conn)
        
        self.assertEqual(len(results), 2)
        titles = [book.title for book in results]
        self.assertIn("Python Programming", titles)
        self.assertIn("Java Programming", titles)
    
    def test_search_books_all_fields(self):
        """Test searching across all fields"""
        book = Book(
            title="Machine Learning",
            author="Smith",
            category="AI",
            total_quantity=1,
            available_quantity=1
        )
        book.save(self.conn)
        
        # Search by author
        results = Book.search("Smith", "all", self.conn)
        self.assertEqual(len(results), 1)
        
        # Search by category
        results = Book.search("AI", "all", self.conn)
        self.assertEqual(len(results), 1)
    
    def test_get_categories(self):
        """Test getting unique categories"""
        books = [
            Book(title="Book 1", author="Author", category="Fiction", total_quantity=1, available_quantity=1),
            Book(title="Book 2", author="Author", category="Science", total_quantity=1, available_quantity=1),
            Book(title="Book 3", author="Author", category="Fiction", total_quantity=1, available_quantity=1)
        ]
        
        for book in books:
            book.save(self.conn)
        
        categories = Book.get_categories(self.conn)
        
        self.assertEqual(len(categories), 2)
        self.assertIn("Fiction", categories)
        self.assertIn("Science", categories)
    
    def test_update_availability(self):
        """Test updating book availability"""
        book = Book(
            title="Test Book",
            author="Author",
            category="Fiction",
            total_quantity=5,
            available_quantity=5
        )
        book.save(self.conn)
        
        # Simulate borrowing (decrease by 1)
        self.assertTrue(book.update_availability(-1, self.conn))
        self.assertEqual(book.available_quantity, 4)
        self.assertEqual(book.status, "Available")
        
        # Simulate returning (increase by 1)
        self.assertTrue(book.update_availability(1, self.conn))
        self.assertEqual(book.available_quantity, 5)
        
        # Test invalid decrease
        self.assertFalse(book.update_availability(-10, self.conn))
    
    def test_is_available(self):
        """Test book availability check"""
        book = Book(
            title="Test Book",
            author="Author",
            category="Fiction",
            total_quantity=5,
            available_quantity=3
        )
        
        self.assertTrue(book.is_available())
        
        book.available_quantity = 0
        self.assertFalse(book.is_available())
    
    def test_get_total_count(self):
        """Test counting total books"""
        for i in range(5):
            book = Book(
                title=f"Book {i}",
                author="Author",
                category="Fiction",
                total_quantity=1,
                available_quantity=1
            )
            book.save(self.conn)
        
        count = Book.get_total_count(self.conn)
        self.assertEqual(count, 5)


class TestAdminController(unittest.TestCase):
    """Test cases for AdminController"""
    
    def setUp(self):
        """Set up test database and controller"""
        self.db_name = 'test_library.db'
        self.conn = sqlite3.Connection(self.db_name)
        
        # Create tables
        Book.create_table(self.conn)
        
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                role TEXT,
                account_status TEXT,
                fine_balance REAL,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrow_records (
                borrow_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                book_id INTEGER,
                borrow_date TEXT,
                due_date TEXT,
                return_date TEXT,
                overdue_fine REAL,
                status TEXT
            )
        ''')
        
        self.conn.commit()
        self.controller = AdminController(self.conn)
    
    def tearDown(self):
        """Clean up after tests"""
        self.conn.close()
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
    
    def test_add_book_success(self):
        """Test successfully adding a book"""
        success, message = self.controller.add_book(
            title="New Book",
            author="New Author",
            category="Fiction",
            description="A new book",
            detailed_info="Detailed info",
            quantity=5
        )
        
        self.assertTrue(success)
        self.assertIn("success", message.lower())
        self.assertIn("New Book", message)
    
    def test_add_book_validation(self):
        """Test book addition validation"""
        # Empty title
        success, message = self.controller.add_book("", "Author", "Fiction", "", "", 1)
        self.assertFalse(success)
        
        # Empty author
        success, message = self.controller.add_book("Title", "", "Fiction", "", "", 1)
        self.assertFalse(success)
        
        # Invalid quantity
        success, message = self.controller.add_book("Title", "Author", "Fiction", "", "", 0)
        self.assertFalse(success)
    
    def test_update_book_success(self):
        """Test successfully updating a book"""
        # First add a book
        success, msg = self.controller.add_book("Original", "Author", "Fiction", "", "", 5)
        self.assertTrue(success)
        
        # Get the book
        books = Book.get_all(self.conn, limit=1)
        book_id = books[0].book_id
        
        # Update it
        success, message = self.controller.update_book(
            book_id,
            title="Updated Title",
            author="Updated Author"
        )
        
        self.assertTrue(success)
        
        updated_book = Book.get_by_id(book_id, self.conn)
        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.author, "Updated Author")
    
    def test_add_member_success(self):
        """Test successfully adding a member"""
        success, message = self.controller.add_member(
            username="testuser",
            password="password123",
            full_name="Test User",
            email="test@test.com",
            phone="1234567890"
        )
        
        self.assertTrue(success)
        self.assertIn("success", message.lower())
    
    def test_add_member_validation(self):
        """Test member addition validation"""
        # Empty username
        success, msg = self.controller.add_member("", "pass", "Name", "", "")
        self.assertFalse(success)
        
        # Short password
        success, msg = self.controller.add_member("user", "123", "Name", "", "")
        self.assertFalse(success)
        
        # Empty full name
        success, msg = self.controller.add_member("user", "password", "", "", "")
        self.assertFalse(success)
    
    def test_add_duplicate_username(self):
        """Test adding member with duplicate username"""
        self.controller.add_member("testuser", "password", "User One", "", "")
        
        success, message = self.controller.add_member("testuser", "password", "User Two", "", "")
        
        self.assertFalse(success)
        self.assertIn("exists", message.lower())
    
    def test_get_statistics(self):
        """Test getting system statistics"""
        # Add some test data
        self.controller.add_book("Book 1", "Author", "Fiction", "", "", 5)
        self.controller.add_book("Book 2", "Author", "Science", "", "", 3)
        self.controller.add_member("user1", "password", "User One", "", "")
        
        stats = self.controller.get_statistics()
        
        self.assertEqual(stats['total_books'], 2)
        self.assertEqual(stats['total_members'], 1)
        self.assertGreaterEqual(stats['available_books'], 0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
