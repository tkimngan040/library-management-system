"""
Borrow View - Borrow books interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.borrow_controller import BorrowController
from controllers.display_controller import DisplayController
from datetime import datetime, timedelta

class BorrowView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.borrow_controller = BorrowController()
        self.display_controller = DisplayController()
        
        # Configure window
        self.root.title("Borrow Book")
        self.root.geometry("900x600")
        
        # Data
        self.available_books = []
        
        # Create UI
        self.create_widgets()
        
        # Load books
        self.load_available_books()
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="📚 Borrow Book",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # Info frame
        info_frame = ttk.LabelFrame(self.root, text="Borrowing Information", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Check eligibility
        eligibility = self.borrow_controller.check_borrow_eligibility(self.user['user_id'])
        
        if eligibility['eligible']:
            status_text = "✓ You are eligible to borrow books"
            status_color = "green"
        else:
            status_text = f"✗ {eligibility['message']}"
            status_color = "red"
            
        status_label = ttk.Label(
            info_frame,
            text=status_text,
            foreground=status_color,
            font=("Arial", 10, "bold")
        )
        status_label.pack()
        
        # Borrowing stats
        stats_text = f"Currently borrowed: {eligibility.get('borrowed_count', 0)}/5 books"
        if eligibility.get('overdue_count', 0) > 0:
            stats_text += f" | Overdue: {eligibility['overdue_count']} books"
        if eligibility.get('total_fine', 0) > 0:
            stats_text += f" | Fines: {eligibility['total_fine']:,} VND"
            
        stats_label = ttk.Label(info_frame, text=stats_text, font=("Arial", 9))
        stats_label.pack(pady=(5, 0))
        
        # Search frame
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_books)
        
        ttk.Button(search_frame, text="Refresh", command=self.load_available_books).pack(side=tk.RIGHT)
        
        # Books list frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ("ID", "Title", "Author", "Category", "Available")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading("ID", text="Book ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Available", text="Available")
        
        self.tree.column("ID", width=70, anchor=tk.CENTER)
        self.tree.column("Title", width=300)
        self.tree.column("Author", width=200)
        self.tree.column("Category", width=150)
        self.tree.column("Available", width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)
        
        self.borrow_button = ttk.Button(
            bottom_frame,
            text="Borrow Selected Book",
            command=self.borrow_book,
            state=tk.NORMAL if eligibility['eligible'] else tk.DISABLED
        )
        self.borrow_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bottom_frame, text="Close", command=self.root.destroy).pack(side=tk.RIGHT)
        
    def load_available_books(self):
        """Load available books"""
        all_books = self.display_controller.get_all_books()
        self.available_books = [b for b in all_books if b['status'] == 'Available']
        self.display_books(self.available_books)
        
    def display_books(self, books):
        """Display books in treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert books
        for book in books:
            self.tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                f"{book['available_copies']} copies"
            ))
            
    def filter_books(self, event=None):
        """Filter books by search keyword"""
        keyword = self.search_entry.get().strip().lower()
        
        if not keyword:
            self.display_books(self.available_books)
            return
            
        filtered_books = [
            book for book in self.available_books
            if keyword in book['title'].lower() or keyword in book['author'].lower()
        ]
        
        self.display_books(filtered_books)
        
    def borrow_book(self):
        """Borrow selected book"""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to borrow.")
            return
            
        item = self.tree.item(selection[0])
        book_id = item['values'][0]
        book_title = item['values'][1]
        
        # Confirm borrow
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=14)
        
        message = f"Do you want to borrow this book?\n\n"
        message += f"Book: {book_title}\n"
        message += f"Borrow Date: {borrow_date.strftime('%Y-%m-%d')}\n"
        message += f"Due Date: {due_date.strftime('%Y-%m-%d')}\n"
        message += f"(You have 14 days to return this book)"
        
        result = messagebox.askyesno("Confirm Borrow", message)
        
        if result:
            # Perform borrow
            success, message = self.borrow_controller.borrow_book(
                self.user['user_id'],
                book_id
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_available_books()  # Refresh list
            else:
                messagebox.showerror("Error", message)
