"""
Main Menu View - Main dashboard after login
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.book_list_view import BookListView
from views.borrow_view import BorrowView
from views.return_view import ReturnView
from views.history_view import HistoryView
from views.admin_view import AdminView
from views.change_password_view import ChangePasswordView

class MainMenuView:
    def __init__(self, root, user, on_logout):
        self.root = root
        self.user = user
        self.on_logout = on_logout
        
        # Configure root window
        self.root.title(f"Library Management System - {user['role']}")
        self.root.geometry("900x600")
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Top bar
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Welcome label
        welcome_label = ttk.Label(
            top_frame,
            text=f"Welcome, {self.user['full_name']} ({self.user['role']})",
            font=("Arial", 12, "bold")
        )
        welcome_label.pack(side=tk.LEFT)
        
        # Logout button
        logout_button = ttk.Button(
            top_frame,
            text="Logout",
            command=self.handle_logout
        )
        logout_button.pack(side=tk.RIGHT)
        
        # Change Password button
        change_pwd_button = ttk.Button(
            top_frame,
            text="Change Password",
            command=self.open_change_password
        )
        change_pwd_button.pack(side=tk.RIGHT, padx=5)
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10)
        
        # Main content frame
        content_frame = ttk.Frame(self.root, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            content_frame,
            text="📚 Library Management System",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Menu buttons frame
        menu_frame = ttk.Frame(content_frame)
        menu_frame.pack(expand=True)
        
        # Create menu based on role
        if self.user['role'] == 'Guest':
            self.create_guest_menu(menu_frame)
        elif self.user['role'] == 'Member':
            self.create_member_menu(menu_frame)
        elif self.user['role'] == 'Admin':
            self.create_admin_menu(menu_frame)
            
    def create_guest_menu(self, parent):
        """Create menu for Guest users"""
        # View Books button
        view_books_btn = ttk.Button(
            parent,
            text="📖 View All Books",
            command=self.open_book_list,
            width=30
        )
        view_books_btn.pack(pady=10)
        
        # Search Books button
        search_books_btn = ttk.Button(
            parent,
            text="🔍 Search Books",
            command=lambda: self.open_book_list(search_mode=True),
            width=30
        )
        search_books_btn.pack(pady=10)
        
    def create_member_menu(self, parent):
        """Create menu for Member users"""
        # View Books button
        view_books_btn = ttk.Button(
            parent,
            text="📖 View All Books",
            command=self.open_book_list,
            width=30
        )
        view_books_btn.pack(pady=10)
        
        # Search Books button
        search_books_btn = ttk.Button(
            parent,
            text="🔍 Search Books",
            command=lambda: self.open_book_list(search_mode=True),
            width=30
        )
        search_books_btn.pack(pady=10)
        
        # Borrow Book button
        borrow_book_btn = ttk.Button(
            parent,
            text="📚 Borrow Book",
            command=self.open_borrow,
            width=30
        )
        borrow_book_btn.pack(pady=10)
        
        # Return Book button
        return_book_btn = ttk.Button(
            parent,
            text="📥 Return Book",
            command=self.open_return,
            width=30
        )
        return_book_btn.pack(pady=10)
        
        # View History button
        history_btn = ttk.Button(
            parent,
            text="📋 View Borrowing History",
            command=self.open_history,
            width=30
        )
        history_btn.pack(pady=10)
        
    def create_admin_menu(self, parent):
        """Create menu for Admin users"""
        # Manage Books button
        manage_books_btn = ttk.Button(
            parent,
            text="📚 Manage Books",
            command=lambda: self.open_admin('books'),
            width=30
        )
        manage_books_btn.pack(pady=10)
        
        # Manage Members button
        manage_members_btn = ttk.Button(
            parent,
            text="👥 Manage Members",
            command=lambda: self.open_admin('members'),
            width=30
        )
        manage_members_btn.pack(pady=10)
        
        # Manage Borrow Records button
        manage_records_btn = ttk.Button(
            parent,
            text="📋 Manage Borrow Records",
            command=lambda: self.open_admin('records'),
            width=30
        )
        manage_records_btn.pack(pady=10)
        
        # View All Books button
        view_books_btn = ttk.Button(
            parent,
            text="📖 View All Books",
            command=self.open_book_list,
            width=30
        )
        view_books_btn.pack(pady=10)
        
    def open_book_list(self, search_mode=False):
        """Open book list window"""
        book_window = tk.Toplevel(self.root)
        BookListView(book_window, self.user, search_mode)
        
    def open_borrow(self):
        """Open borrow book window"""
        borrow_window = tk.Toplevel(self.root)
        BorrowView(borrow_window, self.user)
        
    def open_return(self):
        """Open return book window"""
        return_window = tk.Toplevel(self.root)
        ReturnView(return_window, self.user)
        
    def open_history(self):
        """Open history window"""
        history_window = tk.Toplevel(self.root)
        HistoryView(history_window, self.user)
        
    def open_admin(self, tab='books'):
        """Open admin panel"""
        admin_window = tk.Toplevel(self.root)
        AdminView(admin_window, self.user, tab)
        
    def open_change_password(self):
        """Open change password window"""
        if self.user['role'] == 'Guest':
            messagebox.showinfo("Guest Mode", "Guests cannot change password.")
            return
        change_pwd_window = tk.Toplevel(self.root)
        ChangePasswordView(change_pwd_window, self.user)
        
    def handle_logout(self):
        """Handle logout"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.on_logout()
