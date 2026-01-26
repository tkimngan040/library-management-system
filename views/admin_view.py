"""
Admin View - Admin management interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.admin_controller import AdminController
from datetime import datetime

class AdminView:
    def __init__(self, root, user, initial_tab='books'):
        self.root = root
        self.user = user
        self.admin_controller = AdminController()
        
        # Configure window
        self.root.title("Admin Panel")
        self.root.geometry("1200x700")
        
        # Create UI
        self.create_widgets(initial_tab)
        
    def create_widgets(self, initial_tab):
        """Create all UI widgets"""
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="🔧 Admin Panel",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.books_frame = ttk.Frame(self.notebook)
        self.members_frame = ttk.Frame(self.notebook)
        self.records_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.books_frame, text="📚 Manage Books")
        self.notebook.add(self.members_frame, text="👥 Manage Members")
        self.notebook.add(self.records_frame, text="📋 Manage Records")
        
        # Build each tab
        self.build_books_tab()
        self.build_members_tab()
        self.build_records_tab()
        
        # Select initial tab
        if initial_tab == 'members':
            self.notebook.select(1)
        elif initial_tab == 'records':
            self.notebook.select(2)
            
        # Close button
        close_button = ttk.Button(self.root, text="Close", command=self.root.destroy)
        close_button.pack(pady=10)
        
    # ==================== BOOKS TAB ====================
    
    def build_books_tab(self):
        """Build books management tab"""
        # Top buttons
        button_frame = ttk.Frame(self.books_frame, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add New Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Book", command=self.edit_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Book", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_books).pack(side=tk.RIGHT)
        
        # Search frame
        search_frame = ttk.Frame(self.books_frame, padding="10")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.book_search_entry = ttk.Entry(search_frame, width=40)
        self.book_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Clear", command=self.load_books).pack(side=tk.LEFT, padx=5)
        
        # Books list
        list_frame = ttk.Frame(self.books_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Title", "Author", "Category", "Total", "Available", "Status")
        self.books_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.books_tree.yview)
        
        for col in columns:
            self.books_tree.heading(col, text=col)
            
        self.books_tree.column("ID", width=50, anchor=tk.CENTER)
        self.books_tree.column("Title", width=300)
        self.books_tree.column("Author", width=200)
        self.books_tree.column("Category", width=120)
        self.books_tree.column("Total", width=80, anchor=tk.CENTER)
        self.books_tree.column("Available", width=80, anchor=tk.CENTER)
        self.books_tree.column("Status", width=100, anchor=tk.CENTER)
        
        self.books_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load books
        self.load_books()
        
    def load_books(self):
        """Load all books"""
        # Clear tree
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
            
        # Get books
        books = self.admin_controller.get_all_books()
        
        for book in books:
            self.books_tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['total_copies'],
                book['available_copies'],
                book['status']
            ))
            
    def search_books(self):
        """Search books"""
        keyword = self.book_search_entry.get().strip()
        
        if not keyword:
            self.load_books()
            return
            
        # Clear tree
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
            
        # Search
        books = self.admin_controller.search_books(keyword)
        
        for book in books:
            self.books_tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['total_copies'],
                book['available_copies'],
                book['status']
            ))
            
    def add_book(self):
        """Add new book"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.grid(row=0, column=1, pady=5)
        
        # Author
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5)
        author_entry = ttk.Entry(form_frame, width=40)
        author_entry.grid(row=1, column=1, pady=5)
        
        # Category
        ttk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        categories = self.admin_controller.get_categories()
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, values=categories, width=37)
        category_combo.grid(row=2, column=1, pady=5)
        
        # Total Copies
        ttk.Label(form_frame, text="Total Copies:").grid(row=3, column=0, sticky=tk.W, pady=5)
        copies_entry = ttk.Entry(form_frame, width=40)
        copies_entry.insert(0, "1")
        copies_entry.grid(row=3, column=1, pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(form_frame, width=40, height=10)
        desc_text.grid(row=4, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            category = category_var.get().strip()
            description = desc_text.get(1.0, tk.END).strip()
            
            try:
                total_copies = int(copies_entry.get().strip())
            except ValueError:
                messagebox.showerror("Invalid Input", "Total copies must be a number.")
                return
                
            if not all([title, author, category]):
                messagebox.showwarning("Missing Information", "Please fill all required fields.")
                return
                
            success, message = self.admin_controller.add_book(
                title, author, category, description, total_copies
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", message)
                
        ttk.Button(button_frame, text="Save", command=save_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def edit_book(self):
        """Edit selected book"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to edit.")
            return
            
        item = self.books_tree.item(selection[0])
        book_id = item['values'][0]
        
        # Get book details
        book = self.admin_controller.get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            return
            
        # Create edit dialog (similar to add_book)
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Book")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Pre-fill fields
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.insert(0, book['title'])
        title_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=5)
        author_entry = ttk.Entry(form_frame, width=40)
        author_entry.insert(0, book['author'])
        author_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        categories = self.admin_controller.get_categories()
        category_var = tk.StringVar(value=book['category'])
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, values=categories, width=37)
        category_combo.grid(row=2, column=1, pady=5)
        
        ttk.Label(form_frame, text="Total Copies:").grid(row=3, column=0, sticky=tk.W, pady=5)
        copies_entry = ttk.Entry(form_frame, width=40)
        copies_entry.insert(0, str(book['total_copies']))
        copies_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(form_frame, width=40, height=10)
        desc_text.insert(1.0, book.get('description', ''))
        desc_text.grid(row=4, column=1, pady=5)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def update_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            category = category_var.get().strip()
            description = desc_text.get(1.0, tk.END).strip()
            
            try:
                total_copies = int(copies_entry.get().strip())
            except ValueError:
                messagebox.showerror("Invalid Input", "Total copies must be a number.")
                return
                
            success, message = self.admin_controller.update_book(
                book_id, title, author, category, description, total_copies
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", message)
                
        ttk.Button(button_frame, text="Update", command=update_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        
    def delete_book(self):
        """Delete selected book"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to delete.")
            return
            
        item = self.books_tree.item(selection[0])
        book_id = item['values'][0]
        book_title = item['values'][1]
        
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this book?\n\n{book_title}"
        )
        
        if result:
            success, message = self.admin_controller.delete_book(book_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_books()
            else:
                messagebox.showerror("Error", message)
                
    # ==================== MEMBERS TAB ====================
    
    def build_members_tab(self):
        """Build members management tab"""
        # Top buttons
        button_frame = ttk.Frame(self.members_frame, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Add New Member", command=self.add_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Member", command=self.edit_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Member", command=self.delete_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View History", command=self.view_member_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_members).pack(side=tk.RIGHT)
        
        # Search
        search_frame = ttk.Frame(self.members_frame, padding="10")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.member_search_entry = ttk.Entry(search_frame, width=40)
        self.member_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_members).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Clear", command=self.load_members).pack(side=tk.LEFT, padx=5)
        
        # Members list
        list_frame = ttk.Frame(self.members_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Username", "Full Name", "Email", "Phone", "Role", "Status")
        self.members_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.members_tree.yview)
        
        for col in columns:
            self.members_tree.heading(col, text=col)
            
        self.members_tree.column("ID", width=50, anchor=tk.CENTER)
        self.members_tree.column("Username", width=120)
        self.members_tree.column("Full Name", width=200)
        self.members_tree.column("Email", width=200)
        self.members_tree.column("Phone", width=120)
        self.members_tree.column("Role", width=80, anchor=tk.CENTER)
        self.members_tree.column("Status", width=80, anchor=tk.CENTER)
        
        self.members_tree.pack(fill=tk.BOTH, expand=True)
        
        self.load_members()
        
    def load_members(self):
        """Load all members"""
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
            
        members = self.admin_controller.get_all_members()
        
        for member in members:
            self.members_tree.insert("", tk.END, values=(
                member['user_id'],
                member['username'],
                member['full_name'],
                member['email'],
                member['phone'],
                member['role'],
                member['account_status']
            ))
            
    def search_members(self):
        """Search members"""
        keyword = self.member_search_entry.get().strip()
        
        if not keyword:
            self.load_members()
            return
            
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
            
        members = self.admin_controller.search_members(keyword)
        
        for member in members:
            self.members_tree.insert("", tk.END, values=(
                member['user_id'],
                member['username'],
                member['full_name'],
                member['email'],
                member['phone'],
                member['role'],
                member['account_status']
            ))
            
    def add_member(self):
        """Add new member"""
        messagebox.showinfo("Info", "Add Member feature - Create dialog similar to Add Book")
        
    def edit_member(self):
        """Edit member"""
        selection = self.members_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a member to edit.")
            return
        messagebox.showinfo("Info", "Edit Member feature")
        
    def delete_member(self):
        """Delete member"""
        selection = self.members_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a member to delete.")
            return
            
        item = self.members_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this member?\n\nUsername: {username}"
        )
        
        if result:
            success, message = self.admin_controller.delete_member(user_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_members()
            else:
                messagebox.showerror("Error", message)
                
    def view_member_history(self):
        """View member's borrowing history"""
        selection = self.members_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a member.")
            return
        messagebox.showinfo("Info", "View Member History feature")
        
    # ==================== RECORDS TAB ====================
    
    def build_records_tab(self):
        """Build borrow records management tab"""
        # Top buttons
        button_frame = ttk.Frame(self.records_frame, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Label(button_frame, text="Filter by Status:").pack(side=tk.LEFT)
        
        self.record_status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(
            button_frame,
            textvariable=self.record_status_var,
            values=["all", "borrowed", "returned", "overdue"],
            state="readonly",
            width=15
        )
        status_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Apply Filter", command=self.filter_records).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Refresh", command=self.load_records).pack(side=tk.RIGHT)
        
        # Records list
        list_frame = ttk.Frame(self.records_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Member", "Book", "Borrow Date", "Due Date", "Return Date", "Status", "Fine")
        self.records_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.records_tree.yview)
        
        for col in columns:
            self.records_tree.heading(col, text=col)
            
        self.records_tree.column("ID", width=50, anchor=tk.CENTER)
        self.records_tree.column("Member", width=150)
        self.records_tree.column("Book", width=250)
        self.records_tree.column("Borrow Date", width=100, anchor=tk.CENTER)
        self.records_tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.records_tree.column("Return Date", width=100, anchor=tk.CENTER)
        self.records_tree.column("Status", width=100, anchor=tk.CENTER)
        self.records_tree.column("Fine", width=100, anchor=tk.E)
        
        self.records_tree.pack(fill=tk.BOTH, expand=True)
        
        self.records_tree.tag_configure('overdue', foreground='red')
        
        self.load_records()
        
    def load_records(self):
        """Load all borrow records"""
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        records = self.admin_controller.get_all_borrow_records()
        
        for record in records:
            tag = 'overdue' if record['status'] == 'Overdue' else ''
            fine = f"{record['fine']:,}" if record['fine'] > 0 else "-"
            return_date = record['return_date'] if record['return_date'] else "-"
            
            self.records_tree.insert("", tk.END, values=(
                record['record_id'],
                record['member_name'],
                record['book_title'],
                record['borrow_date'],
                record['due_date'],
                return_date,
                record['status'],
                fine
            ), tags=(tag,))
            
    def filter_records(self):
        """Filter records by status"""
        status = self.record_status_var.get()
        
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        if status == "all":
            records = self.admin_controller.get_all_borrow_records()
        else:
            records = self.admin_controller.filter_borrow_records(status)
            
        for record in records:
            tag = 'overdue' if record['status'] == 'Overdue' else ''
            fine = f"{record['fine']:,}" if record['fine'] > 0 else "-"
            return_date = record['return_date'] if record['return_date'] else "-"
            
            self.records_tree.insert("", tk.END, values=(
                record['record_id'],
                record['member_name'],
                record['book_title'],
                record['borrow_date'],
                record['due_date'],
                return_date,
                record['status'],
                fine
            ), tags=(tag,))
