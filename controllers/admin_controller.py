"""
Admin Controller - Business logic for admin operations
Author: Member 2 - Book Management (Admin)
Description: Handles all admin-related operations including book and member management
Updated: Added Validators integration for consistent validation
"""

import sqlite3
import hashlib
from typing import List, Optional, Tuple, Dict
from datetime import datetime
from models.book import Book
from utils.validators import Validators


class AdminController:
    """Controller class for managing admin operations"""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        Initialize AdminController with database connection
        
        Args:
            db_connection: SQLite database connection object
        """
        self.conn = db_connection
    
    # ==================== BOOK MANAGEMENT ====================
    
    def add_book(self, title: str, author: str, category: str, 
                 description: str, detailed_info: str, quantity: int) -> Tuple[bool, str]:
        """
        Add a new book to the system
        
        Args:
            title: Book title
            author: Book author
            category: Book category
            description: Brief description
            detailed_info: Detailed information
            quantity: Total number of copies
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Sanitize inputs
        title = Validators.sanitize_input(title)
        author = Validators.sanitize_input(author)
        category = Validators.sanitize_input(category)
        description = Validators.sanitize_input(description)
        detailed_info = Validators.sanitize_input(detailed_info)
        
        # Validate all fields using Validators
        validations = [
            Validators.validate_book_title(title),
            Validators.validate_author_name(author),
            Validators.validate_category(category),
            Validators.validate_book_quantity(quantity)
        ]
        
        is_valid, error_msg = Validators.validate_all(validations)
        if not is_valid:
            return False, error_msg
        
        try:
            # Create new Book object
            book = Book(
                title=title,
                author=author,
                category=category,
                description=description,
                detailed_info=detailed_info,
                total_quantity=quantity,
                available_quantity=quantity,
                status="Available"
            )
            
            # Save to database
            if book.save(self.conn):
                return True, f"Book '{title}' added successfully! (ID: {book.book_id})"
            else:
                return False, "Failed to save book to database!"
                
        except Exception as e:
            return False, f"Error: {str(e)}"

    def update_book(self, book_id: int, title: str = None, author: str = None,
                    category: str = None, description: str = None,
                    detailed_info: str = None, total_quantity: int = None) -> Tuple[bool, str]:
        """
        Update book information
        
        Args:
            book_id: ID of the book to update
            title: New title (None to keep current)
            author: New author (None to keep current)
            category: New category (None to keep current)
            description: New description (None to keep current)
            detailed_info: New detailed info (None to keep current)
            total_quantity: New total quantity (None to keep current)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Get current book information
        book = Book.get_by_id(book_id, self.conn)
        
        if not book:
            return False, f"Book with ID {book_id} not found!"
        
        # Validate and update fields if new values provided
        if title is not None:
            title = Validators.sanitize_input(title)
            is_valid, msg = Validators.validate_book_title(title)
            if not is_valid:
                return False, msg
            book.title = title
        
        if author is not None:
            author = Validators.sanitize_input(author)
            is_valid, msg = Validators.validate_author_name(author)
            if not is_valid:
                return False, msg
            book.author = author
        
        if category is not None:
            category = Validators.sanitize_input(category)
            is_valid, msg = Validators.validate_category(category)
            if not is_valid:
                return False, msg
            book.category = category
        
        if description is not None:
            book.description = Validators.sanitize_input(description)
        
        if detailed_info is not None:
            book.detailed_info = Validators.sanitize_input(detailed_info)
        
        if total_quantity is not None:
            is_valid, msg = Validators.validate_book_quantity(total_quantity)
            if not is_valid:
                return False, msg
            
            # Check if new quantity is valid (must be >= borrowed count)
            borrowed_count = book.total_quantity - book.available_quantity
            if total_quantity < borrowed_count:
                return False, f"New quantity must be >= {borrowed_count} (currently borrowed)!"
            
            # Update available quantity accordingly
            book.available_quantity = total_quantity - borrowed_count
            book.total_quantity = total_quantity
            book.status = "Available" if book.available_quantity > 0 else "Borrowed"
        
        # Save changes
        if book.update(self.conn):
            return True, f"Book '{book.title}' updated successfully!"
        else:
            return False, "Failed to update book!"

    def delete_book(self, book_id: int) -> Tuple[bool, str]:
        """
        Delete a book from the system
        
        Args:
            book_id: ID of the book to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        return Book.delete(book_id, self.conn)

    def get_all_books(self, page: int = 1, per_page: int = 10) -> Tuple[List[Book], int]:
        """
        Get all books with pagination
        
        Args:
            page: Current page number
            per_page: Number of books per page
            
        Returns:
            Tuple of (list of books, total pages)
        """
        offset = (page - 1) * per_page
        books = Book.get_all(self.conn, limit=per_page, offset=offset)
        total_books = Book.get_total_count(self.conn)
        total_pages = (total_books + per_page - 1) // per_page if total_books > 0 else 1
        
        return books, total_pages

    def search_books(self, keyword: str, field: str = 'all') -> List[Book]:
        """
        Search for books by keyword
        
        Args:
            keyword: Search keyword
            field: Field to search in ('title', 'author', 'category', 'all')
            
        Returns:
            List of matching books
        """
        keyword = Validators.sanitize_input(keyword)
        return Book.search(keyword, field, self.conn)

    def get_book_details(self, book_id: int) -> Optional[Book]:
        """
        Get detailed information about a book
        
        Args:
            book_id: ID of the book
            
        Returns:
            Book object if found, None otherwise
        """
        return Book.get_by_id(book_id, self.conn)

    def get_books_by_category(self, category: str) -> List[Book]:
        """
        Get all books in a specific category
        
        Args:
            category: Category name
            
        Returns:
            List of books in the category
        """
        category = Validators.sanitize_input(category)
        return Book.get_by_category(category, self.conn)

    def get_all_categories(self) -> List[str]:
        """
        Get list of all book categories
        
        Returns:
            List of category names
        """
        return Book.get_categories(self.conn)

    # ==================== MEMBER MANAGEMENT ====================
    
    def get_all_members(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """
        Get all members with pagination
        
        Args:
            page: Current page number
            per_page: Number of members per page
            
        Returns:
            Tuple of (list of member dictionaries, total pages)
        """
        try:
            cursor = self.conn.cursor()
            
            # Count total members
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Member'")
            total_members = cursor.fetchone()[0]
            total_pages = (total_members + per_page - 1) // per_page if total_members > 0 else 1
            
            # Get members with pagination
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT user_id, username, full_name, email, phone, 
                       account_status, fine_balance, created_at
                FROM users 
                WHERE role = 'Member'
                ORDER BY user_id DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            
            members = []
            for row in cursor.fetchall():
                members.append({
                    'user_id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'email': row[3] if row[3] else '',
                    'phone': row[4] if row[4] else '',
                    'account_status': row[5],
                    'fine_balance': row[6],
                    'created_at': row[7]
                })
            
            return members, total_pages
            
        except sqlite3.Error as e:
            print(f"Error retrieving members: {e}")
            return [], 0

    def add_member(self, username: str, password: str, full_name: str,
                   email: str = "", phone: str = "") -> Tuple[bool, str]:
        """
        Add a new member to the system
        
        Args:
            username: Username for login
            password: Password (will be hashed)
            full_name: Full name of the member
            email: Email address (optional)
            phone: Phone number (optional)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Sanitize inputs
        username = Validators.sanitize_input(username)
        full_name = Validators.sanitize_input(full_name)
        email = Validators.sanitize_input(email)
        phone = Validators.sanitize_input(phone)
        
        # Validate required fields
        validations = [
            Validators.validate_username(username),
            Validators.validate_password(password),
            Validators.validate_not_empty(full_name, "Full name"),
            Validators.validate_string_length(full_name, 1, 100, "Full name")
        ]
        
        # Validate optional fields if provided
        if email:
            validations.append(Validators.validate_email(email))
        
        if phone:
            validations.append(Validators.validate_phone(phone))
        
        is_valid, error_msg = Validators.validate_all(validations)
        if not is_valid:
            return False, error_msg
        
        try:
            cursor = self.conn.cursor()
            
            # Check if username already exists
            cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return False, f"Username '{username}' already exists!"
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Add new member
            cursor.execute('''
                INSERT INTO users (username, password, full_name, email, phone, 
                                 role, account_status, fine_balance, created_at)
                VALUES (?, ?, ?, ?, ?, 'Member', 'Active', 0, ?)
            ''', (username, hashed_password, full_name, email, phone,
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            self.conn.commit()
            return True, f"Member '{username}' added successfully!"
            
        except sqlite3.Error as e:
            return False, f"Error: {str(e)}"

    def update_member(self, user_id: int, full_name: str = None, email: str = None,
                     phone: str = None, account_status: str = None) -> Tuple[bool, str]:
        """
        Update member information
        
        Args:
            user_id: ID of the member to update
            full_name: New full name (None to keep current)
            email: New email (None to keep current)
            phone: New phone (None to keep current)
            account_status: New status ('Active' or 'Locked', None to keep current)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            cursor = self.conn.cursor()
            
            # Check if member exists
            cursor.execute('SELECT username FROM users WHERE user_id = ? AND role = "Member"', 
                          (user_id,))
            member = cursor.fetchone()
            
            if not member:
                return False, f"Member with ID {user_id} not found!"
            
            # Build dynamic update query
            updates = []
            params = []
            
            if full_name is not None:
                full_name = Validators.sanitize_input(full_name)
                is_valid, msg = Validators.validate_not_empty(full_name, "Full name")
                if not is_valid:
                    return False, msg
                
                is_valid, msg = Validators.validate_string_length(full_name, 1, 100, "Full name")
                if not is_valid:
                    return False, msg
                
                updates.append("full_name = ?")
                params.append(full_name)
            
            if email is not None:
                email = Validators.sanitize_input(email)
                if email:  # Only validate if not empty
                    is_valid, msg = Validators.validate_email(email)
                    if not is_valid:
                        return False, msg
                
                updates.append("email = ?")
                params.append(email)
            
            if phone is not None:
                phone = Validators.sanitize_input(phone)
                if phone:  # Only validate if not empty
                    is_valid, msg = Validators.validate_phone(phone)
                    if not is_valid:
                        return False, msg
                
                updates.append("phone = ?")
                params.append(phone)
            
            if account_status is not None:
                if account_status not in ['Active', 'Locked']:
                    return False, "Status must be 'Active' or 'Locked'!"
                updates.append("account_status = ?")
                params.append(account_status)
            
            if not updates:
                return False, "No information to update!"
            
            # Add updated_at timestamp
            updates.append("updated_at = ?")
            params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Execute update
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
            params.append(user_id)
            
            cursor.execute(query, params)
            self.conn.commit()
            
            return True, "Member information updated successfully!"
            
        except sqlite3.Error as e:
            return False, f"Error: {str(e)}"

    def delete_member(self, user_id: int) -> Tuple[bool, str]:
        """
        Delete a member from the system
        
        Args:
            user_id: ID of the member to delete
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            cursor = self.conn.cursor()
            
            # Check if member has active borrows
            cursor.execute('''
                SELECT COUNT(*) FROM borrow_records 
                WHERE user_id = ? AND return_date IS NULL
            ''', (user_id,))
            
            active_borrows = cursor.fetchone()[0]
            
            if active_borrows > 0:
                return False, f"Cannot delete! Member has {active_borrows} book(s) currently borrowed."
            
            # Delete member
            cursor.execute('DELETE FROM users WHERE user_id = ? AND role = "Member"', (user_id,))
            
            if cursor.rowcount == 0:
                return False, "Member not found!"
            
            self.conn.commit()
            return True, "Member deleted successfully!"
            
        except sqlite3.Error as e:
            return False, f"Error: {str(e)}"

    def get_member_borrow_history(self, user_id: int) -> List[Dict]:
        """
        Get borrowing history for a specific member
        
        Args:
            user_id: ID of the member
            
        Returns:
            List of borrow record dictionaries
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT br.borrow_id, b.title, br.borrow_date, br.due_date, 
                       br.return_date, br.overdue_fine, br.status
                FROM borrow_records br
                JOIN books b ON br.book_id = b.book_id
                WHERE br.user_id = ?
                ORDER BY br.borrow_date DESC
            ''', (user_id,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'borrow_id': row[0],
                    'book_title': row[1],
                    'borrow_date': row[2],
                    'due_date': row[3],
                    'return_date': row[4] if row[4] else None,
                    'overdue_fine': row[5] if row[5] else 0,
                    'status': row[6]
                })
            
            return history
            
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
            return []

    def lock_unlock_member(self, user_id: int, lock: bool) -> Tuple[bool, str]:
        """
        Lock or unlock a member account
        
        Args:
            user_id: ID of the member
            lock: True to lock, False to unlock
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        status = "Locked" if lock else "Active"
        return self.update_member(user_id, account_status=status)

    def search_members(self, keyword: str) -> List[Dict]:
        """
        Search for members by username or full name
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching member dictionaries
        """
        try:
            keyword = Validators.sanitize_input(keyword)
            cursor = self.conn.cursor()
            keyword_pattern = f'%{keyword}%'
            
            cursor.execute('''
                SELECT user_id, username, full_name, email, phone, 
                       account_status, fine_balance, created_at
                FROM users 
                WHERE role = 'Member' AND (username LIKE ? OR full_name LIKE ?)
                ORDER BY user_id DESC
            ''', (keyword_pattern, keyword_pattern))
            
            members = []
            for row in cursor.fetchall():
                members.append({
                    'user_id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'email': row[3] if row[3] else '',
                    'phone': row[4] if row[4] else '',
                    'account_status': row[5],
                    'fine_balance': row[6],
                    'created_at': row[7]
                })
            
            return members
            
        except sqlite3.Error as e:
            print(f"Error searching members: {e}")
            return []

    # ==================== BORROW RECORDS MANAGEMENT ====================
    
    def get_all_borrow_records(self, status_filter: str = 'all', 
                              page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """
        Get all borrow records with optional filtering and pagination
        
        Args:
            status_filter: Filter by status ('all', 'borrowed', 'returned', 'overdue')
            page: Current page number
            per_page: Number of records per page
            
        Returns:
            Tuple of (list of record dictionaries, total pages)
        """
        try:
            cursor = self.conn.cursor()
            
            # Build base query
            base_query = '''
                SELECT br.borrow_id, u.username, u.full_name, b.title, 
                       br.borrow_date, br.due_date, br.return_date, 
                       br.overdue_fine, br.status
                FROM borrow_records br
                JOIN users u ON br.user_id = u.user_id
                JOIN books b ON br.book_id = b.book_id
            '''
            
            # Add filter
            if status_filter == 'borrowed':
                base_query += " WHERE br.return_date IS NULL"
            elif status_filter == 'returned':
                base_query += " WHERE br.return_date IS NOT NULL"
            elif status_filter == 'overdue':
                base_query += " WHERE br.return_date IS NULL AND date('now') > br.due_date"
            
            # Count total records
            count_query = f"SELECT COUNT(*) FROM ({base_query})"
            cursor.execute(count_query)
            total_records = cursor.fetchone()[0]
            total_pages = (total_records + per_page - 1) // per_page if total_records > 0 else 1
            
            # Get paginated data
            base_query += " ORDER BY br.borrow_date DESC LIMIT ? OFFSET ?"
            offset = (page - 1) * per_page
            cursor.execute(base_query, (per_page, offset))
            
            records = []
            for row in cursor.fetchall():
                records.append({
                    'borrow_id': row[0],
                    'username': row[1],
                    'full_name': row[2],
                    'book_title': row[3],
                    'borrow_date': row[4],
                    'due_date': row[5],
                    'return_date': row[6] if row[6] else None,
                    'overdue_fine': row[7] if row[7] else 0,
                    'status': row[8]
                })
            
            return records, total_pages
            
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
            return [], 0

    def get_statistics(self) -> Dict:
        """
        Get system statistics
        
        Returns:
            Dictionary containing various statistics
        """
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Total books
            cursor.execute('SELECT COUNT(*) FROM books')
            stats['total_books'] = cursor.fetchone()[0]
            
            # Total members
            cursor.execute('SELECT COUNT(*) FROM users WHERE role = "Member"')
            stats['total_members'] = cursor.fetchone()[0]
            
            # Active borrows
            cursor.execute('SELECT COUNT(*) FROM borrow_records WHERE return_date IS NULL')
            stats['active_borrows'] = cursor.fetchone()[0]
            
            # Overdue books
            cursor.execute('''
                SELECT COUNT(*) FROM borrow_records 
                WHERE return_date IS NULL AND date('now') > due_date
            ''')
            stats['overdue_books'] = cursor.fetchone()[0]
            
            # Available books
            cursor.execute('SELECT COUNT(*) FROM books WHERE available_quantity > 0')
            stats['available_books'] = cursor.fetchone()[0]
            
            # Total fines
            cursor.execute('SELECT SUM(fine_balance) FROM users WHERE role = "Member"')
            total_fines = cursor.fetchone()[0]
            stats['total_fines'] = total_fines if total_fines else 0
            
            return stats
            
        except sqlite3.Error as e:
            print(f"Error getting statistics: {e}")
            return {}
