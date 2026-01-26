"""
History View - View borrowing history
"""
import tkinter as tk
from tkinter import ttk
from controllers.history_controller import HistoryController

class HistoryView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.history_controller = HistoryController()
        
        # Configure window
        self.root.title("Borrowing History")
        self.root.geometry("1200x600")
        
        # Data
        self.all_records = []
        
        # Create UI
        self.create_widgets()
        
        # Load history
        self.load_history()
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="📋 Borrowing History",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # Filter frame
        filter_frame = ttk.Frame(self.root, padding="10")
        filter_frame.pack(fill=tk.X)
        
        ttk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["all", "borrowed", "returned", "overdue"],
            state="readonly",
            width=15
        )
        status_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="Show All", command=self.load_history).pack(side=tk.LEFT, padx=5)
        
        # Results label
        self.results_label = ttk.Label(filter_frame, text="", font=("Arial", 9))
        self.results_label.pack(side=tk.RIGHT)
        
        # List frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = (
            "Record ID", "Book", "Author", 
            "Borrow Date", "Due Date", "Return Date",
            "Status", "Fine"
        )
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("Record ID", text="ID")
        self.tree.heading("Book", text="Book Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Borrow Date", text="Borrow Date")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Return Date", text="Return Date")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Fine", text="Fine (VND)")
        
        self.tree.column("Record ID", width=60, anchor=tk.CENTER)
        self.tree.column("Book", width=300)
        self.tree.column("Author", width=150)
        self.tree.column("Borrow Date", width=100, anchor=tk.CENTER)
        self.tree.column("Due Date", width=100, anchor=tk.CENTER)
        self.tree.column("Return Date", width=100, anchor=tk.CENTER)
        self.tree.column("Status", width=100, anchor=tk.CENTER)
        self.tree.column("Fine", width=100, anchor=tk.E)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Tag colors
        self.tree.tag_configure('overdue', foreground='red')
        self.tree.tag_configure('returned', foreground='green')
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self.root, text="Summary", padding="10")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.summary_label = ttk.Label(summary_frame, text="", font=("Arial", 10))
        self.summary_label.pack()
        
        # Bottom frame
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)
        
        ttk.Button(bottom_frame, text="Close", command=self.root.destroy).pack(side=tk.RIGHT)
        
    def load_history(self):
        """Load all borrowing history"""
        self.all_records = self.history_controller.get_member_history(self.user['user_id'])
        self.display_records(self.all_records)
        self.update_summary()
        
    def apply_filter(self):
        """Apply status filter"""
        status = self.status_var.get()
        
        if status == "all":
            filtered_records = self.all_records
        else:
            filtered_records = [
                r for r in self.all_records
                if r['status'].lower() == status.lower()
            ]
            
        self.display_records(filtered_records)
        
    def display_records(self, records):
        """Display records in treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert records
        for record in records:
            status = record['status']
            
            # Determine tag
            if status == 'Overdue':
                tag = 'overdue'
            elif status == 'Returned':
                tag = 'returned'
            else:
                tag = ''
                
            # Format fine
            fine_display = f"{record['fine']:,}" if record['fine'] > 0 else "-"
            
            # Format return date
            return_date = record['return_date'] if record['return_date'] else "-"
            
            self.tree.insert("", tk.END, values=(
                record['record_id'],
                record['book_title'],
                record['author'],
                record['borrow_date'],
                record['due_date'],
                return_date,
                status,
                fine_display
            ), tags=(tag,))
            
        # Update results count
        self.results_label.config(text=f"Showing {len(records)} record(s)")
        
    def update_summary(self):
        """Update summary statistics"""
        if not self.all_records:
            self.summary_label.config(text="No borrowing records found.")
            return
            
        total = len(self.all_records)
        borrowed = sum(1 for r in self.all_records if r['status'] == 'Borrowed')
        returned = sum(1 for r in self.all_records if r['status'] == 'Returned')
        overdue = sum(1 for r in self.all_records if r['status'] == 'Overdue')
        total_fine = sum(r['fine'] for r in self.all_records)
        
        summary = f"Total Records: {total} | "
        summary += f"Currently Borrowed: {borrowed} | "
        summary += f"Returned: {returned} | "
        summary += f"Overdue: {overdue} | "
        summary += f"Total Fines: {total_fine:,} VND"
        
        self.summary_label.config(text=summary)
