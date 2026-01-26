"""
Return View - Return borrowed books interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.return_controller import ReturnController
from datetime import datetime

class ReturnView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.return_controller = ReturnController()
        
        # Configure window
        self.root.title("Return Book")
        self.root.geometry("1000x600")
        
        # Data
        self.borrowed_books = []
        
        # Create UI
        self.create_widgets()
        
        # Load borrowed books
        self.load_borrowed_books()
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="📥 Return Book",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # Info label
        self.info_label = ttk.Label(
            self.root,
            text="",
            font=("Arial", 10)
        )
        self.info_label.pack(pady=5)
        
        # Books list frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ("Record ID", "Book", "Author", "Borrow Date", "Due Date", "Days Left", "Status")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading("Record ID", text="Record ID")
        self.tree.heading("Book", text="Book Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Borrow Date", text="Borrow Date")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Days Left", text="Days Left")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Record ID", width=80, anchor=tk.CENTER)
        self.tree.column("Book", width=300)
        self.tree.column("Author", width=150)
        self.tree.column("Borrow Date", width=100, anchor=tk.CENTER)
        self.tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.tree.column("Days Left", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Tag colors for overdue
        self.tree.tag_configure('overdue', foreground='red')
        self.tree.tag_configure('due_soon', foreground='orange')
        
        # Bottom frame
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)
        
        ttk.Button(
            bottom_frame,
            text="Return Selected Book",
            command=self.return_book
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            bottom_frame,
            text="Refresh",
            command=self.load_borrowed_books
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bottom_frame, text="Close", command=self.root.destroy).pack(side=tk.RIGHT)
        
    def load_borrowed_books(self):
        """Load borrowed books for current user"""
        self.borrowed_books = self.return_controller.get_borrowed_books(self.user['user_id'])
        self.display_books(self.borrowed_books)
        
        # Update info label
        if not self.borrowed_books:
            self.info_label.config(text="You have no borrowed books.")
        else:
            overdue_count = sum(1 for b in self.borrowed_books if b['days_left'] < 0)
            if overdue_count > 0:
                self.info_label.config(
                    text=f"You have {len(self.borrowed_books)} borrowed book(s), {overdue_count} overdue!",
                    foreground="red"
                )
            else:
                self.info_label.config(
                    text=f"You have {len(self.borrowed_books)} borrowed book(s).",
                    foreground="black"
                )
                
    def display_books(self, books):
        """Display borrowed books in treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert books
        for book in books:
            days_left = book['days_left']
            
            if days_left < 0:
                status = "OVERDUE"
                tag = 'overdue'
            elif days_left <= 3:
                status = "Due Soon"
                tag = 'due_soon'
            else:
                status = "Active"
                tag = ''
                
            self.tree.insert("", tk.END, values=(
                book['record_id'],
                book['book_title'],
                book['author'],
                book['borrow_date'],
                book['due_date'],
                f"{days_left} days" if days_left >= 0 else f"{abs(days_left)} days",
                status
            ), tags=(tag,))
            
    def return_book(self):
        """Return selected book"""
        selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book to return.")
            return
            
        item = self.tree.item(selection[0])
        record_id = item['values'][0]
        book_title = item['values'][1]
        days_left = int(item['values'][5].split()[0])
        
        # Calculate fine if overdue
        fine = 0
        if days_left < 0:
            overdue_days = abs(days_left)
            fine = self.return_controller.calculate_fine(overdue_days)
            
        # Confirm return
        message = f"Do you want to return this book?\n\n"
        message += f"Book: {book_title}\n"
        message += f"Return Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        
        if fine > 0:
            message += f"\n⚠️ OVERDUE FINE: {fine:,} VND\n"
            message += f"Overdue by {abs(days_left)} day(s)\n"
            message += "\nThis fine will be added to your account."
            
        result = messagebox.askyesno("Confirm Return", message)
        
        if result:
            # Perform return
            success, return_message = self.return_controller.return_book(record_id)
            
            if success:
                if fine > 0:
                    messagebox.showinfo(
                        "Success",
                        f"{return_message}\n\nFine: {fine:,} VND has been added to your account."
                    )
                else:
                    messagebox.showinfo("Success", return_message)
                    
                self.load_borrowed_books()  # Refresh list
            else:
                messagebox.showerror("Error", return_message)
