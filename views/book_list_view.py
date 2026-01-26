"""
Book List View - Display and search books
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.search_controller import SearchController
from controllers.display_controller import DisplayController

class BookListView:
    def __init__(self, root, user, search_mode=False):
        self.root = root
        self.user = user
        self.search_controller = SearchController()
        self.display_controller = DisplayController()
        
        # Configure window
        self.root.title("Books")
        self.root.geometry("1000x700")
        
        # Data
        self.current_books = []
        self.categories = self.display_controller.get_categories()
        
        # Create UI
        self.create_widgets()
        
        # Load initial data
        if search_mode:
            self.search_entry.focus()
        else:
            self.load_all_books()
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Top frame - Search and filters
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Search frame
        search_frame = ttk.LabelFrame(top_frame, text="Search", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry
        ttk.Label(search_frame, text="Keyword:").grid(row=0, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_books())
        
        # Search by
        ttk.Label(search_frame, text="Search by:").grid(row=0, column=2, padx=(20, 5))
        self.search_by_var = tk.StringVar(value="title")
        search_by_combo = ttk.Combobox(
            search_frame,
            textvariable=self.search_by_var,
            values=["title", "author", "category"],
            state="readonly",
            width=12
        )
        search_by_combo.grid(row=0, column=3)
        
        # Filter by availability
        ttk.Label(search_frame, text="Status:").grid(row=0, column=4, padx=(20, 5))
        self.status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(
            search_frame,
            textvariable=self.status_var,
            values=["all", "available", "borrowed"],
            state="readonly",
            width=12
        )
        status_combo.grid(row=0, column=5)
        
        # Buttons
        ttk.Button(search_frame, text="Search", command=self.search_books).grid(row=0, column=6, padx=5)
        ttk.Button(search_frame, text="Show All", command=self.load_all_books).grid(row=0, column=7)
        ttk.Button(search_frame, text="Clear", command=self.clear_search).grid(row=0, column=8)
        
        # Category and Sort frame
        filter_frame = ttk.Frame(top_frame)
        filter_frame.pack(fill=tk.X)
        
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=["All"] + self.categories,
            state="readonly",
            width=20
        )
        category_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Filter", command=self.filter_by_category).pack(side=tk.LEFT)
        
        ttk.Label(filter_frame, text="Sort by:").pack(side=tk.LEFT, padx=(20, 5))
        self.sort_var = tk.StringVar(value="title_asc")
        sort_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.sort_var,
            values=[
                "title_asc",
                "title_desc",
                "author_asc",
                "author_desc",
                "status"
            ],
            state="readonly",
            width=15
        )
        sort_combo.pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Sort", command=self.sort_books).pack(side=tk.LEFT, padx=5)
        
        # Results count
        self.results_label = ttk.Label(filter_frame, text="", font=("Arial", 9))
        self.results_label.pack(side=tk.RIGHT)
        
        # Tree frame
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = ("ID", "Title", "Author", "Category", "Status", "Available")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Available", text="Available Copies")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Title", width=300)
        self.tree.column("Author", width=200)
        self.tree.column("Category", width=150)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        self.tree.column("Available", width=120, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Double-click to view details
        self.tree.bind("<Double-1>", self.view_details)
        
        # Bottom buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.root.destroy).pack(side=tk.RIGHT)
        
    def load_all_books(self):
        """Load all books"""
        self.current_books = self.display_controller.get_all_books()
        self.display_books(self.current_books)
        
    def search_books(self):
        """Search books"""
        keyword = self.search_entry.get().strip()
        search_by = self.search_by_var.get()
        
        if not keyword:
            messagebox.showwarning("Input Required", "Please enter a search keyword.")
            return
            
        self.current_books = self.search_controller.search_books(keyword, search_by)
        self.display_books(self.current_books)
        
    def filter_by_category(self):
        """Filter books by category"""
        category = self.category_var.get()
        
        if category == "All":
            self.load_all_books()
        else:
            self.current_books = self.display_controller.get_books_by_category(category)
            self.display_books(self.current_books)
            
    def sort_books(self):
        """Sort current books"""
        sort_by = self.sort_var.get()
        
        if not self.current_books:
            return
            
        self.current_books = self.display_controller.sort_books(self.current_books, sort_by)
        self.display_books(self.current_books)
        
    def display_books(self, books):
        """Display books in treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Filter by status if needed
        status_filter = self.status_var.get()
        if status_filter != "all":
            books = [b for b in books if b['status'].lower() == status_filter]
            
        # Insert books
        for book in books:
            status_display = "✓ Available" if book['status'] == 'Available' else "✗ Borrowed"
            
            self.tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                status_display,
                f"{book['available_copies']}/{book['total_copies']}"
            ))
            
        # Update results count
        self.results_label.config(text=f"Found {len(books)} book(s)")
        
    def clear_search(self):
        """Clear search and filters"""
        self.search_entry.delete(0, tk.END)
        self.search_by_var.set("title")
        self.status_var.set("all")
        self.category_var.set("All")
        self.sort_var.set("title_asc")
        self.load_all_books()
        
    def view_details(self, event=None):
        """View book details"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to view details.")
            return
            
        item = self.tree.item(selection[0])
        book_id = item['values'][0]
        
        # Get full book details
        book = self.display_controller.get_book_details(book_id)
        
        if book:
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Book Details - {book['title']}")
            details_window.geometry("600x500")
            
            # Main frame
            main_frame = ttk.Frame(details_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Title
            title_label = ttk.Label(
                main_frame,
                text=book['title'],
                font=("Arial", 16, "bold"),
                wraplength=550
            )
            title_label.pack(pady=(0, 20))
            
            # Details frame
            details_frame = ttk.Frame(main_frame)
            details_frame.pack(fill=tk.BOTH, expand=True)
            
            # Book information
            info = [
                ("Book ID:", book['book_id']),
                ("Author:", book['author']),
                ("Category:", book['category']),
                ("Status:", book['status']),
                ("Available Copies:", f"{book['available_copies']} / {book['total_copies']}"),
                ("", ""),
                ("Description:", ""),
            ]
            
            row = 0
            for label, value in info:
                if label:
                    ttk.Label(details_frame, text=label, font=("Arial", 10, "bold")).grid(
                        row=row, column=0, sticky=tk.W, pady=5
                    )
                    ttk.Label(details_frame, text=value, font=("Arial", 10)).grid(
                        row=row, column=1, sticky=tk.W, padx=(10, 0), pady=5
                    )
                row += 1
                
            # Description text
            desc_text = tk.Text(details_frame, height=8, width=60, wrap=tk.WORD, font=("Arial", 10))
            desc_text.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
            desc_text.insert(1.0, book.get('description', 'No description available.'))
            desc_text.config(state=tk.DISABLED)
            
            # Close button
            ttk.Button(main_frame, text="Close", command=details_window.destroy).pack(pady=(20, 0))
