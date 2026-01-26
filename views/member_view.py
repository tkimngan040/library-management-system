import tkinter as tk
from tkinter import ttk, messagebox
from controllers.borrow_controller import BorrowController
from controllers.return_controller import ReturnController
from controllers.history_controller import HistoryController
from controllers.search_controller import SearchController

class MemberView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.create_widgets()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        browse_frame = tk.Frame(notebook)
        borrow_frame = tk.Frame(notebook)
        history_frame = tk.Frame(notebook)
        
        notebook.add(browse_frame, text='Browse Books')
        notebook.add(borrow_frame, text='My Borrowed Books')
        notebook.add(history_frame, text='History')
        
        tk.Label(browse_frame, text="Browse and Borrow Books",
                font=('Arial', 16)).pack(pady=20)
