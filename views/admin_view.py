"""
Admin View - Console user interface for admin operations
Author: Member 2 - Book Management (Admin)
Description: Provides all UI components for admin features
"""

import os
import sys
from typing import List, Dict
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)


class AdminView:
    """Class managing all admin interface displays and interactions"""
    
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title: str):
        """
        Print a formatted header
        
        Args:
            title: Header title text
        """
        print(Fore.CYAN + "=" * 80)
        print(Fore.YELLOW + Style.BRIGHT + f"  {title.center(76)}")
        print(Fore.CYAN + "=" * 80)
        print()

    @staticmethod
    def print_success(message: str):
        """Print success message in green"""
        print(Fore.GREEN + Style.BRIGHT + "✓ " + message)

    @staticmethod
    def print_error(message: str):
        """Print error message in red"""
        print(Fore.RED + Style.BRIGHT + "✗ " + message)

    @staticmethod
    def print_info(message: str):
        """Print information message in cyan"""
        print(Fore.CYAN + "ⓘ " + message)

    @staticmethod
    def print_warning(message: str):
        """Print warning message in yellow"""
        print(Fore.YELLOW + "⚠ " + message)

    @staticmethod
    def pause():
        """Pause and wait for user to press Enter"""
        input(Fore.YELLOW + "\n⏎ Press Enter to continue...")

    @staticmethod
    def get_confirmation(message: str) -> bool:
        """
        Get yes/no confirmation from user
        
        Args:
            message: Confirmation message
            
        Returns:
            bool: True if user confirms, False otherwise
        """
        response = input(Fore.YELLOW + message + " (y/n): ").strip().lower()
        return response == 'y'

    # ==================== MAIN MENU ====================
    
    @staticmethod
    def admin_menu() -> str:
        """
        Display admin main menu
        
        Returns:
            User's menu choice
        """
        AdminView.clear_screen()
        AdminView.print_header("ADMIN DASHBOARD")
        
        print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════╗")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "1. 📚 Manage Books" + " " * 19 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "2. 👥 Manage Members" + " " * 16 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "3. 📋 Manage Borrow Records" + " " * 9 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "4. 📊 View Statistics" + " " * 15 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.RED + "0. 🚪 Logout" + " " * 23 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════╝")
        print()
        
        choice = input(Fore.YELLOW + "➤ Enter your choice: " + Fore.WHITE).strip()
        return choice

    # ==================== BOOK MANAGEMENT ====================
    
    @staticmethod
    def show_book_management_menu() -> str:
        """
        Display book management menu
        
        Returns:
            User's menu choice
        """
        AdminView.clear_screen()
        AdminView.print_header("BOOK MANAGEMENT")
        
        print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════╗")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "1. ➕ Add New Book" + " " * 19 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "2. 📋 View All Books" + " " * 16 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "3. 🔍 Search Books" + " " * 18 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "4. ✏️  Update Book" + " " * 18 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "5. 🗑️  Delete Book" + " " * 18 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "6. 📂 View by Category" + " " * 13 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.RED + "0. ⬅️  Back" + " " * 24 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════╝")
        print()
        
        choice = input(Fore.YELLOW + "➤ Enter your choice: " + Fore.WHITE).strip()
        return choice

    @staticmethod
    def add_book_form() -> Dict:
        """
        Display form to add a new book
        
        Returns:
            Dictionary with book information or None if cancelled
        """
        AdminView.clear_screen()
        AdminView.print_header("ADD NEW BOOK")
        
        print(Fore.CYAN + "Enter book information:")
        print(Fore.YELLOW + "─" * 80 + "\n")
        
        title = input(Fore.WHITE + "📖 Book Title: ").strip()
        if not title:
            AdminView.print_error("Book title cannot be empty!")
            AdminView.pause()
            return None
        
        author = input(Fore.WHITE + "✍️  Author: ").strip()
        if not author:
            AdminView.print_error("Author name cannot be empty!")
            AdminView.pause()
            return None
        
        # Show existing categories
        print(Fore.CYAN + "\n📂 You can enter an existing category or create a new one")
        
        category = input(Fore.WHITE + "📂 Category: ").strip()
        if not category:
            AdminView.print_error("Category cannot be empty!")
            AdminView.pause()
            return None
        
        description = input(Fore.WHITE + "📝 Brief Description: ").strip()
        detailed_info = input(Fore.WHITE + "📄 Detailed Information: ").strip()
        
        try:
            quantity = int(input(Fore.WHITE + "🔢 Quantity: ").strip())
            if quantity <= 0:
                AdminView.print_error("Quantity must be greater than 0!")
                AdminView.pause()
                return None
        except ValueError:
            AdminView.print_error("Quantity must be a number!")
            AdminView.pause()
            return None
        
        # Show confirmation
        print(Fore.YELLOW + "\n" + "─" * 80)
        print(Fore.CYAN + "📋 Confirm Information:")
        print(Fore.WHITE + f"   Title: {title}")
        print(Fore.WHITE + f"   Author: {author}")
        print(Fore.WHITE + f"   Category: {category}")
        print(Fore.WHITE + f"   Quantity: {quantity}")
        print(Fore.YELLOW + "─" * 80 + "\n")
        
        if not AdminView.get_confirmation("Confirm adding this book?"):
            AdminView.print_info("Operation cancelled!")
            AdminView.pause()
            return None
        
        return {
            'title': title,
            'author': author,
            'category': category,
            'description': description,
            'detailed_info': detailed_info,
            'quantity': quantity
        }

    @staticmethod
    def display_books_table(books: List, page: int = 1, total_pages: int = 1):
        """
        Display books in a formatted table
        
        Args:
            books: List of Book objects
            page: Current page number
            total_pages: Total number of pages
        """
        if not books:
            AdminView.print_error("No books found!")
            return
        
        AdminView.clear_screen()
        AdminView.print_header(f"BOOK LIST (Page {page}/{total_pages})")
        
        # Prepare table data
        table_data = []
        for book in books:
            status_color = Fore.GREEN if book.status == "Available" else Fore.RED
            table_data.append([
                book.book_id,
                book.title[:40] + "..." if len(book.title) > 40 else book.title,
                book.author[:30] + "..." if len(book.author) > 30 else book.author,
                book.category[:20],
                f"{book.available_quantity}/{book.total_quantity}",
                status_color + book.status + Style.RESET_ALL
            ])
        
        headers = [
            Fore.CYAN + "ID",
            "Title",
            "Author",
            "Category",
            "Available",
            "Status" + Style.RESET_ALL
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()

    @staticmethod
    def display_books_list(books: List, page: int, total_pages: int) -> str:
        """
        Display books list with pagination controls
        
        Args:
            books: List of Book objects
            page: Current page number
            total_pages: Total number of pages
            
        Returns:
            User's navigation choice
        """
        AdminView.display_books_table(books, page, total_pages)
        
        if total_pages > 1:
            print(Fore.YELLOW + f"Page {page}/{total_pages}")
            print(Fore.CYAN + "[N] Next Page | [P] Previous Page | [Enter] Back")
            choice = input(Fore.YELLOW + "➤ ").strip().lower()
            return choice
        else:
            AdminView.pause()
            return ''

    @staticmethod
    def search_books_form() -> Dict:
        """
        Display search form for books
        
        Returns:
            Dictionary with search criteria or None if cancelled
        """
        AdminView.clear_screen()
        AdminView.print_header("SEARCH BOOKS")
        
        print(Fore.CYAN + "Select search field:")
        print(Fore.WHITE + "1. Title")
        print(Fore.WHITE + "2. Author")
        print(Fore.WHITE + "3. Category")
        print(Fore.WHITE + "4. All Fields")
        print()
        
        field_choice = input(Fore.YELLOW + "➤ Choose (1-4): ").strip()
        
        field_map = {'1': 'title', '2': 'author', '3': 'category', '4': 'all'}
        field = field_map.get(field_choice, 'all')
        
        keyword = input(Fore.YELLOW + "\n🔍 Enter keyword: ").strip()
        
        if not keyword:
            AdminView.print_error("Keyword cannot be empty!")
            AdminView.pause()
            return None
        
        return {'keyword': keyword, 'field': field}

    @staticmethod
    def display_search_results(books: List, keyword: str):
        """
        Display search results
        
        Args:
            books: List of Book objects found
            keyword: Search keyword used
        """
        if not books:
            AdminView.clear_screen()
            AdminView.print_header("SEARCH RESULTS")
            AdminView.print_error(f"No books found with keyword '{keyword}'!")
            AdminView.pause()
            return
        
        AdminView.clear_screen()
        AdminView.print_header(f"SEARCH RESULTS: '{keyword}'")
        
        table_data = []
        for book in books:
            status_color = Fore.GREEN if book.status == "Available" else Fore.RED
            table_data.append([
                book.book_id,
                book.title[:40],
                book.author[:30],
                book.category[:20],
                f"{book.available_quantity}/{book.total_quantity}",
                status_color + book.status + Style.RESET_ALL
            ])
        
        headers = [Fore.CYAN + "ID", "Title", "Author", "Category", "Available", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(Fore.GREEN + f"\nFound {len(books)} book(s)")
        print()
        
        AdminView.pause()

    @staticmethod
    def update_book_form(book) -> Dict:
        """
        Display form to update book information
        
        Args:
            book: Current Book object
            
        Returns:
            Dictionary with updated information or None if cancelled
        """
        AdminView.clear_screen()
        AdminView.print_header("UPDATE BOOK INFORMATION")
        
        # Display current information
        print(Fore.CYAN + "📖 Current Information:")
        print(Fore.YELLOW + "─" * 80)
        print(Fore.WHITE + f"Title: {book.title}")
        print(Fore.WHITE + f"Author: {book.author}")
        print(Fore.WHITE + f"Category: {book.category}")
        print(Fore.WHITE + f"Description: {book.description}")
        print(Fore.WHITE + f"Quantity: {book.total_quantity} (Available: {book.available_quantity})")
        print(Fore.YELLOW + "─" * 80 + "\n")
        
        print(Fore.CYAN + "Enter new information (press Enter to keep current):\n")
        
        title = input(Fore.WHITE + f"📖 Title [{book.title}]: ").strip()
        author = input(Fore.WHITE + f"✍️  Author [{book.author}]: ").strip()
        category = input(Fore.WHITE + f"📂 Category [{book.category}]: ").strip()
        description = input(Fore.WHITE + f"📝 Description [{book.description}]: ").strip()
        detailed_info = input(Fore.WHITE + f"📄 Detailed Info [{book.detailed_info}]: ").strip()
        
        quantity_input = input(Fore.WHITE + f"🔢 Quantity [{book.total_quantity}]: ").strip()
        quantity = None
        if quantity_input:
            try:
                quantity = int(quantity_input)
            except ValueError:
                AdminView.print_error("Quantity must be a number!")
                AdminView.pause()
                return None
        
        if not AdminView.get_confirmation("\nConfirm update?"):
            AdminView.print_info("Operation cancelled!")
            AdminView.pause()
            return None
        
        return {
            'title': title if title else None,
            'author': author if author else None,
            'category': category if category else None,
            'description': description if description else None,
            'detailed_info': detailed_info if detailed_info else None,
            'quantity': quantity
        }

    @staticmethod
    def delete_book_form() -> int:
        """
        Get book ID to delete
        
        Returns:
            Book ID or None if cancelled
        """
        AdminView.clear_screen()
        AdminView.print_header("DELETE BOOK")
        
        try:
            book_id = int(input(Fore.YELLOW + "📌 Enter Book ID to delete: ").strip())
            return book_id
        except ValueError:
            AdminView.print_error("ID must be a number!")
            AdminView.pause()
            return None

    @staticmethod
    def confirm_delete_book(book) -> bool:
        """
        Show book details and confirm deletion
        
        Args:
            book: Book object to delete
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        print(Fore.CYAN + "\n📖 Book Information:")
        print(Fore.YELLOW + "─" * 80)
        print(Fore.WHITE + f"ID: {book.book_id}")
        print(Fore.WHITE + f"Title: {book.title}")
        print(Fore.WHITE + f"Author: {book.author}")
        print(Fore.WHITE + f"Quantity: {book.total_quantity} (Borrowed: {book.total_quantity - book.available_quantity})")
        print(Fore.YELLOW + "─" * 80 + "\n")
        
        return AdminView.get_confirmation(Fore.RED + "⚠️  CONFIRM DELETE THIS BOOK?")

    @staticmethod
    def display_categories(categories: List[str]):
        """
        Display list of categories
        
        Args:
            categories: List of category names
        """
        AdminView.clear_screen()
        AdminView.print_header("BOOK CATEGORIES")
        
        if not categories:
            AdminView.print_error("No categories found!")
            AdminView.pause()
            return
        
        print(Fore.CYAN + "Available Categories:\n")
        for i, category in enumerate(categories, 1):
            print(Fore.WHITE + f"  {i}. {category}")
        
        print()
        choice = input(Fore.YELLOW + "➤ Select category number to view books (or Enter to go back): ").strip()
        
        return choice

    # ==================== MEMBER MANAGEMENT ====================
    
    @staticmethod
    def show_member_management_menu() -> str:
        """
        Display member management menu
        
        Returns:
            User's menu choice
        """
        AdminView.clear_screen()
        AdminView.print_header("MEMBER MANAGEMENT")
        
        print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════╗")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "1. ➕ Add New Member" + " " * 16 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "2. 📋 View All Members" + " " * 13 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "3. 🔍 Search Members" + " " * 15 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "4. ✏️  Update Member Info" + " " * 11 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "5. 🔒 Lock/Unlock Account" + " " * 10 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "6. 📜 View Borrow History" + " " * 10 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "7. 🗑️  Delete Member" + " " * 16 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.RED + "0. ⬅️  Back" + " " * 24 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════╝")
        print()
        
        choice = input(Fore.YELLOW + "➤ Enter your choice: " + Fore.WHITE).strip()
        return choice

    @staticmethod
    def add_member_form() -> Dict:
        """
        Display form to add a new member
        
        Returns:
            Dictionary with member information or None if cancelled
        """
        AdminView.clear_screen()
        AdminView.print_header("ADD NEW MEMBER")
        
        print(Fore.CYAN + "Enter member information:")
        print(Fore.YELLOW + "─" * 80 + "\n")
        
        username = input(Fore.WHITE + "👤 Username: ").strip()
        password = input(Fore.WHITE + "🔑 Password: ").strip()
        full_name = input(Fore.WHITE + "📝 Full Name: ").strip()
        email = input(Fore.WHITE + "📧 Email (optional): ").strip()
        phone = input(Fore.WHITE + "📱 Phone (optional): ").strip()
        
        if not AdminView.get_confirmation("\nConfirm adding this member?"):
            AdminView.print_info("Operation cancelled!")
            AdminView.pause()
            return None
        
        return {
            'username': username,
            'password': password,
            'full_name': full_name,
            'email': email,
            'phone': phone
        }

    @staticmethod
    def display_members_table(members: List[Dict], page: int, total_pages: int):
        """
        Display members in a formatted table
        
        Args:
            members: List of member dictionaries
            page: Current page number
            total_pages: Total number of pages
        """
        if not members:
            AdminView.print_error("No members found!")
            return
        
        AdminView.clear_screen()
        AdminView.print_header(f"MEMBER LIST (Page {page}/{total_pages})")
        
        table_data = []
        for member in members:
            status_color = Fore.GREEN if member['account_status'] == 'Active' else Fore.RED
            table_data.append([
                member['user_id'],
                member['username'][:20],
                member['full_name'][:30],
                member['email'][:25] if member['email'] else 'N/A',
                member['phone'] if member['phone'] else 'N/A',
                status_color + member['account_status'] + Style.RESET_ALL,
                f"{member['fine_balance']:,.0f}"
            ])
        
        headers = [
            Fore.CYAN + "ID", "Username", "Full Name", "Email", 
            "Phone", "Status", "Fine (VND)" + Style.RESET_ALL
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()

    @staticmethod
    def display_members_list(members: List[Dict], page: int, total_pages: int) -> str:
        """
        Display members list with pagination controls
        
        Args:
            members: List of member dictionaries
            page: Current page number
            total_pages: Total number of pages
            
        Returns:
            User's navigation choice
        """
        AdminView.display_members_table(members, page, total_pages)
        
        if total_pages > 1:
            print(Fore.YELLOW + f"Page {page}/{total_pages}")
            print(Fore.CYAN + "[N] Next Page | [P] Previous Page | [Enter] Back")
            choice = input(Fore.YELLOW + "➤ ").strip().lower()
            return choice
        else:
            AdminView.pause()
            return ''

    @staticmethod
    def display_member_history(history: List[Dict], user_id: int):
        """
        Display borrowing history for a member
        
        Args:
            history: List of borrow record dictionaries
            user_id: ID of the member
        """
        AdminView.clear_screen()
        AdminView.print_header(f"BORROW HISTORY - Member ID: {user_id}")
        
        if not history:
            AdminView.print_error("No borrow history found!")
            AdminView.pause()
            return
        
        table_data = []
        for record in history:
            status_color = Fore.GREEN if record['status'] == 'Returned' else Fore.YELLOW
            table_data.append([
                record['borrow_id'],
                record['book_title'][:40],
                record['borrow_date'],
                record['due_date'],
                record['return_date'] if record['return_date'] else 'Not returned',
                f"{record['overdue_fine']:,.0f}",
                status_color + record['status'] + Style.RESET_ALL
            ])
        
        headers = [Fore.CYAN + "ID", "Book Title", "Borrow Date", "Due Date", "Return Date", "Fine (VND)", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
        AdminView.pause()

    # ==================== BORROW RECORDS MANAGEMENT ====================
    
    @staticmethod
    def show_borrow_records_menu() -> str:
        """
        Display borrow records management menu
        
        Returns:
            User's menu choice
        """
        AdminView.clear_screen()
        AdminView.print_header("BORROW RECORDS MANAGEMENT")
        
        print(Fore.WHITE + Style.BRIGHT + "╔════════════════════════════════════════╗")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "1. 📚 View All Records" + " " * 14 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "2. ⏳ View Borrowed Books" + " " * 11 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "3. ✅ View Returned Books" + " " * 11 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.CYAN + "4. ⚠️  View Overdue Books" + " " * 11 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "║  " + Fore.RED + "0. ⬅️  Back" + " " * 24 + Fore.WHITE + "║")
        print(Fore.WHITE + Style.BRIGHT + "╚════════════════════════════════════════╝")
        print()
        
        choice = input(Fore.YELLOW + "➤ Enter your choice: " + Fore.WHITE).strip()
        return choice

    @staticmethod
    def display_borrow_records(records: List[Dict], status_filter: str, page: int, total_pages: int) -> str:
        """
        Display borrow records with filtering and pagination
        
        Args:
            records: List of borrow record dictionaries
            status_filter: Current filter applied
            page: Current page number
            total_pages: Total number of pages
            
        Returns:
            User's navigation choice
        """
        filter_names = {
            'all': 'ALL RECORDS',
            'borrowed': 'CURRENTLY BORROWED',
            'returned': 'RETURNED BOOKS',
            'overdue': 'OVERDUE BOOKS'
        }
        
        if not records:
            AdminView.clear_screen()
            AdminView.print_header(f"BORROW RECORDS - {filter_names[status_filter]}")
            AdminView.print_error("No records found!")
            AdminView.pause()
            return ''
        
        AdminView.clear_screen()
        AdminView.print_header(f"BORROW RECORDS - {filter_names[status_filter]} (Page {page}/{total_pages})")
        
        table_data = []
        for record in records:
            status_color = Fore.GREEN if record['status'] == 'Returned' else Fore.YELLOW
            table_data.append([
                record['borrow_id'],
                record['username'][:15],
                record['full_name'][:25],
                record['book_title'][:30],
                record['borrow_date'],
                record['due_date'],
                record['return_date'] if record['return_date'] else 'Not returned',
                f"{record['overdue_fine']:,.0f}",
                status_color + record['status'] + Style.RESET_ALL
            ])
        
        headers = [
            Fore.CYAN + "ID", "Username", "Full Name", "Book Title", 
            "Borrow Date", "Due Date", "Return Date", "Fine (VND)", "Status"
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()
        
        if total_pages > 1:
            print(Fore.YELLOW + f"Page {page}/{total_pages}")
            print(Fore.CYAN + "[N] Next Page | [P] Previous Page | [Enter] Back")
            choice = input(Fore.YELLOW + "➤ ").strip().lower()
            return choice
        else:
            AdminView.pause()
            return ''

    # ==================== STATISTICS ====================
    
    @staticmethod
    def display_statistics(stats: Dict):
        """
        Display system statistics
        
        Args:
            stats: Dictionary containing statistics
        """
        AdminView.clear_screen()
        AdminView.print_header("SYSTEM STATISTICS")
        
        print(Fore.CYAN + Style.BRIGHT + "\n📊 Library Statistics\n")
        print(Fore.YELLOW + "─" * 60)
        
        print(Fore.WHITE + f"📚 Total Books:          {Fore.GREEN}{stats.get('total_books', 0):,}")
        print(Fore.WHITE + f"✅ Available Books:      {Fore.GREEN}{stats.get('available_books', 0):,}")
        print(Fore.WHITE + f"👥 Total Members:        {Fore.GREEN}{stats.get('total_members', 0):,}")
        print(Fore.WHITE + f"📖 Active Borrows:       {Fore.YELLOW}{stats.get('active_borrows', 0):,}")
        print(Fore.WHITE + f"⚠️  Overdue Books:        {Fore.RED}{stats.get('overdue_books', 0):,}")
        print(Fore.WHITE + f"💰 Total Fines:          {Fore.CYAN}{stats.get('total_fines', 0):,.0f} VND")
        
        print(Fore.YELLOW + "─" * 60)
        print()
        
        AdminView.pause()
